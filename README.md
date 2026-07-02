# Tabdeal API Python SDK
[![PyPI version](https://img.shields.io/pypi/v/tabdeal-python)](https://pypi.python.org/pypi/tabdeal-python)
[![Python version](https://img.shields.io/pypi/pyversions/tabdeal-python)](https://www.python.org/downloads/)



Official python package to use [Tabdeal Exchange](https://www.tabdeal.org/) API

## Quickstart Panel

This fork adds a beginner-friendly desktop quickstart helper for local setup only.

- credentials are stored locally on the current machine only
- no real trading is performed by the panel or generated example
- the panel only supports SDK install/update, public ping, account test, config save, and example generation

### Windows

```powershell
.\install.ps1
```

### Linux

```bash
chmod +x install.sh
./install.sh
```

### Safe local configuration

- use placeholders from `.env.example`
- generated example files read credentials from environment variables
- example generation refuses to overwrite an existing file automatically

## Installation

```bash
pip install tabdeal-python
```

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
python -m compileall tabdeal tests
python -m unittest discover -s tests
```
