import logging
import time

from tabdeal.utils import config_logger
from tabdeal.websocket_client import SpotWebsocketClient as TabdealWS

config_logger(logging, logging.DEBUG)


def handler(message):
    print(message)


tabdeal_ws = TabdealWS()


tabdeal_ws.market_order_book(
    symbol="bnbusdt",
    id=1,
    callback=handler,
)


time.sleep(2)


tabdeal_ws.market_order_book(
    symbol="btcusdt",
    id=2,
    callback=handler,
)

time.sleep(30)

logging.debug("closing ws connection")
tabdeal_ws.stop()
