from Load_prices import fetch_close_prices, compute_returns
from Signals import generate_momentum_signal, generate_mean_reversion_signal, combine_signals_by_regime
from Backtest import net_strategy_returns
from Regimes import identify_regimes, classify_regimes
from Performance import calculate_performance_metrics, print_metrics

def generate_walk_forward_windows(index, train_size=504, test_size=126):
    # Yields (train dates, test dates) pairs, rolling forward by one test window each time so every test day appears exactly once
    start = 0
    while start + train_size < len(index): # stop once no test days are left after the train window; the final test slice may be shorter than test_size
        train_indices = index[start:start + train_size]
        test_indices = index[start + train_size:start + train_size + test_size]
        yield train_indices, test_indices
        start += test_size

def run_strategy(Close, Returns, regimes, fast_window, slow_window, z_threshold):
    # returns the net returns series for this one parameter combination
    momentum_signal = generate_momentum_signal(Close, fast_window, slow_window)
    mean_reversion_signal = generate_mean_reversion_signal(Close, threshold=z_threshold)
    combined_signal = combine_signals_by_regime(momentum_signal, mean_reversion_signal, regimes)
    net_returns = net_strategy_returns(Returns, combined_signal)

    return net_returns

if __name__ == "__main__":
    # sanity check: prints each window's dates so you can confirm there are no gaps/overlaps and the last test window reaches the end of the data
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = compute_returns(Close)

    windows = list(generate_walk_forward_windows(Returns.index))
    print("Number of windows:", len(windows))

    for i, (train_idx, test_idx) in enumerate(windows, start=1):
        print(f"Window {i}: train {train_idx[0].date()} to {train_idx[-1].date()} ({len(train_idx)} days), "
              f"test {test_idx[0].date()} to {test_idx[-1].date()} ({len(test_idx)} days)")

    # check run_strategy reproduces Performance.py with the default parameters - should give 0.87% total return
    regimes = classify_regimes(identify_regimes(Close))
    net_returns = run_strategy(Close, Returns, regimes, fast_window=20, slow_window=100, z_threshold=1.5)
    performance_metrics = calculate_performance_metrics(net_returns)
    print_metrics(performance_metrics)