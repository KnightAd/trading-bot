"""Order placement functions for Binance Futures Demo API.

Each function builds the correct parameters, delegates to
``client.signed_request``, and returns a concise dict with the
most useful fields from the API response.
"""

from bot.client import signed_request
from bot.logging_config import logger


def _summarise(response: dict) -> dict:
    """Extract the most useful fields from a raw order response."""
    return {
        "orderId": response.get("orderId"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice", response.get("price")),
    }


def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    """Place a MARKET order on Binance Futures Demo.

    Parameters
    ----------
    symbol : str   – e.g. ``"BTCUSDT"``
    side : str     – ``"BUY"`` or ``"SELL"``
    quantity : float

    Returns
    -------
    dict – concise order response
    """
    logger.info(f"Placing MARKET order | symbol={symbol}, side={side}, quantity={quantity}")
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    raw = signed_request("POST", "/fapi/v1/order", params)
    summary = _summarise(raw)
    logger.info(f"MARKET order response | {summary}")
    return summary


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    """Place a LIMIT order (GTC) on Binance Futures Demo.

    Parameters
    ----------
    symbol : str
    side : str
    quantity : float
    price : float

    Returns
    -------
    dict – concise order response
    """
    logger.info(
        f"Placing LIMIT order | symbol={symbol}, side={side}, "
        f"quantity={quantity}, price={price}"
    )
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price,
    }
    raw = signed_request("POST", "/fapi/v1/order", params)
    summary = _summarise(raw)
    logger.info(f"LIMIT order response | {summary}")
    return summary


def place_stop_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
) -> dict:
    """Place a STOP-LIMIT order on Binance Futures Demo.

    Parameters
    ----------
    symbol : str
    side : str
    quantity : float
    price : float      – limit price once stop triggers
    stop_price : float – the trigger price

    Returns
    -------
    dict – concise order response
    """
    logger.info(
        f"Placing STOP_LIMIT order | symbol={symbol}, side={side}, "
        f"quantity={quantity}, price={price}, stopPrice={stop_price}"
    )
    params = {
        "symbol": symbol,
        "side": side,
        "type": "STOP",
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price,
        "stopPrice": stop_price,
    }
    raw = signed_request("POST", "/fapi/v1/order", params)
    summary = _summarise(raw)
    logger.info(f"STOP_LIMIT order response | {summary}")
    return summary
