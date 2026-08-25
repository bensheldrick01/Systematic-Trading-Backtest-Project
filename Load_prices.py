import yfinance as yf

def fetch_close_prices(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    return df['Close'].squeeze()

Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
Returns = Close.pct_change()
Returns = Returns.dropna()
print(Returns)

cutoff = int(len(Returns) * 0.7)
train = Returns.iloc[:cutoff]
test = Returns.iloc[cutoff:]


