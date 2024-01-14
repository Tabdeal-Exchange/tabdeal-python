import json
from typing import Sequence

from tabdeal.client import Client
from tabdeal.enums import OrderSides, OrderTypes, RequestTypes, SecurityTypes
from tabdeal.utils import add_symbol_to_data, check_new_order_params


class IsolatedMargin(Client):
    # Isolated Margin

    def transfer(
            self,
            asset: str,
            symbol: str,
            amount: str,
            trans_from: str,
            trans_to: str):

        data = {
            "asset": asset,
            "amount": str(amount),
            "transFrom": trans_from,
            "transTo": trans_to,
        }
        add_symbol_to_data(data, symbol)

        return self.request(
            url="margin/isolated/transfer",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def transfer_spot_to_isolated_margin(self, asset: str,
                                symbol: str,
                                amount: str):
        return self.transfer(asset=asset, symbol=symbol, amount=amount, trans_from="SPOT", trans_to="ISOLATED_MARGIN")

    def transfer_isolated_margin_to_spot(self, asset: str,
                                         symbol: str,
                                         amount: str):
        return self.transfer(asset=asset, symbol=symbol, amount=amount, trans_from="ISOLATED_MARGIN", trans_to="SPOT")

    def get_isolated_margin_account(self, symbols=None, tabdeal_symbols=None):
        symbols_str = ""
        tabdeal_symbols_str = ""
        data = {}
        if symbols is not None:
            for symbol in symbols:
                symbols_str += f"{symbol},"
            data["symbols"] = symbols_str[:-1]
        elif tabdeal_symbols is not None:
            for symbol in tabdeal_symbols:
                tabdeal_symbols += f"{symbol},"
            data["tabdeal_symbols"] = tabdeal_symbols_str[:-1]

        return self.request(
            url="margin/isolated/account/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data
        )

    def get_all_assets(
            self,
    ):

        return self.request(
            url="margin/allAssets",
            method=RequestTypes.GET,
            security_type=SecurityTypes.NONE
        )

    def get_transfers(self, asset: str = None, symbol: str = None, type: str = None,
                      start_time: int = None,
                      end_time: int = None,
                      size: int = None,
                      current: int = None
                      ):
        data = {}
        if asset:
            data["asset"] = asset
        if type:
            data["type"] = type
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if current:
            data["current"] = current
        if size:
            data["size"] = size
        if symbol:
            data["symbol"] = symbol

        return self.request(
            url="margin/isolated/transfer/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def create_margin_order(
            self,
            symbol: str,
            side: OrderSides,
            type: OrderTypes,
            borrow_quantity: str,
            quantity: str,
            client_order_id: str = None,
            price: str = None,
            stop_price: str = None
    ):

        data = {
            "side": side.value,
            "type": type.value,
            "quantity": quantity,
            "price": 0 if not price else price,
            "stopPrice": 0 if not stop_price else stop_price,
            "borrow_quantity": 0 if not borrow_quantity else borrow_quantity
        }

        add_symbol_to_data(data, symbol)

        if client_order_id:
            data.update({"newClientOrderId": client_order_id})

        return self.request(
            url="margin/order/",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_open_margin_orders(self, symbol: str = None):
        return self.client_get_open_orders(symbol=symbol, url="margin/openOrders")

    def cancel_margin_order(
            self, symbol: str, order_id: int = None, client_order_id: str = None
    ):
        return self.cancel_order(symbol=symbol, order_id=order_id, client_order_id=client_order_id, url="margin/order")

    def get_margin_order(self, symbol: str, order_id: int = None, client_order_id: str = None):
        return self.get_order(symbol=symbol, order_id=order_id, client_order_id=client_order_id)

    def get_all_margin_orders(
            self,
            symbol: str,
            start_time: int = None,
            end_time: int = None,
            limit: int = None,
    ):
        return self.client_get_orders(symbol=symbol, start_time=start_time, end_time=end_time, limit=limit,
                                      url="margin/allOrders")

    def get_margin_repay_details(self, asset: str = None, isolatedSymbol: str = None, txId: str = None,
                                 start_time: int = None,
                                 end_time: int = None,
                                 size: int = None,
                                 current: int = None
                                 ):
        data = {}
        if asset:
            data["asset"] = asset
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if current:
            data["current"] = current
        if size:
            data["size"] = size
        if isolatedSymbol:
            data["isolatedSymbol"] = isolatedSymbol
        if txId:
            data["txId"] = txId

        return self.request(
            url="margin/repay/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_margin_loan_details(self, asset: str, tx_id: str=None):
        data = {"asset": asset}
        if tx_id is not None:
            data["tx_id"] = tx_id
        return self.request(
            url="margin/loan/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_margin_force_liquidation_rec(self, isolatedSymbol: str = None, txId: str = None,
                                         start_time: int = None,
                                         end_time: int = None,
                                         size: int = None,
                                         current: int = None
                                         ):
        data = {}
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if current:
            data["current"] = current
        if size:
            data["size"] = size
        if isolatedSymbol:
            data["isolatedSymbol"] = isolatedSymbol
        if txId:
            data["txId"] = txId

        return self.request(
            url="margin/forceLiquidationRec/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def get_interests(self, asset: str = None, isolatedSymbol: str = None,
                      start_time: int = None,
                      end_time: int = None,
                      size: int = None,
                      current: int = None
                      ):
        data = {}
        if asset:
            data["asset"] = asset
        if type:
            data["type"] = type
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if current:
            data["current"] = current
        if size:
            data["size"] = size
        if isolatedSymbol:
            data["isolatedSymbol"] = isolatedSymbol

        return self.request(
            url="margin/interestHistory/",
            method=RequestTypes.GET,
            security_type=SecurityTypes.TRADE,
            data=data,
        )

    def cancel_margin_open_orders(self, symbol: str):
        return self.client_cancel_open_orders(symbol=symbol, url="margin/openOrders")
