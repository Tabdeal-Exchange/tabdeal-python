# Tabdeal

Unofficial python package to use Tabdeal API

[//]: # (## Getting Started)

[//]: # ()
[//]: # (These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.)

[//]: # (### Prerequisites)

[//]: # ()
[//]: # (The things you need before installing the software.)

[//]: # ()
[//]: # (* You need this)

[//]: # (* And you need this)
[//]: # (* Oh, and don't forget this)

### Installation

[//]: # (A step by step guide that will tell you how to get the development environment up and running.)

```
$ pip install tabdeal
```

## Usage

[//]: # (A few examples of useful commands and/or tasks.)

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

[//]: # (## Deployment)

[//]: # ()
[//]: # (Additional notes on how to deploy this on a live or release system. Explaining the most important branches, what pipelines they trigger and how to update the database &#40;if anything special&#41;.)

[//]: # ()
[//]: # (### Server)

[//]: # ()
[//]: # (* Live:)

[//]: # (* Release:)

[//]: # (* Development:)

[//]: # ()
[//]: # (### Branches)

[//]: # ()
[//]: # (* Master:)

[//]: # (* Feature:)

[//]: # (* Bugfix:)

[//]: # (* etc...)

[//]: # ()
[//]: # (## Additional Documentation and Acknowledgments)

[//]: # ()
[//]: # (* Project folder on server:)

[//]: # (* Confluence link:)

[//]: # (* Asana board:)

[//]: # (* etc...)
