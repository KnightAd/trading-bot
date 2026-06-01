# ui.py - Lightweight Streamlit UI for Binance Futures Testnet Trading Bot

"""A minimal graphical interface built with Streamlit.

Features
- Input fields for symbol, side, order type, quantity, and price (only for LIMIT).
- Shows request summary and response details.
- Logs activity via the existing bot.logging_config logger.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables (API keys) from .env if present
load_dotenv()

# Import bot components
from bot.orders import place_market_order, place_limit_order
from bot.logging_config import logger

st.set_page_config(page_title="Binance Trading Bot UI", page_icon="🚀", layout="centered")

st.title("🚀 Binance Futures Testnet Trading Bot")

with st.form(key="order_form"):
    symbol = st.text_input("Symbol", value="BTCUSDT")
    side = st.selectbox("Side", options=["BUY", "SELL"])
    order_type = st.selectbox("Order Type", options=["MARKET", "LIMIT"])
    quantity = st.text_input("Quantity", value="0.001")
    price = st.text_input("Price (required for LIMIT)", value="")
    submit = st.form_submit_button("Place Order")

if submit:
    # Basic validation
    try:
        quantity_val = float(quantity)
        if quantity_val <= 0:
            raise ValueError("Quantity must be positive")
        if order_type == "LIMIT":
            price_val = float(price)
            if price_val <= 0:
                raise ValueError("Price must be positive for LIMIT orders")
    except ValueError as e:
        st.error(f"❌ Input error: {e}")
        st.stop()

    st.write("**Request Summary:**")
    st.json({
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity_val,
        "price": price if order_type == "LIMIT" else None,
    })

    with st.spinner("Placing order…"):
        try:
            if order_type == "MARKET":
                result = place_market_order(symbol, side, quantity_val)
            else:
                result = place_limit_order(symbol, side, quantity_val, float(price))
            st.success("✅ Order placed successfully!")
            st.write("**Response:**")
            st.json(result)
        except Exception as exc:
            logger.exception("Error placing order via UI")
            st.error(f"❌ Order failed: {exc}")
