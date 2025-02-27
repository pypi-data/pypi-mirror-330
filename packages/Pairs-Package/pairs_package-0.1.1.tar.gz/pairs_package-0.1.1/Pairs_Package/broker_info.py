from alpaca_trade_api.rest import REST, TimeFrame, Order, Account
import requests
import datetime
import os

# Replace with your Alpaca API credentials
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY","")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET","")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL","")  # Change to live URL if needed

api = REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL)

HEADERS = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET
}

def get_account():
    """Fetch account details (including cash balance, buying power, etc.)."""
    url = f"{ALPACA_BASE_URL}/v2/account"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def get_daily_pnl():
    """Fetch PnL details from Alpaca API."""
    account_info = get_account()
    if account_info:
        return {
            "equity": account_info.get("equity"),
            "last_equity": account_info.get("last_equity"),
            "pnl_today": float(account_info.get("equity", 0)) - float(account_info.get("last_equity", 0))
        }
    return None


def get_historical_pnl(start_date=None, end_date=None, timeframe="1D"):
    """Fetch PnL over a custom period from Alpaca API."""
    
    if start_date is None:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    url = f"{ALPACA_BASE_URL}/v2/account/portfolio/history"
    params = {
        "period": "1M",  # Adjust period if needed (e.g., "1W", "3M", "1Y")
        "timeframe": timeframe
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Error fetching portfolio history: {response.text}")
        return None

    data = response.json()
    if "equity" not in data or not data["equity"]:
        print("No portfolio history found.")
        return None

    # Convert response data into a pandas DataFrame
    history = pd.DataFrame({
        "timestamp": data["timestamp"],
        "equity": data["equity"]
    })

    # Convert timestamps to datetime
    history["date"] = pd.to_datetime(history["timestamp"], unit="s")
    history.set_index("date", inplace=True)

    # Filter data within the date range
    history = history.loc[start_date:end_date]

    if history.empty:
        print("No data available for the given date range.")
        return None

    # Get equity at start and end of the period
    start_equity = history["equity"].iloc[0]
    end_equity = history["equity"].iloc[-1]

    # Calculate PnL
    pnl = end_equity - start_equity
    return {
        "start_equity": start_equity,
        "end_equity": end_equity,
        "pnl": pnl
    }


def get_transactions():
    """Fetch account activities (transactions such as fills, dividends, etc.)."""
    url = f"{ALPACA_BASE_URL}/v2/account/activities"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None


def get_positions():
    """Fetch current portfolio positions."""
    url = f"{ALPACA_BASE_URL}/v2/positions"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

