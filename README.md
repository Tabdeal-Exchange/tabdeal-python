# Tabdeal API Python SDK
[![PyPI version](https://img.shields.io/pypi/v/tabdeal-python)](https://pypi.python.org/pypi/tabdeal-python)
[![Python version](https://img.shields.io/pypi/pyversions/tabdeal-python)](https://www.python.org/downloads/)



Official python package to use [Tabdeal Exchange](https://www.tabdeal.org/) API


## Installation

```bash
pip install tabdeal-python
```

## Documentation

[https://docs.tabdeal.org](https://docs.tabdeal.org/)

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
                         quantity=0.002)

print(order)
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
