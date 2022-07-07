import logging
import time

from tabdeal.spot import Spot as TabdealClient
from tabdeal.utils import config_logger
from tabdeal.websocket_client import SpotWebsocketClient as TabdealWS

config_logger(logging, logging.DEBUG)


def handler(message):
    print(message)


api_key = ""
client = TabdealClient(api_key=api_key)
response = client.new_listen_key()

logging.debug(f"listen key : {response['listenKey']}")

tabdeal_ws = TabdealWS()

tabdeal_ws.user_data(
    listen_key=response["listenKey"],
    callback=handler,
)

time.sleep(30)

logging.debug("closing ws connection")
tabdeal_ws.stop()
