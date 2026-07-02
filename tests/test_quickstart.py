import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tabdeal.quickstart import (
    DEFAULT_BASE_URL,
    QuickstartError,
    generate_example_script,
    load_config,
    save_config,
    test_authenticated_connection,
)


class QuickstartTests(unittest.TestCase):
    def test_load_config_returns_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                config = load_config()

        self.assertEqual(config["base_url"], DEFAULT_BASE_URL)
        self.assertEqual(config["market"], "spot")
        self.assertEqual(config["example_symbol"], "BTC_IRT")

    def test_save_config_creates_local_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                path = save_config({"market": "future", "example_symbol": "BTCUSDT"})
                loaded = load_config()
                saved_exists = path.exists()

        self.assertTrue(saved_exists)
        self.assertEqual(loaded["market"], "future")
        self.assertEqual(loaded["example_symbol"], "BTCUSDT")
        self.assertEqual(loaded["api_key"], "")
        self.assertEqual(loaded["api_secret"], "")

    def test_generate_example_script_uses_placeholders_not_real_secrets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                path = generate_example_script(
                    {
                        "api_key": "REAL_KEY_123",
                        "api_secret": "REAL_SECRET_456",
                        "market": "future",
                        "example_symbol": "BTCUSDT",
                    }
                )
                content = path.read_text(encoding="utf-8")

        self.assertIn('os.getenv("TABDEAL_API_KEY", "YOUR_API_KEY_HERE")', content)
        self.assertIn('os.getenv("TABDEAL_API_SECRET", "YOUR_API_SECRET_HERE")', content)
        self.assertIn("from tabdeal.future import Future", content)
        self.assertIn('symbol="BTCUSDT"', content)
        self.assertNotIn("REAL_KEY_123", content)
        self.assertNotIn("REAL_SECRET_456", content)

    def test_generate_example_script_refuses_to_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                generate_example_script({})
                with self.assertRaises(QuickstartError):
                    generate_example_script({})

    def test_account_test_requires_keys_without_network(self):
        with self.assertRaises(QuickstartError):
            test_authenticated_connection({})


if __name__ == "__main__":
    unittest.main()
