import yfinance as yf

def fetch_close_prices(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df['Close'].squeeze()

# guard keeps this block from re-running whenever this file is imported elsewhere
if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    Returns = Close.pct_change()
    Returns = Returns.dropna()  # first row has no prior day, so it's NaN
    print(Returns)

    cutoff = int(len(Returns) * 0.7)
    train = Returns.iloc[:cutoff]
    test = Returns.iloc[cutoff:]



