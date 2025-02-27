from Pairs_Package.signals import generate_trading_signals_macd, rolling_betas, beta_neutral_weights, normalize_weights
import statsmodels.api as sm
import os

import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame, Order, Account

# # Replace with your Alpaca API credentials
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY","")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET","")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL","")  # Change to live URL if needed

# Initialize Alpaca API client
api = REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL)

def generate_signals_table(stock1_prices, stock2_prices, residuals, market_returns, zscore_threshold=2):
    """
    Generate a signals table that follows the backtest_pair logic:
      - Uses MACD-based signals derived from residuals.
      - Uses rolling beta estimates to compute beta-neutral weights.
      - Assigns positions as:
            * For a long residual signal: long stock1 and short stock2.
            * For a short residual signal: short stock1 and long stock2.
      - Forces positions to zero when exit signals are active.
      - Shifts the signals to avoid lookahead bias.
    
    Parameters:
      stock1_prices, stock2_prices: pd.Series with .name attributes set to the respective symbols.
      residuals: pd.Series from the OLS regression residuals.
      market_returns: DataFrame (or Series) of benchmark returns (with a 'SPY' column for rolling beta).
      zscore_threshold: Parameter passed to generate_trading_signals_macd (used here as the MACD threshold).
    
    Returns:
      signals_table: pd.DataFrame containing beta-weighted positions for each stock.
    """
    # Generate MACD-based signals
    long_signals, short_signals, exit_signals = generate_trading_signals_macd(residuals, threshold=zscore_threshold)
    
    # Create boolean DataFrames for trade entries
    long_entries = pd.DataFrame(False, index=stock1_prices.index, columns=[stock1_prices.name, stock2_prices.name])
    short_entries = pd.DataFrame(False, index=stock1_prices.index, columns=[stock1_prices.name, stock2_prices.name])
    
    # Combine signals into a single DataFrame for clarity
    long_short_pair = pd.concat([long_signals, short_signals], axis=1)
    long_short_pair.columns = ["Long", "Short"]
    
    # Signal assignment:
    # - When the residual is “short” (i.e. short_signals True): 
    #       • Long the second stock and short the first.
    # - When the residual is “long” (i.e. long_signals True):
    #       • Long the first stock and short the second.
    long_entries.loc[long_short_pair['Short'], stock2_prices.name] = True
    short_entries.loc[long_short_pair['Short'], stock1_prices.name] = True
    long_entries.loc[long_short_pair['Long'], stock1_prices.name] = True
    short_entries.loc[long_short_pair['Long'], stock2_prices.name] = True

    # Compute rolling betas from percentage returns
    stock1_returns = stock1_prices.pct_change().dropna()
    stock2_returns = stock2_prices.pct_change().dropna()
    rolling_beta_1, rolling_beta_2 = rolling_betas(stock1_returns, stock2_returns, market_returns)
    
    # Compute beta-neutral weights (assumes rolling_beta_* have a column 'SPY')
    common_index = rolling_beta_1.dropna().index
    weights = []
    for ts in common_index:
        beta1 = rolling_beta_1.loc[ts, 'SPY']
        beta2 = rolling_beta_2.loc[ts, 'SPY']
        w1_n, w2_n = beta_neutral_weights(beta1, beta2)
        w1, w2 = normalize_weights(w1_n, w2_n)
        weights.append((w1, w2))
    weights_df = pd.DataFrame(weights, index=common_index, columns=[stock1_prices.name, stock2_prices.name])
    
    # Assign positions according to the signals:
    # For a "long" residual signal: long stock1 and short stock2.
    weights_df.loc[long_signals, stock1_prices.name] = weights_df.loc[long_signals, stock1_prices.name]
    weights_df.loc[long_signals, stock2_prices.name] = -weights_df.loc[long_signals, stock2_prices.name]
    # For a "short" residual signal: short stock1 and long stock2.
    weights_df.loc[short_signals, stock1_prices.name] = -weights_df.loc[short_signals, stock1_prices.name]
    weights_df.loc[short_signals, stock2_prices.name] = weights_df.loc[short_signals, stock2_prices.name]
    
    # Zero out positions when exit signals are active (i.e. when exit_signals is False)
    weights_df.loc[~exit_signals, [stock1_prices.name, stock2_prices.name]] = 0
    
    # Reindex to match the full price series and drop any missing values; then shift to avoid lookahead bias.
    weights_df = weights_df.reindex(stock1_prices.index, method='nearest').dropna()
    signals_table = weights_df.shift(1)
    
    # Optionally, attach the raw signal flags (shifted) to the table
    signals_table['Long'] = long_signals.shift(1)
    signals_table['Short'] = short_signals.shift(1)
    signals_table['Exit'] = exit_signals.shift(1)
    
    return signals_table

## Now we want to actually interact with the API to place our orders etc.

#First we want to get the actual value of the portfolio of the two pairs.
def get_account_info():
    account = api.get_account()
    return float(account.equity)  # Returns current account equity

#Next, we create a function to ajust position of the current stock pairs that we have that we have 
def adjust_position(symbol, target_allocation):
    """
    Adjusts the position in a symbol to match the target dollar allocation.
    Uses recent bar data (previous close) to compute how many shares to trade.
    """
    try:
        bars = api.get_bars(symbol, TimeFrame.Day, limit=5).df
        if bars.empty:
            print(f"Skipping {symbol}: no price data available.")
            return

        previous_close = bars.iloc[-1].close
        target_shares = int(target_allocation // previous_close)
        
        try:
            position = api.get_position(symbol)
            current_shares = int(float(position.qty))
        except Exception:
            current_shares = 0

        share_diff = target_shares - current_shares
        if share_diff > 0:
            api.submit_order(
                symbol=symbol,
                qty=share_diff,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
            print(f"BUY {share_diff} shares of {symbol} (target: {target_shares}).")
        elif share_diff < 0:
            api.submit_order(
                symbol=symbol,
                qty=abs(share_diff),
                side="sell",
                type="market",
                time_in_force="gtc"
            )
            print(f"SELL {abs(share_diff)} shares of {symbol} (target: {target_shares}).")
        else:
            print(f"{symbol} is already at the target allocation ({target_shares} shares).")
    except Exception as e:
        print(f"Error adjusting position for {symbol}: {e}")

## Next we need an actual way to place orders to Alpaca:
def place_orders(df_orders):
    """
    Expects a DataFrame with columns "Symbol" and "Dollar Allocation".
    Iterates over each row to adjust the position.
    """
    for _, row in df_orders.iterrows():
        adjust_position(row["Symbol"], row["Dollar Allocation"])

## As well as a way to close positions
def close_positions(new_portfolio_df):
    """
    Closes any open positions for symbols that are not in the new portfolio.
    """
    try:
        positions = api.list_positions()
        new_symbols = set(new_portfolio_df["Symbol"])
        for position in positions:
            if position.symbol not in new_symbols:
                qty = abs(int(float(position.qty)))
                side = "sell" if position.side == "long" else "buy"
                api.submit_order(
                    symbol=position.symbol,
                    qty=qty,
                    side=side,
                    type="market",
                    time_in_force="gtc"
                )
                print(f"Closing position for {position.symbol}: {side.upper()} {qty} shares.")
        print("Closed positions not in the new portfolio.")
    except Exception as e:
        print(f"Error closing positions: {e}")

def fetch_data(symbol, start_date, end_date):
    """Fetch historical market data from Alpaca."""
    try:
        bars = api.get_bars(symbol, TimeFrame.Day, start=start_date, end=end_date).df
        bars.index = pd.to_datetime(bars.index)  # Ensure datetime format
        return bars
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def send_daily_pair_trade(stock1_ticker, stock2_ticker, benchmark_ticker, start_date, end_date, allocation_multiplier=1.0):
    """
    Generates beta‑weighted pair trade signals using our custom generate_signals_table function,
    then sends orders via Alpaca based on the most recent signal.
    This function is designed to be run on a daily schedule.
    
    Parameters:
      stock1_prices, stock2_prices: pd.Series with price data (their .name attribute should be set to the ticker).
      residuals: pd.Series of regression residuals.
      market_returns: Benchmark returns with a 'SPY' column for rolling beta calculation.
      allocation_multiplier: Fraction of total equity to allocate.
    """

    stock1_bars = fetch_data(stock1_ticker, start_date, end_date)
    stock2_bars = fetch_data(stock2_ticker, start_date, end_date)
    benchmark_bars = fetch_data(benchmark_ticker, start_date, end_date)

    stock1_prices = stock1_bars["close"].copy()
    stock2_prices = stock2_bars["close"].copy()
    stock1_prices.name = stock1_ticker
    stock2_prices.name = stock2_ticker

    # We compute regression residuals (OLS of stock1 on stock2)
    stock2_const = sm.add_constant(stock2_prices)
    model = sm.OLS(stock1_prices, stock2_const)
    results = model.fit()
    residuals = results.resid

    benchmark_prices = benchmark_bars["close"]
    benchmark_returns = benchmark_prices.pct_change().dropna().to_frame(name="SPY")

    # We generate beta‑weighted signals table using the custom function
    signals_table = generate_signals_table(stock1_prices, stock2_prices, residuals, benchmark_returns)
    latest_signal = signals_table.iloc[-1]

    equity = get_account_info()

    target_allocation_stock1 = allocation_multiplier * equity * latest_signal[stock1_ticker]
    target_allocation_stock2 = allocation_multiplier * equity * latest_signal[stock2_ticker]
    
    df_orders = pd.DataFrame({
        "Symbol": [stock1_ticker, stock2_ticker],
        "Dollar Allocation": [target_allocation_stock1, target_allocation_stock2]
    })
    
    print("Placing orders based on latest daily signals:")
    print(df_orders)
    
    place_orders(df_orders)
    close_positions(df_orders)



send_daily_pair_trade(
    stock1_ticker="MMM",
    stock2_ticker="HWM",
    benchmark_ticker="SPY",
    start_date="2023-01-01",
    end_date="2023-12-31",
    allocation_multiplier=1.0
)

