from typing import Callable

from tabdeal.client import TabdealWebsocketClientThread


class SpotWebsocketClient:
    def __init__(self):
        self._websockets = []

    def market_order_book(self, symbol: str, id: int, callback: Callable):
        ws = TabdealWebsocketClientThread(
            callback=callback,
            payload={
                "method": "SUBSCRIBE",
                "id": id,
                "params": [f"{symbol}@depth@2000ms"],
            },
        )
        ws.start()

        self._websockets.append(ws)

        return ws

    def stop(self):
        for _websocket in self._websockets:
            _websocket.join()
