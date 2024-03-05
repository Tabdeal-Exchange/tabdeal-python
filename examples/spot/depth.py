#!/usr/bin/env python

import logging
from tabdeal.spot import Spot as Client
from tabdeal.utils import config_logger

config_logger(logging, logging.DEBUG)

spot_client = Client()

logging.info(spot_client.depth("BTCUSDT"))
logging.info(spot_client.depth("BTCUSDT", limit=10))
