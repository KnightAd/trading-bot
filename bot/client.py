import os
import time
import hmac
import hashlib
import requests
from bot.logging_config import logger

# Base URL for Binance Futures Demo (USDT-M)
BASE_URL = "https://demo-fapi.binance.com"


def _get_credentials():
    """Read API key and secret from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise EnvironmentError(
            "Binance API credentials not found. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET environment variables (or create a .env file)."
        )
    return api_key, api_secret


def _get_server_time() -> int:
    """Fetch the current server timestamp from Binance to avoid clock-sync issues."""
    resp = requests.get(f"{BASE_URL}/fapi/v1/time", timeout=10)
    resp.raise_for_status()
    return resp.json()["serverTime"]


def _sign(query_string: str, secret: str) -> str:
    """Generate HMAC-SHA256 signature for a query string."""
    return hmac.new(
        secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def signed_request(method: str, path: str, params: dict | None = None) -> dict:
    """Send a signed request to the Binance Futures Demo API.

    Parameters
    ----------
    method : str
        HTTP method – ``"GET"`` or ``"POST"``.
    path : str
        API path, e.g. ``"/fapi/v1/order"``.
    params : dict, optional
        Query / body parameters (excluding ``timestamp`` and ``signature``).

    Returns
    -------
    dict
        Parsed JSON response from Binance.
    """
    api_key, api_secret = _get_credentials()

    if params is None:
        params = {}

    # Attach server timestamp and a generous recvWindow
    params["recvWindow"] = 60000
    params["timestamp"] = _get_server_time()

    # Build the query string deterministically
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    signature = _sign(query_string, api_secret)
    query_string += f"&signature={signature}"

    url = f"{BASE_URL}{path}?{query_string}"
    headers = {"X-MBX-APIKEY": api_key}

    logger.info(f"Sending {method} request to {path} | params={params}")

    if method.upper() == "GET":
        resp = requests.get(url, headers=headers, timeout=15)
    else:
        resp = requests.post(url, headers=headers, timeout=15)

    data = resp.json()

    if resp.status_code != 200:
        error_msg = data.get("msg", resp.text)
        logger.error(f"API error {data.get('code')}: {error_msg}")
        raise RuntimeError(f"Binance API error {data.get('code')}: {error_msg}")

    logger.info(f"Response from {path}: {data}")
    return data
