import yfinance as yf

def fetch_close_prices(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df['Close'].squeeze()

def compute_returns(prices):
    returns = prices.pct_change().dropna()
    return returns

# guard keeps this block from re-running whenever this file is imported elsewhere
if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = compute_returns(Close)
    print(Returns)

    # train-test split
    cutoff = int(len(Returns) * 0.7)
    train = Returns.iloc[:cutoff]
    test = Returns.iloc[cutoff:]



