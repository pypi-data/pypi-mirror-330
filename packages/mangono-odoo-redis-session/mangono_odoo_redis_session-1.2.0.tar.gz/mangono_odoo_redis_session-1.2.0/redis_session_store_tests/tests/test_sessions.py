import redis

from odoo import http
from odoo.tests.common import HttpCase
from odoo.tools import config

from odoo.addons.redis_session_store.redis_config import RedisConfig
from odoo.addons.redis_session_store.redis_session import RedisSessionStore


def store() -> RedisSessionStore:
    return http.root.session_store


class TestSessions(HttpCase):
    def setUp(self):
        super().setUp()
        self.redis = RedisConfig.create_config(config)
        self.redis_conn: redis.Redis = self.redis.connect()

    def test_create_session(self):
        self.authenticate("admin", "admin")
        key = store().build_key(self.session.sid)
        self.assertTrue(self.redis_conn.exists(key))
