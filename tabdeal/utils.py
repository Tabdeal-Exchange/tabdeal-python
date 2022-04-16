from tabdeal.enums import OrderTypes
from tabdeal.exceptions import ParameterRequiredException


def check_new_order_params(order_type: OrderTypes, **kwargs):
    order_type_required_fields = {
        OrderTypes.LIMIT: ["price"],
        OrderTypes.MARKET: [],
        OrderTypes.STOP_LIMIT: ["stopPrice", "price"],
    }

    for field in order_type_required_fields.get(order_type):
        if not kwargs.get(field, None):
            raise ParameterRequiredException(param=field, action="new order")


def add_symbol_to_data(data, symbol):
    if "_" in symbol:
        data.update({"tabdealSymbol": symbol})
    else:
        data.update({"symbol": symbol})

    return data
