from typing import Sequence

from tabdeal.client import Client
from tabdeal.enums import OrderSides, OrderTypes, RequestTypes, SecurityTypes
from tabdeal.utils import add_symbol_to_data, check_new_order_params


class Spot(Client):
    # SPOT
    def new_order(
        self,
        symbol: str,
        side: OrderSides,
        type: OrderTypes,
        quantity: float,
        client_order_id: str = None,
        price: float = None,
        stop_price: float = None,
    ):
        check_new_order_params(type, price=price, stop_price=stop_price)

        data = {
            "side": side.value,
            "type": type.value,
            "quantity": quantity,
            "price": 0 if not price else price,
            "stopPrice": 0 if not stop_price else stop_price,
        }

        add_symbol_to_data(data, symbol)

        if client_order_id:
            data.update({"newClientOrderId": client_order_id})

        return self.request(
            url="order",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_open_orders(self, symbol: str = None):
        data = dict() if not symbol else add_symbol_to_data(dict(), symbol)

        return self.request(
            url="openOrders",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_order(self, symbol: str, order_id: int):
        data = {
            "orderId": order_id,
        }

        add_symbol_to_data(data, symbol)

        return self.request(
            url="order",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_order(self, symbol: str, order_id: int):
        data = {
            "orderId": order_id,
        }

        add_symbol_to_data(data, symbol)

        return self.request(
            url="order",
            method=RequestTypes.DELETE,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def my_trades(self, symbol: str):
        data = dict()

        add_symbol_to_data(data, symbol)

        return self.request(
            url="myTrades",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_orders(
        self,
        symbol: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ):
        data = dict()

        add_symbol_to_data(data, symbol)

        if start_time:
            data.update({"startTime": start_time})

        if end_time:
            data.update({"endTime": end_time})

        if limit:
            data.update({"limit": limit})

        return self.request(
            url="allOrders",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_open_orders(self, symbol: str):
        data = dict()

        add_symbol_to_data(data, symbol)

        return self.request(
            url="openOrders",
            method=RequestTypes.DELETE,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    # MARKET
    def depth(self, symbol: str, limit: int = None):
        data = dict()

        add_symbol_to_data(data, symbol)

        if limit:
            data.update({"limit": limit})

        return self.request(
            url="depth",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    def trades(self, symbol: str, limit: int = None):
        data = dict()

        add_symbol_to_data(data, symbol)

        if limit:
            data.update({"limit": limit})

        return self.request(
            url="trades",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    def exchange_info(self, symbol: str = None, symbols: Sequence[str] = None):
        data = dict()

        if symbol:
            add_symbol_to_data(data, symbol)

        elif symbols:
            symbols = '["' + '","'.join(symbols) + '"]'
            data.update({"symbols": symbols})

        return self.request(
            url="exchangeInfo",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    def ping(self):
        return self.request(
            url="ping",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
        )

    def time(self):
        return self.request(
            url="time",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
        )
