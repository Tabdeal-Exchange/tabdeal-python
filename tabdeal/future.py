from typing import Sequence

from tabdeal.client import Client
from tabdeal.enums import OrderSides, OrderTypes, RequestTypes, SecurityTypes


class Future(Client):
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        base_url="https://api1.tabdeal.org",
        timeout=None,
        receive_window=None,
    ):
        super().__init__(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            version="v1",
            timeout=timeout,
            receive_window=receive_window,
        )
        self.base_url = f"{base_url}/fapi/"
        self.base_read_url = f"{base_url}/r/fapi/"

    # Public market endpoints
    def ping(self):
        return self.request(
            url="v1/ping",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
        )

    def time(self):
        return self.request(
            url="v1/time",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
        )

    def exchange_info(self, symbol: str = None, symbols: Sequence[str] = None):
        data = {}
        if symbol:
            data["symbol"] = symbol
        elif symbols:
            data["symbols"] = ",".join([str(item).upper() for item in symbols])

        return self.request(
            url="v1/exchangeInfo",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    def depth(self, symbol: str, limit: int = None):
        data = {"symbol": symbol}
        if limit is not None:
            data["limit"] = limit

        return self.request(
            url="v1/depth",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    def agg_depth(self, symbol: str, aggregation_precision: str, limit_rows: int = None):
        data = {
            "symbol": symbol,
            "aggregationPrecision": aggregation_precision,
        }
        if limit_rows is not None:
            data["limitRows"] = limit_rows

        return self.request(
            url="v1/aggDepth",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE,
            data=data,
        )

    # Trading endpoints
    def new_order(
        self,
        symbol: str,
        side: OrderSides,
        type: OrderTypes,
        quantity: str = None,
        price: str = None,
        time_in_force: str = None,
        reduce_only: bool = None,
    ):
        data = {
            "symbol": symbol,
            "side": side.value,
            "type": type.value,
        }
        if quantity is not None:
            data["quantity"] = quantity
        if price is not None:
            data["price"] = price
        if time_in_force is not None:
            data["timeInForce"] = time_in_force
        if reduce_only is not None:
            data["reduceOnly"] = reduce_only

        return self.request(
            url="v1/order",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_order(self, symbol: str, order_id: int):
        data = {"symbol": symbol, "orderId": order_id}
        return self.request(
            url="v1/order",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_order(self, symbol: str, order_id: int):
        data = {"symbol": symbol, "orderId": order_id}
        return self.request(
            url="v1/order",
            method=RequestTypes.DELETE,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_open_orders(self, symbol: str = None, limit: int = None):
        data = {}
        if symbol:
            data["symbol"] = symbol
        if limit is not None:
            data["limit"] = limit
        return self.request(
            url="v1/openOrders",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_all_orders(
        self,
        symbol: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
        is_active: int = None,
        is_done: int = None,
    ):
        data = {"symbol": symbol}
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if limit is not None:
            data["limit"] = limit
        if is_active is not None:
            data["isActive"] = is_active
        if is_done is not None:
            data["isDone"] = is_done

        return self.request(
            url="v1/allOrders",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_leverage(self, symbol: str):
        return self.request(
            url="v1/leverage",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data={"symbol": symbol},
        )

    def change_leverage(self, symbol: str, leverage: int):
        return self.request(
            url="v1/leverage",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data={"symbol": symbol, "leverage": leverage},
        )

    def transfer(self, transfer_type: int, amount: str, asset: str):
        return self.request(
            url="v1/transfer",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data={"type": transfer_type, "amount": amount, "asset": asset},
        )

    def transfer_history(
        self,
        transfer_type: int = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
        purpose: str = None,
    ):
        data = {}
        if transfer_type is not None:
            data["type"] = transfer_type
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if limit is not None:
            data["limit"] = limit
        if purpose is not None:
            data["purpose"] = purpose

        return self.request(
            url="v1/transfer",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def user_trades(
        self,
        symbol: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ):
        data = {"symbol": symbol}
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if limit is not None:
            data["limit"] = limit

        return self.request(
            url="v1/userTrades",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def income(
        self,
        symbol: str = None,
        income_type: str = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ):
        data = {}
        if symbol:
            data["symbol"] = symbol
        if income_type:
            data["incomeType"] = income_type
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if limit is not None:
            data["limit"] = limit

        return self.request(
            url="v1/income",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def force_orders(self, symbol: str = None):
        data = {}
        if symbol:
            data["symbol"] = symbol
        return self.request(
            url="v1/forceOrders",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_positions(
        self,
        symbol: str = None,
        side: str = None,
        state: int = None,
        is_active: int = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ):
        data = {}
        if symbol:
            data["symbol"] = symbol
        if side:
            data["side"] = side
        if state is not None:
            data["state"] = state
        if is_active is not None:
            data["isActive"] = is_active
        if start_time is not None:
            data["startTime"] = start_time
        if end_time is not None:
            data["endTime"] = end_time
        if limit is not None:
            data["limit"] = limit

        return self.request(
            url="v1/position",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def close_position(self, symbol: str):
        return self.request(
            url="v1/position",
            method=RequestTypes.DELETE,
            security_type=SecurityTypes.TRADE,
            data={"symbol": symbol},
        )

    def position_sl_tp(
        self,
        position_id: int,
        symbol: str = None,
        sl_price: str = None,
        tp_price: str = None,
        working_type: str = None,
    ):
        data = {"positionId": position_id}
        if symbol:
            data["symbol"] = symbol
        if sl_price is not None:
            data["slPrice"] = sl_price
        if tp_price is not None:
            data["tpPrice"] = tp_price
        if working_type:
            data["workingType"] = working_type

        return self.request(
            url="v1/positionSlTp",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    # Account endpoints
    def position_risk(self, symbol: str = None):
        data = {}
        if symbol:
            data["symbol"] = symbol
        return self.request(
            url="v3/positionRisk",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def account(self):
        return self.request(
            url="v3/account",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
        )

    def balance(self):
        return self.request(
            url="v3/balance",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
        )
