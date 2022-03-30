from enum import Enum


class SecurityTypes(Enum):
    TRADE = "TRADE"
    NONE = "NONE"


class RequestTypes(Enum):
    GET = "GET"
    POST = "POST"


class OrderSides(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderTypes(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LIMIT = "STOP_LOSS_LIMIT"
