import re
from typing import Literal, Optional


def validate_symbol(symbol: str) -> str:
    """Validate Binance symbol (e.g., BTCUSDT). Must be 6‑12 uppercase alphanumerics."""
    pattern = re.compile(r"^[A-Z0-9]{6,12}$")
    if not pattern.fullmatch(symbol):
        raise ValueError(f"Invalid symbol '{symbol}'. Must be 6‑12 uppercase letters/numbers.")
    return symbol


def validate_side(side: str) -> Literal["BUY", "SELL"]:
    side_up = side.upper()
    if side_up not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL")
    return side_up  # type: ignore


def validate_order_type(order_type: str) -> Literal["MARKET", "LIMIT", "STOP_LIMIT"]:
    ot = order_type.upper()
    if ot not in {"MARKET", "LIMIT", "STOP_LIMIT"}:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT")
    return ot  # type: ignore


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except Exception:
        raise ValueError("Quantity must be a positive number")


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    """Validate regular price for LIMIT and STOP_LIMIT orders.

    For MARKET orders the price is ignored and this returns ``None``.
    """
    if order_type.upper() in {"LIMIT", "STOP_LIMIT"}:
        if price is None:
            raise ValueError("Price is required for LIMIT and STOP_LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError
            return p
        except Exception:
            raise ValueError("Price must be a positive number")
    return None


def validate_stop_price(stop_price: Optional[str], order_type: str) -> Optional[float]:
    """Validate stop price for STOP_LIMIT orders.

    For MARKET and LIMIT orders this returns ``None``.
    """
    if order_type.upper() == "STOP_LIMIT":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders")
        try:
            sp = float(stop_price)
            if sp <= 0:
                raise ValueError
            return sp
        except Exception:
            raise ValueError("Stop price must be a positive number")
    return None
