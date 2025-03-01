from __future__ import annotations

import json
import logging
import warnings

import odoo
from odoo.service import security

from . import json_encoding
from .redis_config import RedisConfig

MAJOR = odoo.release.version_info[0]
try:
    with warnings.catch_warnings(record=True):
        import werkzeug.contrib.sessions as sessions
except ImportError:
    from odoo.tools._vendor import sessions


_logger = logging.getLogger("odoo.session.REDIS")


# this is equal to the duration of the session garbage collector in
# odoo.http.session_gc()


_logger = logging.getLogger(__name__)


class RedisSessionStore(sessions.SessionStore):
    """SessionStore that saves session to redis"""

    def __init__(
        self,
        redis_config: RedisConfig,
        session_class,
    ):
        super().__init__(session_class=session_class)
        self.redis = redis_config.connect()
        self.expiration = redis_config.expiration
        self.anon_expiration = redis_config.anon_expiration
        self.support_expire = b"expire" in self.redis.command_list()
        self.prefix = "session:"
        if redis_config.prefix:
            self.prefix = f"{self.prefix}:{redis_config.prefix}:"

    def build_key(self, sid):
        return f"{self.prefix}{sid}"

    def get_expiration(self, session):
        # session.expiration allow to set a custom expiration for a session
        # such as a very short one for monitoring requests
        if not self.support_expire:
            return -1
        expiration = session.expiration or self.anon_expiration
        if session.uid:
            expiration = session.expiration or self.expiration
        return expiration

    def save(self, session):
        key = self.build_key(session.sid)
        expiration = self.get_expiration(session)
        if _logger.isEnabledFor(logging.DEBUG):
            if session.uid:
                user_msg = f"user '{session.login}' (id: {session.uid})"
            else:
                user_msg = "anonymous user"
            _logger.debug(
                "saving session with key '%s' and expiration of %s seconds for %s",
                key,
                expiration,
                user_msg,
            )

        data = json.dumps(dict(session), cls=json_encoding.SessionEncoder).encode("utf-8")
        result = self.redis.set(key, data)
        if result and self.support_expire:
            return self.redis.expire(key, expiration)
        return -1

    def delete(self, session):
        key = self.build_key(session.sid)
        _logger.debug("deleting session with key %s", key)
        return self.redis.delete(key)

    def get(self, sid):
        if not self.is_valid_key(sid):
            _logger.debug(
                "session with invalid sid '%s' has been asked, returning a new one",
                sid,
            )
            return self.new()

        key = self.build_key(sid)
        saved = self.redis.get(key)
        if not saved:
            _logger.debug(
                "session with non-existent key '%s' has been asked, returning a new one",
                key,
            )
            return self.new()
        try:
            data = json.loads(saved.decode("utf-8"), cls=json_encoding.SessionDecoder)
        except ValueError:
            _logger.debug(
                "session for key '%s' has been asked but its json content could not be read, it has been reset",
                key,
            )
            data = {}
        return self.session_class(data, sid, False)

    def list(self):
        keys = self.redis.keys(f"{self.prefix}*")
        _logger.debug("a listing redis keys has been called")
        return [key[len(self.prefix) :] for key in keys]

    def rotate(self, session, env):
        self.delete(session)
        session.sid = self.generate_key()
        if session.uid and env:
            session.session_token = security.compute_session_token(session, env)
        self.save(session)

    def vacuum(self, *args, **kwargs):
        """Do not garbage collect the sessions

        Redis keys are automatically cleaned at the end of their
        expiration.
        """
        return None
