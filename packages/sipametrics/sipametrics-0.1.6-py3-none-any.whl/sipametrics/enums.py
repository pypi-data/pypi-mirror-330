from enum import Enum


class Products(Enum):
    PRIVATE_EQUITY = "pe"
    PRIVATE_INFRA = "pi"


class Apps(Enum):
    INDICES = "indices"
    VALUATION = "valuation"
    CLIMATE = "climate"
