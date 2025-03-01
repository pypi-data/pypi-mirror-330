from __future__ import annotations

import logging
import os

import odoo

from .redis_config import RedisConfig
from .redis_session import RedisSessionStore

_logger = logging.getLogger("odoo.session.REDIS")

try:
    import redis

    _logger.info("Lib redis installed")
except ImportError:
    redis = None

MAJOR = odoo.release.version_info[0]
if MAJOR >= 16:
    from odoo.http import Session as OdooSessionClass
else:
    from odoo.http import OpenERPSession as OdooSessionClass


@odoo.tools.func.lazy_property
def session_store(self):
    config = RedisConfig.create_config(odoo.tools.config)
    return RedisSessionStore(redis_config=config, session_class=OdooSessionClass)


REDIS_SESSION_STORE_ENABLE = False


def _post_load_module():
    if "redis_session_store" not in odoo.conf.server_wide_modules:
        return
    if not redis:
        raise ImportError("Please install package redis")
    redis_config = RedisConfig.create_config(odoo.tools.config)
    server_info = redis_config.connect().info()
    if not server_info and os.getenv("KV_HOST"):  # IN case this is a materia KV Redis compatible database
        server_info = {"redis_version": "CleverCloud Materia KV"}
    if not server_info:
        raise ValueError("Can't display server info")
    _logger.info("Redis Session enable [%s]", server_info["redis_version"])
    if MAJOR <= 15.0:
        odoo.http.Root.session_store = session_store
        odoo.http.session_gc = lambda s: None
    elif MAJOR >= 16.0:
        odoo.http.Application.session_store = session_store
        # There is no more session_gc global function.
        # Now See FilesystemSessionStore#vacuum
        # So no more patch need
