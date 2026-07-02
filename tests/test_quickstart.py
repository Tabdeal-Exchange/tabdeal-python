import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tabdeal import quickstart


class QuickstartTests(unittest.TestCase):
    def test_load_config_returns_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                config = quickstart.load_config()

        self.assertEqual(config["market"], "spot")
        self.assertEqual(config["base_url"], quickstart.DEFAULT_BASE_URL)

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                saved_path = quickstart.save_config(
                    {
                        "api_key": "k",
                        "api_secret": "s",
                        "base_url": "https://example.com",
                        "market": "future",
                        "example_symbol": "BTCUSDT",
                    }
                )
                loaded = quickstart.load_config()
                saved_exists = saved_path.exists()

        self.assertTrue(saved_exists)
        self.assertEqual(loaded["api_key"], "k")
        self.assertEqual(loaded["market"], "future")

    def test_generate_example_script_uses_market_specific_client(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            app_dir = Path(tmpdir)
            with patch("tabdeal.quickstart.app_home", return_value=app_dir):
                path = quickstart.generate_example_script(
                    {
                        "api_key": "demo",
                        "api_secret": "secret",
                        "base_url": "https://example.com",
                        "market": "future",
                        "example_symbol": "BTCUSDT",
                    }
                )
                content = path.read_text(encoding="utf-8")

        self.assertIn("from tabdeal.future import Future", content)
        self.assertIn('client = Future(', content)
        self.assertIn('symbol="BTCUSDT"', content)


if __name__ == "__main__":
    unittest.main()
