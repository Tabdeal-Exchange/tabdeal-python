# Tabdeal API Python SDK

Official python package to use [Tabdeal](https://www.tabdeal.org/) API


## Installation

```
$ pip install tabdeal-python
```

## Usage

```
from tabdeal.enums import OrderSides, OrderTypes
from tabdeal.spot import Spot

api_key = '<api_key>'
api_secret = '<api_secret>'


client = Spot(api_key, api_secret)

order = client.new_order(symbol='BTC_IRT',
                         side=OrderSides.BUY,
                         type=OrderTypes.MARKET,
                         quantity=0.002)
```
