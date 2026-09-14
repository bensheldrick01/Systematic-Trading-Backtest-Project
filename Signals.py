# Generates momentum and mean-reversion trading signals and combines them into one blended signal.
from Load_prices import fetch_close_prices
import numpy as np
import pandas as pd

def generate_momentum_signal(Close, fast_window=20, slow_window=100):
    fast_ma = Close.rolling(fast_window).mean()
    slow_ma = Close.rolling(slow_window).mean()
    signal = np.where(fast_ma > slow_ma, 1, np.where(slow_ma.isna(), np.nan, -1))
    return pd.Series(signal, index=Close.index) # returns a pandas Series with the same dated index as Close

# Diagnostic function to pick the threshold used in the mean reversion function - above the threshold is the 
# number of standard deviations away from the mean that we consider to be a significant deviation
def explore_zscore_thresholds(Close, window=20):
    z_scores = (Close - Close.rolling(window).mean()) / Close.rolling(window).std()
    thresholds = np.arange(0.5, 3.5, 0.5)
    results = {}
    
    for threshold in thresholds:
        signal = np.where(z_scores > threshold, -1, np.where(z_scores < -threshold, 1, 0))
        results[float(threshold)] = round(float((signal != 0).sum() / len(signal)) * 100, 2)  # percentage of non-zero signals for each threshold, 1.5 seems to be a good balance between signal frequency and strength
    return results

def generate_mean_reversion_signal(Close, window=20, threshold=1.5):
    z_score = (Close - Close.rolling(window).mean()) / Close.rolling(window).std()
    signal = np.where(z_score > threshold, -1, np.where(z_score < -threshold, 1, 0))
    return pd.Series(signal, index=Close.index)

def explore_combined_signal_thresholds(momentum_signal, mean_reversion_signal):
    blend = 0.6 * momentum_signal + 0.4 * mean_reversion_signal
    thresholds = sorted(blend.dropna().unique())
    print("\n Combined Signal Thresholds:", [round(float(th), 2) for th in thresholds]) # 0.2 is the natural cutoff - it separates the two cases where the signals actively disagree (+-0.2) from where they agree or one is neutral (+-0.6, +-1.0)

    for t in thresholds:
        long_signals = (blend > t).sum()
        short_signals = (blend < -t).sum()
        flat_signals = len(blend) - long_signals - short_signals
        print(f"Threshold: {round(float(t), 2)}, Long Signals: {long_signals}, Short Signals: {short_signals}, Flat Signals: {flat_signals}")

def combine_signals(momentum_signal, mean_reversion_signal, threshold=0.2):
    # continuous blend - not yet a clean {-1, 0, +1} signal
    blend = 0.6 * momentum_signal + 0.4 * mean_reversion_signal
    # discretise: only count it as long/short if the blend clears the threshold either way
    combined_signal = np.where(blend > threshold, 1, np.where(blend < -threshold, -1, 0))
    return pd.Series(combined_signal, index=momentum_signal.index)

if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")

    momentum_signal = generate_momentum_signal(Close)
    zscore_thresholds = explore_zscore_thresholds(Close)
    mean_reversion_signal = generate_mean_reversion_signal(Close)
    combined_signal = combine_signals(momentum_signal, mean_reversion_signal)

    print("Momentum Signal:",momentum_signal)
    print("\n zscore_thresholds:", zscore_thresholds)
    print("\n Mean Reversion Signal:", mean_reversion_signal)
    explore_combined_signal_thresholds(momentum_signal, mean_reversion_signal)
    print("\n Combined Signal:", combined_signal)