from Load_prices import fetch_close_prices, compute_returns
from Signals import generate_momentum_signal, generate_mean_reversion_signal, combine_signals
from Backtest import net_strategy_returns, equity_curve
import numpy as np

def calculate_performance_metrics(net_returns):
    total_return = equity_curve(net_returns).iloc[-1] - 1 # total return over the period
    annualized_return = (1 + total_return) ** (252 / len(net_returns)) - 1 # assuming 252 trading days in a year
    annualized_volatility = net_returns.std() * (252 ** 0.5)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else np.nan
    running_max = equity_curve(net_returns).cummax() # this day's peak-to-date, one value per day
    drawdown_series = (equity_curve(net_returns) - running_max) / running_max # this day's % gap from its own peak
    max_drawdown = drawdown_series.min() # the single worst day across the whole series
    
    return {
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown
    }

if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = compute_returns(Close)
    combined_signal = combine_signals(generate_momentum_signal(Close), generate_mean_reversion_signal(Close))
    net_returns = net_strategy_returns(Returns, combined_signal, cost_per_trade=0.0005)
    performance_metrics = calculate_performance_metrics(net_returns)

    print(f"Total Return: {performance_metrics['Total Return']:.2%}")
    print(f"Annualized Return: {performance_metrics['Annualized Return']:.2%}")
    print(f"Annualized Volatility: {performance_metrics['Annualized Volatility']:.2%}")
    print(f"Sharpe Ratio: {performance_metrics['Sharpe Ratio']:.2f}")
    print(f"Max Drawdown: {performance_metrics['Max Drawdown']:.2%}")