from Load_prices import fetch_close_prices
import numpy as np

def generate_signals(Close, fast_window=20, slow_window=100):
    fast_ma = Close.rolling(fast_window).mean()
    slow_ma = Close.rolling(slow_window).mean()
    signal = np.where(fast_ma > slow_ma, 1, np.where(slow_ma.isna(), np.nan, -1))
    return signal

if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    signals = generate_signals(Close)
    print(signals)