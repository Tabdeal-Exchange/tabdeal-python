from enum import Enum


class SecurityTypes(Enum):
    TRADE = "TRADE"
    USER_STREAM = "USER_STREAM"
    NONE = "NONE"


class RequestTypes(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class OrderSides(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderTypes(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LIMIT = "STOP_LOSS_LIMIT"
