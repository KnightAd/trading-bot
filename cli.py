import os
from pathlib import Path

import typer
from dotenv import load_dotenv

from bot import validators, orders
from bot.logging_config import logger

app = typer.Typer(help="Simple Binance Futures Testnet trading bot")

# Load environment variables from a .env file if present (API keys)
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


@app.command()
def place_order(
    symbol: str = typer.Option(..., "--symbol", help="Trading pair, e.g., BTCUSDT"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET, LIMIT, or STOP_LIMIT"),
    quantity: str = typer.Option(..., "--quantity", "-q", help="Order quantity (positive number)"),
    price: str = typer.Option(None, "--price", "-p", help="Limit price (required for LIMIT or STOP_LIMIT)"),
    stop_price: str = typer.Option(None, "--stop-price", help="Stop price (required for STOP_LIMIT)"),
):
    """Place a MARKET, LIMIT, or STOP‑LIMIT order on Binance Futures Testnet.

    The function validates inputs, prints a summary, and displays the concise
    response returned by the API.
    """
    try:
        # Validation – will raise ValueError on failure
        symbol = validators.validate_symbol(symbol)
        side = validators.validate_side(side)
        order_type = validators.validate_order_type(order_type)
        quantity = validators.validate_quantity(quantity)
        price_val = validators.validate_price(price, order_type)
        stop_price_val = validators.validate_stop_price(stop_price, order_type)
    except ValueError as ve:
        typer.echo(f"[ERROR] Input validation failed: {ve}")
        raise typer.Exit(code=1)

    typer.echo("\n--- Order Request Summary ---")
    typer.echo(f"Symbol      : {symbol}")
    typer.echo(f"Side        : {side}")
    typer.echo(f"Order Type  : {order_type}")
    typer.echo(f"Quantity    : {quantity}")
    if order_type in ("LIMIT", "STOP_LIMIT"):
        typer.echo(f"Price       : {price_val}")
    if order_type == "STOP_LIMIT":
        typer.echo(f"Stop Price  : {stop_price_val}")
    typer.echo("------------------------------\n")

    try:
        if order_type == "MARKET":
            response = orders.place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            response = orders.place_limit_order(symbol, side, quantity, price_val)  # type: ignore[arg-type]
        else:  # STOP_LIMIT
            response = orders.place_stop_limit_order(
                symbol, side, quantity, price_val, stop_price_val  # type: ignore[arg-type]
            )
    except Exception as exc:
        typer.echo(f"[ERROR] Failed to place order: {exc}")
        logger.exception("Order placement failed")
        raise typer.Exit(code=1)

    typer.echo("--- Order Response ---")
    for key, val in response.items():
        typer.echo(f"{key}: {val}")
    typer.echo("----------------------")


if __name__ == "__main__":
    app()
