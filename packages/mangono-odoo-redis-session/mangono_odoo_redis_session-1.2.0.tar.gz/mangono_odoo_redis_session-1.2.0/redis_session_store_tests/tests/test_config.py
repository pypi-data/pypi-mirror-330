from __future__ import annotations

import os
import unittest.mock

from odoo.tests import TransactionCase
from odoo.tools import config

from odoo.addons.redis_session_store.redis_config import (
    DEFAULT_SESSION_TIMEOUT,
    DEFAULT_SESSION_TIMEOUT_ANONYMOUS,
    RedisConfig,
)


class TestRedisSessionStore(TransactionCase):
    def _copy_config_with_misc(self, misc_data: dict[str, dict[str, str]]):
        new_config = type(config)()
        new_config.misc.update(misc_data)
        return new_config

    def test_import_store_is_redis(self):
        """
        Assert Parsing misc config
        """
        odoo_config = self._copy_config_with_misc(
            {
                "redis_sessions_store": {
                    "url": "redis://localhost:6379/0",
                    "prefix": "my-prefix",
                }
            }
        )
        with unittest.mock.patch.dict(os.environ, {}, clear=True):
            redis_config = RedisConfig.create_config(odoo_config)
        self.assertEqual(redis_config.prefix, "my-prefix")
        self.assertEqual(redis_config.expiration, DEFAULT_SESSION_TIMEOUT)
        self.assertEqual(redis_config.anon_expiration, DEFAULT_SESSION_TIMEOUT_ANONYMOUS)
        self.assertEqual(redis_config.url, "redis://localhost:6379/0")
