from Load_prices import fetch_close_prices, compute_returns
from Signals import generate_momentum_signal, generate_mean_reversion_signal, combine_signals
import pandas as pd

def backtest_strategy_returns(Returns, combined_signal):
    strategy_returns = combined_signal.shift(1) * Returns  # shift the signal by one day to avoid lookahead bias
    return strategy_returns

def transaction_costs(combined_signal, cost_per_trade=0.0005):
    trades = combined_signal.shift(1).diff().abs()  # count the number of trades (changes in signal), shifted to match the returns
    costs = trades * cost_per_trade
    return costs

def net_strategy_returns(Returns, combined_signal, cost_per_trade=0.0005): # ignores compounding - just for comparison
    strategy_returns = backtest_strategy_returns(Returns, combined_signal)
    costs = transaction_costs(combined_signal, cost_per_trade)
    net_returns = strategy_returns - costs
    return net_returns

def equity_curve(net_returns): # correctly accounts for compounding
    equity_curve = (1 + net_returns).cumprod()
    return equity_curve

if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = compute_returns(Close)
    combined_signal = combine_signals(generate_momentum_signal(Close), generate_mean_reversion_signal(Close))
    
    print("Total strategy returns:", backtest_strategy_returns(Returns, combined_signal).sum())
    print("Total transaction costs:", transaction_costs(combined_signal).sum())
    print("Total net strategy returns:", net_strategy_returns(Returns, combined_signal).sum()) # ignores compounding - kept just for comparison with below
    print("Equity Curve:", equity_curve(net_strategy_returns(Returns, combined_signal))) # cumulative product of net returns over time, showing the true growth of $1 invested in the strategy (in this case it's an 8% loss)
