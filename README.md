# Binance Futures Testnet Trading Bot

## Overview
A lightweight Python 3 command‑line tool that can place **MARKET** and **LIMIT** orders (BUY/SELL) on the Binance Futures Testnet (USDT‑M).  The code is deliberately split into a small, reusable library (`bot/`) and a thin Typer‑based CLI (`cli.py`).  Logging of every request, response and error is written to `logs/bot.log` using **loguru**.

## Project Structure
```
trading_bot/
├─ bot/
│   ├─ __init__.py          # package marker
│   ├─ client.py            # Binance client wrapper (testnet)
│   ├─ orders.py            # market & limit order functions
│   ├─ validators.py        # input validation helpers for CLI
│   └─ logging_config.py    # loguru rotating file logger
├─ logs/                     # generated at runtime (ignored in Git)
├─ cli.py                    # Typer entry point
├─ requirements.txt
├─ .gitignore                # exclude logs, env, pyc, etc.
└─ README.md
```

## Prerequisites
* Python 3.10+ (tested on 3.11)
* A Binance Futures **Testnet** account – create one at https://testnet.binancefuture.com and generate an **API Key** and **Secret**.
* (Optional) `git` if you want to clone the repo.

## Setup
```bash
# 1. Clone (or copy) the repository
git clone <repo‑url> trading_bot   # or download the zip you receive
cd trading_bot

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate   # on Windows PowerShell
# or: source venv/bin/activate   # on *nix

# 3. Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root (same folder as `cli.py`) containing:
```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret
```
The CLI automatically loads these variables via **python‑dotenv**.

## Usage
### Market Order
```bash
python cli.py place-order \
    --symbol BTCUSDT \
    --side BUY \
    --type MARKET \
    --quantity 0.001
```
### Limit Order
```bash
python cli.py place-order \
    --symbol ETHUSDT \
    --side SELL \
    --type LIMIT \
    --quantity 0.02 \
    --price 1800
```
The command prints a **request summary**, attempts the order, and then prints a concise **response** (`orderId`, `status`, `executedQty`, `avgPrice`).  All activity is also recorded in `logs/bot.log`.

## Logging
`bot/logging_config.py` configures **loguru** to write rotating logs (`5 MB` per file, keep 10 days).  Example log entries look like:
```
2026‑06‑01 14:10:23 | INFO | bot.orders: Placing MARKET order | symbol='BTCUSDT', side='BUY', quantity=0.001
2026‑06‑01 14:10:24 | INFO | bot.orders: Market order response | response={...}
```
Two example logs (`market_order.log` and `limit_order.log`) are provided in the `logs/` directory.

## Assumptions & Limitations
* Only **USDT‑M** Futures testnet is supported (the base URL is hard‑coded).
* The bot does **not** implement advanced order types (Stop‑Limit, OCO, etc.) – they can be added later.
* No UI; the CLI is intentionally minimal.
* Errors from Binance are re‑raised after logging; the CLI exits with a non‑zero code.

## Extending the Bot (Bonus Ideas)
* Add a **Stop‑Limit** order function in `orders.py` and expose it via CLI.
* Replace the CLI with a tiny **Streamlit** or **Flask** front‑end.
* Implement richer input prompts (Typer's `prompt` helpers) for an interactive menu.

## License
MIT – feel free to fork, modify, and use as a learning reference.
## Binance Futures Testnet Setup

1. **Register a Testnet Account**
   - Visit the Binance Futures Testnet portal: https://testnet.binancefuture.com (or demo.binance.com)
   - Click **"Register"** and fill in the required information.
   - After registration you will be able to **Log In** to the testnet UI.

2. **Create API Credentials**
   - Once logged in, navigate to **"API Management"** or **"Demo API"**.
   - Click **"Create API"** and give the key a name, e.g., `trading_bot`.
   - **Enable** the **Futures** permission and **Leave** all other permissions unchecked for safety.
   - **Save** the API Key and Secret. Copy them into a safe place.

3. **Configure the Project**
   - In the project root (`trading_bot/`) create a file named `.env`:
     ```
     BINANCE_API_KEY=YOUR_TESTNET_API_KEY
     BINANCE_API_SECRET=YOUR_TESTNET_API_SECRET
     ```
   - The code (`bot/client.py`) automatically reads these variables and performs signed HMAC-SHA256 direct REST requests to the active Binance Futures Demo endpoint (`https://demo-fapi.binance.com`).

4. **Verify Connectivity**
   - After installing dependencies (`pip install -r requirements.txt`) run a quick sanity check:
     ```bash
     python -c "from dotenv import load_dotenv; load_dotenv(); from bot.client import signed_request; print(signed_request('GET', '/fapi/v2/balance'))"
     ```
   - If the credentials are correct, you will see a JSON list of balances.

5. **Start Trading**
   - Use the CLI or Streamlit UI as described in the README to place **MARKET**, **LIMIT**, or **STOP‑LIMIT** orders on the testnet.

> **Note**: The testnet environment is completely isolated from the real Binance exchange – no real funds are at risk.
