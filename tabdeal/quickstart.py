import json
import os
import subprocess
import sys
from pathlib import Path

from tabdeal.exceptions import CoreException
from tabdeal.future import Future
from tabdeal.spot import Spot


APP_DIR_NAME = "TabdealPythonSDK"
CONFIG_FILE_NAME = "config.json"
EXAMPLE_FILE_NAME = "example_client.py"
DEFAULT_BASE_URL = "https://api1.tabdeal.org"
DEFAULT_MARKET = "spot"
DEFAULT_SYMBOL = "BTC_IRT"


class QuickstartError(CoreException):
    pass


class InstallResult(object):
    def __init__(self, command, returncode, output):
        self.command = command
        self.returncode = returncode
        self.output = output


def app_home():
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return root / APP_DIR_NAME
    return Path.home() / ".local" / "share" / "tabdeal-python-sdk"


def config_path():
    return app_home() / CONFIG_FILE_NAME


def example_script_path():
    return app_home() / EXAMPLE_FILE_NAME


def ensure_app_home():
    path = app_home()
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_config():
    return {
        "api_key": "",
        "api_secret": "",
        "base_url": DEFAULT_BASE_URL,
        "market": DEFAULT_MARKET,
        "example_symbol": DEFAULT_SYMBOL,
    }


def load_config():
    path = config_path()
    config = default_config()
    if not path.exists():
        return config

    with path.open("r", encoding="utf-8") as handle:
        config.update(json.load(handle))

    return config


def save_config(config, overwrite=False):
    ensure_app_home()
    path = config_path()
    if path.exists() and not overwrite:
        raise QuickstartError("Config already exists. Refusing to overwrite without explicit permission.")

    merged = default_config()
    merged.update(config)

    with path.open("w", encoding="utf-8") as handle:
        json.dump(merged, handle, indent=2, sort_keys=True)

    return path


def project_root():
    return Path(__file__).resolve().parent.parent


def install_target():
    root = project_root()
    if (root / "setup.py").exists():
        return str(root)
    return "tabdeal-python"


def run_command(command):
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return InstallResult(command, completed.returncode, completed.stdout.strip())


def install_or_update_sdk(python_executable=None):
    python_executable = python_executable or sys.executable
    return run_command(
        [
            python_executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            install_target(),
        ]
    )


def build_client(config):
    normalized = default_config()
    normalized.update(config or {})
    market = str(normalized.get("market") or DEFAULT_MARKET).lower()
    api_key = normalized.get("api_key") or None
    api_secret = normalized.get("api_secret") or None
    base_url = normalized.get("base_url") or DEFAULT_BASE_URL

    if market == "future":
        return Future(api_key=api_key, api_secret=api_secret, base_url=base_url)

    return Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)


def test_public_connection(config):
    client = build_client(config)
    return client.ping()


def test_authenticated_connection(config):
    normalized = default_config()
    normalized.update(config or {})
    if not normalized.get("api_key") or not normalized.get("api_secret"):
        raise QuickstartError("API key and API secret are required for the account test.")

    client = build_client(normalized)
    return client.account()


def generate_example_script(config, overwrite=False):
    ensure_app_home()
    path = example_script_path()
    if path.exists() and not overwrite:
        raise QuickstartError("Example script already exists. Refusing to overwrite it automatically.")

    normalized = default_config()
    normalized.update(config or {})
    market = str(normalized.get("market") or DEFAULT_MARKET).lower()
    class_name = "Future" if market == "future" else "Spot"
    module_name = "future" if market == "future" else "spot"
    symbol = normalized.get("example_symbol") or DEFAULT_SYMBOL
    base_url = normalized.get("base_url") or DEFAULT_BASE_URL

    contents = """import os

from tabdeal.{module_name} import {class_name}


API_KEY = os.getenv("TABDEAL_API_KEY", "YOUR_API_KEY_HERE")
API_SECRET = os.getenv("TABDEAL_API_SECRET", "YOUR_API_SECRET_HERE")
BASE_URL = os.getenv("TABDEAL_BASE_URL", "{base_url}")


def main():
    # Quickstart helper only. No real trading is performed by this example.
    client = {class_name}(api_key=API_KEY, api_secret=API_SECRET, base_url=BASE_URL)
    print("Ping:", client.ping())
    print("Exchange info:", client.exchange_info(symbol="{symbol}"))


if __name__ == "__main__":
    main()
""".format(
        module_name=module_name,
        class_name=class_name,
        base_url=base_url,
        symbol=symbol,
    )

    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(contents)

    return path
