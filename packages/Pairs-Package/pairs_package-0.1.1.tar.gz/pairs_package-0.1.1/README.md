# **Pairs_Package**

**alpaca-pairs-pkg** is a Python package designed for executing pairs trading strategies using Alpaca Markets API. It allows users to monitor account performance, track profit and loss (PnL), and execute trades based on statistical arbitrage strategies.

## **Features**

- **Pairs Trading Execution**: Automates long/short trades for selected stock pairs.
- **Account Info Retrieval**: Fetches account balance and equity from Alpaca.
- **Trade Execution**: Places market orders based on trading signals.
- **Order Management**: Retrieves past and active orders.
- **Portfolio Monitoring**: Checks positions and transaction history.
- **PnL Tracking**: Monitors daily and historical profit and loss (PnL).

---

## **Installation**

Before using the package, install the required dependencies:

```bash
pip install -r requirements.txt
```

Clone the repository (if applicable):

```bash
pip install Pairs_Package
```

---

## **Usage**

### **1. Import the necessary functions**

```python
from Pairs_Package.trade import send_daily_pair_trade
from Pairs_Package.broker_info import get_account, get_daily_pnl, get_historical_pnl, get_transactions, get_positions
```

### **2. Fetch Account Info**

Retrieve your account’s total portfolio value from Alpaca:

```python
account_info = get_account()
```

### **3. Fetch Orders**

Retrieve all past and active orders:

```python
orders = get_orders()
```

### **4. Fetch Portfolio Positions**

Retrieve all active positions in the portfolio:

```python
positions = get_positions()
```

### **5. Fetch Transactions**

Retrieve past transaction history (e.g., fills, dividends, etc.):

```python
transactions = get_transactions()
```

### **6. Track PnL**

#### **Daily PnL**

```python
daily_pnl = get_daily_pnl()
```

#### **7. Historical PnL**

Fetch profit and loss over a custom period:

```python
historical_pnl = get_historical_pnl()  # default: last 7 days
historical_pnl = get_historical_pnl(start_date='2023-01-01', end_date='2023-12-31', timeframe='1D')
```

#### **8. Execute Pairs Trading**

Run the daily trading strategy for pairs trading:

```python
send_daily_pair_trade()
```

## Output

```python
Placing orders based on latest daily signals:
  Symbol  Dollar Allocation
0    MMM       52076.211751
1    HWM       48331.488249
MMM is already at the target allocation (348 shares).
HWM is already at the target allocation (379 shares).
Closed positions not in the new portfolio.
```

## **Configuration**

This package requires Alpaca API credentials. Set them as environment variables:

```python
ALPACA_API_KEY = "your_api_key"
ALPACA_API_SECRET = "your_api_secret"
BASE_URL = "https://paper-api.alpaca.markets"  # Use live URL for real trading
```

## **Dependencies**

- `alpaca-trade-api`
- `pandas`
- `numpy`
- `yfinance`
- `setuptools`
