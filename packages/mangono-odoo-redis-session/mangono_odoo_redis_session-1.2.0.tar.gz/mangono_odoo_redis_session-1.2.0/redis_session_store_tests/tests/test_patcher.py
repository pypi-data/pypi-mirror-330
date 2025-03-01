from __future__ import annotations

import odoo
from odoo.tests import TransactionCase

from odoo.addons.redis_session_store.redis_session import RedisSessionStore

MAJOR = odoo.release.version_info[0]


class TestRedisSessionStore(TransactionCase):
    def _get_store(self):
        return odoo.http.root.session_store

    def test_module_loaded(self):
        self.assertIn("redis_session_store", odoo.conf.server_wide_modules)

    def test_import_store_is_redis(self):
        """
        Assert the patched `session_store` property return a RedisSessionStore instance
        """
        session_store = self._get_store()
        self.assertIsNotNone(session_store)
        self.assertIsInstance(session_store, RedisSessionStore)
