from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from tabdeal.exceptions import CoreException
from tabdeal.future import Future
from tabdeal.spot import Spot


APP_DIR_NAME = "TabdealPythonSDK"
CONFIG_FILE_NAME = "config.json"
DEFAULT_BASE_URL = "https://api1.tabdeal.org"


class QuickstartError(CoreException):
    pass


@dataclass
class InstallResult:
    command: List[str]
    returncode: int
    output: str


def app_home() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return root / APP_DIR_NAME
    return Path.home() / ".local" / "share" / "tabdeal-python-sdk"


def config_path() -> Path:
    return app_home() / CONFIG_FILE_NAME


def ensure_app_home() -> Path:
    path = app_home()
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_config() -> dict:
    defaults = {
        "api_key": "",
        "api_secret": "",
        "base_url": DEFAULT_BASE_URL,
        "market": "spot",
        "example_symbol": "BTC_IRT",
    }
    path = config_path()
    if not path.exists():
        return defaults.copy()

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    merged = defaults.copy()
    merged.update(data)
    return merged


def save_config(config: dict) -> Path:
    ensure_app_home()
    path = config_path()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
    return path


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def install_target() -> str:
    root = project_root()
    if (root / "setup.py").exists():
        return str(root)
    return "tabdeal-python"


def run_command(command: List[str]) -> InstallResult:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    return InstallResult(
        command=command,
        returncode=completed.returncode,
        output=completed.stdout.strip(),
    )


def install_or_update_sdk(python_executable: Optional[str] = None) -> InstallResult:
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


def _build_client(config: dict):
    base_url = config.get("base_url") or DEFAULT_BASE_URL
    market = (config.get("market") or "spot").lower()
    if market == "future":
        return Future(
            api_key=config.get("api_key") or None,
            api_secret=config.get("api_secret") or None,
            base_url=base_url,
        )
    return Spot(
        api_key=config.get("api_key") or None,
        api_secret=config.get("api_secret") or None,
        base_url=base_url,
    )


def test_public_connection(config: dict) -> dict:
    client = _build_client(config)
    return client.ping()


def test_authenticated_connection(config: dict) -> dict:
    if not config.get("api_key") or not config.get("api_secret"):
        raise QuickstartError("API key and API secret are required for authenticated checks.")
    client = _build_client(config)
    return client.account()


def example_script_path() -> Path:
    return ensure_app_home() / "example_client.py"


def generate_example_script(config: dict) -> Path:
    market = (config.get("market") or "spot").lower()
    base_url = config.get("base_url") or DEFAULT_BASE_URL
    symbol = config.get("example_symbol") or ("BTCUSDT" if market == "future" else "BTC_IRT")
    class_name = "Future" if market == "future" else "Spot"
    import_name = "future" if market == "future" else "spot"

    code = f'''from tabdeal.{import_name} import {class_name}

api_key = "{config.get("api_key", "")}"
api_secret = "{config.get("api_secret", "")}"

client = {class_name}(api_key=api_key, api_secret=api_secret, base_url="{base_url}")

print("Ping:", client.ping())
print("Exchange info:", client.exchange_info(symbol="{symbol}"))
'''

    target = example_script_path()
    with target.open("w", encoding="utf-8") as handle:
        handle.write(code)
    return target
