from Pairs_Package.data import calculate_macd

def generate_trading_signals_macd(residuals, threshold=0):
    """
    Generate trading signals based on MACD crossovers.
      - When MACD crosses above its signal line: long signal.
      - When MACD crosses below its signal line: short signal.
      - Exit signal is defined when the MACD and signal line are very close.
    """
    macd_line, signal_line, _ = calculate_macd(residuals)
    long_signals = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
    short_signals = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))
    exit_signals = (macd_line - signal_line).abs() < threshold
    return long_signals, short_signals, exit_signals

def rolling_betas(stock1_returns, stock2_returns, market_returns, window=60):
    """
    Calculate rolling beta estimates.  
    Assumes market_returns is a pd.Series or DataFrame with a column 'SPY'.
    """
    rolling_beta_1 = stock1_returns.rolling(window=window).cov(market_returns) / market_returns.rolling(window=window).var()
    rolling_beta_2 = stock2_returns.rolling(window=window).cov(market_returns) / market_returns.rolling(window=window).var()
    return rolling_beta_1, rolling_beta_2

def beta_neutral_weights(beta_1, beta_2):
    """
    Calculate beta-neutral weights for the pair.
    For example, if going long stock1 and short stock2, one possible formulation is:
      w1 = -beta_2 / (beta_1 - beta_2)    and    w2 = 1 - w1
    """
    w_1 = -beta_2 / (beta_1 - beta_2)
    w_2 = 1 - w_1
    return w_1, w_2

def normalize_weights(w_1, w_2):
    """Normalize weights so that the total absolute weight sums to 1."""
    total = abs(w_1) + abs(w_2)
    if total == 0:
        return 0, 0
    return w_1 / total, w_2 / total