from typing import Callable

from tabdeal.client import TabdealWebsocketClientThread


class SpotWebsocketClient:
    def __init__(self):
        self._websockets = []

    def subscribe(self, callback, stream=None, payload=None):
        ws = TabdealWebsocketClientThread(
            callback=callback, payload=payload, stream=stream
        )
        ws.start()

        self._websockets.append(ws)

    def market_order_book(self, symbol: str, id: int, callback: Callable):
        return self.subscribe(
            payload={
                "method": "SUBSCRIBE",
                "id": id,
                "params": [f"{symbol}@depth@2000ms"],
            },
            callback=callback,
        )

    def user_data(self, listen_key: str, callback):
        return self.subscribe(callback=callback, stream=listen_key)

    def stop(self):
        for _websocket in self._websockets:
            _websocket.join()
