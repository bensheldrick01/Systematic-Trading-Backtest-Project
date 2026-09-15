from Load_prices import fetch_close_prices
import numpy as np
import pandas as pd

def identify_regimes(Close, window=200):
    long_term_ma = Close.rolling(window).mean()
    distance_from_ma = (Close - long_term_ma) / long_term_ma
    return distance_from_ma

def explore_distance_from_ma_thresholds(distance_from_ma):
    thresholds = [0.03, 0.05, 0.08,0.10]
    results = {}
    
    for threshold in thresholds:
        # .dropna() here is required, not optional - without it, warmup NaN rows get
        # miscounted into "Within Threshold" via the raw len() below.
        above_threshold = (distance_from_ma.dropna() > threshold).sum()
        below_threshold = (distance_from_ma.dropna() < -threshold).sum()
        within_threshold = len(distance_from_ma.dropna()) - above_threshold - below_threshold
        results[float(threshold)] = {
            "Above Threshold": above_threshold,
            "Below Threshold": below_threshold,
            "Within Threshold": within_threshold
        }
    return results # 0.05 seems to be a good balance between regime frequency and strength

def classify_regimes(distance_from_ma, threshold=0.05):
    # isna() checked first so warmup days get an explicit "unknown" label,
    # rather than silently defaulting into "Neutral" 
    regime = np.where(distance_from_ma.isna(), "unknown", np.where(distance_from_ma > threshold, "Bullish", np.where(distance_from_ma < -threshold, "Bearish", "Neutral")))
    return pd.Series(regime, index=distance_from_ma.index)

if __name__ == "__main__":
    Close = fetch_close_prices("^GSPC", start="2018-01-01", end="2023-01-01")
    distance_from_ma = identify_regimes(Close)
    print("Distance from long-term moving average:", distance_from_ma)
    print(distance_from_ma.describe())

    regime_thresholds = explore_distance_from_ma_thresholds(distance_from_ma)
    print("\n Regime Thresholds:", regime_thresholds)
 