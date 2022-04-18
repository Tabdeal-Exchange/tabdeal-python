# Tabdeal

official python package to use Tabdeal API


## Installation

```
$ pip install tabdeal
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
