import json
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

    def get_order(self, symbol: str, order_id: int = None, client_order_id: str = None):
        data = dict()

        add_symbol_to_data(data, symbol)

        if client_order_id:
            data.update({"origClientOrderId": client_order_id})

        if order_id:
            data.update({"orderId": order_id})

        return self.request(
            url="order",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_order(
        self, symbol: str, order_id: int = None, client_order_id: str = None
    ):
        data = dict()

        add_symbol_to_data(data, symbol)

        if client_order_id:
            data.update({"origClientOrderId": client_order_id})

        if order_id:
            data.update({"orderId": order_id})

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

    def new_oco_order(
        self,
        symbol: str,
        side: OrderSides,
        quantity: float,
        price: float,
        stop_price: float,
        stop_limit_price: float,
        list_client_order_id: str = None,
        limit_client_order_id: str = None,
        stop_client_order_id: str = None,
    ):
        data = {
            "side": side.value,
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "stopLimitPrice": stop_limit_price,
        }

        add_symbol_to_data(data, symbol)

        if list_client_order_id:
            data.update({"listClientOrderId": list_client_order_id})
        if limit_client_order_id:
            data.update({"limitClientOrderId": limit_client_order_id})
        if stop_client_order_id:
            data.update({"stopClientOrderId": stop_client_order_id})

        return self.request(
            url="order/oco",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_oco_order(
        self, symbol: str, oco_id: int = None, client_oco_id: str = None
    ):
        data = dict()

        add_symbol_to_data(data, symbol)

        if oco_id:
            data.update({"orderListId": oco_id})

        if client_oco_id:
            data.update({"listClientOrderId": client_oco_id})

        return self.request(
            url="orderList",
            method=RequestTypes.DELETE,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_oco_order(self, oco_id: int = None, client_oco_id: str = None):
        data = dict()

        if oco_id:
            data.update({"orderListId": oco_id})

        if client_oco_id:
            data.update({"origClientOrderId": client_oco_id})

        return self.request(
            url="orderList",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_oco_orders(
        self, start_time: int = None, end_time: int = None, limit: int = None
    ):
        data = dict()

        if start_time:
            data.update({"startTime": start_time})

        if end_time:
            data.update({"endTime": end_time})

        if limit:
            data.update({"limit": limit})

        return self.request(
            url="allOrderList",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_oco_open_orders(self):
        return self.request(
            url="openOrderList",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
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

    def exchange_info(
        self,
        symbol: str = None,
        symbols: Sequence[str] = None,
        tabdeal_symbols: Sequence[str] = None,
    ):
        data = dict()

        if symbol:
            add_symbol_to_data(data, symbol)

        elif symbols:
            symbols = json.dumps(symbols)
            data.update({"symbols": symbols})

        elif tabdeal_symbols:
            tabdeal_symbols = json.dumps(tabdeal_symbols)
            data.update({"tabdealSymbols": tabdeal_symbols})

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
