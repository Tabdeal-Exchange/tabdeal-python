from tabdeal.client import Client
from tabdeal.enums import OrderSides, OrderTypes, RequestTypes, SecurityTypes
from tabdeal.utils import check_new_order_params


class Spot(Client):
    def new_order(
        self,
        symbol,
        side: OrderSides,
        type: OrderTypes,
        quantity: int,
        price: float = None,
        stop_price: float = None,
    ):
        check_new_order_params(type, price=price, stop_price=stop_price)

        data = {
            "symbol": symbol,
            "side": side.value,
            "type": type.value,
            "quantity": quantity,
            "price": 0 if not price else price,
            "stopPrice": 0 if not stop_price else stop_price,
        }

        return self.request(
            url="order",
            method=RequestTypes.POST,
            security_type=SecurityTypes.TRADE,
            data=data,
        )
