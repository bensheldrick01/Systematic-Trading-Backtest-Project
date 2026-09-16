# Fetches historical price data and computes daily returns with a chronological train/test split.
import yfinance as yf

def fetch_close_prices(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df['Close'].squeeze()

def compute_returns(prices):
    returns = prices.pct_change().dropna()
    return returns

def train_test_split(returns, train_fraction=0.7):
    cutoff = int(len(returns) * train_fraction)
    return returns.iloc[:cutoff], returns.iloc[cutoff:]

# guard keeps this block from re-running whenever this file is imported elsewhere
if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = compute_returns(Close)
    print(Returns)

    train_returns, test_returns = train_test_split(Returns, train_fraction=0.7)




