# Tabdeal API Python SDK
[![PyPI version](https://img.shields.io/pypi/v/tabdeal-python)](https://pypi.python.org/pypi/tabdeal-python)
[![Python version](https://img.shields.io/pypi/pyversions/tabdeal-python)](https://www.python.org/downloads/)

Official python package to use [Tabdeal Exchange](https://www.tabdeal.org/) API

## Quickstart Installer Panel

This repository now includes a beginner-friendly desktop quickstart panel for Windows and Linux.

It helps with:

- one-click virtual environment setup
- automatic SDK installation or update
- saving API key and secret locally
- public ping test
- authenticated account test
- generating a ready-to-run example script

### Windows one-click

Right click PowerShell and run:

```powershell
.\install.ps1
```

What it does:

- finds Python 3 or installs Python 3.11 with `winget` if available
- creates a dedicated virtual environment in `%LOCALAPPDATA%\TabdealPythonSDK\venv`
- installs this SDK from the current repository
- launches the desktop panel

### Linux one-click

```bash
chmod +x install.sh
./install.sh
```

What it does:

- installs Python and Tkinter if missing on common distros
- creates a dedicated virtual environment in `~/.local/share/tabdeal-python-sdk/venv`
- installs this SDK from the current repository
- launches the desktop panel

### Run the panel manually

After installation you can run:

```bash
tabdeal-panel
```

or:

```bash
python -m tabdeal
```

## Installation

```bash
pip install tabdeal-python
```

Recommended Python version: `3.9+`

## Documentation

[https://docs.tabdeal.org](https://docs.tabdeal.org/)

[Postman Collection](https://github.com/Tabdeal-Exchange/tabdeal-api-postman)

## RESTful APIs

Usage examples:
```python
from tabdeal.enums import OrderSides, OrderTypes
from tabdeal.spot import Spot

api_key = '<api_key>'
api_secret = '<api_secret>'


client = Spot(api_key, api_secret)

order = client.new_order(symbol='BTC_IRT',
                         side=OrderSides.BUY,
                         type=OrderTypes.MARKET,
                         quantity="0.002")

print(order)
```

## Future APIs

Usage example:
```python
from tabdeal.enums import OrderSides, OrderTypes
from tabdeal.future import Future

api_key = "<api_key>"
api_secret = "<api_secret>"

client = Future(api_key, api_secret)

client.ping()
client.exchange_info()

order = client.new_order(
    symbol="BTCUSDT",
    side=OrderSides.BUY,
    type=OrderTypes.MARKET,
    quantity="0.001",
)

print(order)
```

Special Margin websocket helpers:
```python
from tabdeal.websocket_client import (
    FutureWebsocketClient,
    FutureBroadcastWebsocketClient,
)

stream_ws = FutureWebsocketClient()
broadcast_ws = FutureBroadcastWebsocketClient()
```

### Exception

There are 2 types of exceptions returned from the library:
- `tabdeal.exceptions.ClientException`
    - This is thrown when server returns `4XX`, it's an issue from client side.
    - It has 4 properties:
        - `status` - HTTP status code
        - `code` - Server's error code
        - `message` - Server's error message
        - `detail` - Detail of exception
- `tabdeal.exceptions.ServerException`
    - This is thrown when server returns `5XX`, it's an issue from server side.

## Developer checks

```bash
python -m unittest discover -s tests
```

## Docker dev environment

```bash
docker compose up -d --build
docker compose exec sdk-dev python -m unittest discover -s tests
```
