"""
Fama-French 3-Factor (FF3) Model — Minimal Template
---------------------------------------------------
A compact, well-documented script you can drop into GitHub.

Features
- Pulls daily asset prices (yfinance) and FF3 factors (pandas-datareader)
- Computes excess returns and runs FF3 regression with Newey–West (HAC) errors
- Prints tidy summary and saves a small report to CSV
- Falls back to local CSVs if network is unavailable

Usage
-----
python ff3_simple.py --ticker AAPL --start 2020-01-01 --end 2025-08-01

Local CSV fallback (optional)
-----------------------------
If data downloads fail, you can supply:
- data/asset_prices.csv with columns: Date, Adj Close
- data/ff_factors.csv with columns: Date, Mkt-RF, SMB, HML, RF
(Dates in YYYY-MM-DD)
"""

import argparse
import sys
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore", category=FutureWarning)

# ----------------------------
# Helpers
# ----------------------------

def _to_datetime_index(df, date_col="Date"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()
    return df

def load_prices_yf(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download Adj Close prices using yfinance. Return DataFrame with 'Adj Close'."""
    try:
        import yfinance as yf
        px = yf.download(ticker, start=start, end=end, progress=False)
        if "Adj Close" not in px:
            raise ValueError("Adj Close not found in downloaded data")
        return px[["Adj Close"]].dropna()
    except Exception as e:
        print(f"[warn] yfinance failed ({e}). Falling back to local CSV: data/asset_prices.csv")
        csv_path = Path("data/asset_prices.csv")
        if not csv_path.exists():
            raise FileNotFoundError("data/asset_prices.csv not found and yfinance failed.")
        df = pd.read_csv(csv_path)
        return _to_datetime_index(df, "Date")[["Adj Close"]].dropna()

def load_ff3_factors(start: str, end: str) -> pd.DataFrame:
    """Download FF3 daily factors using pandas-datareader; fallback to local CSV."""
    try:
        from pandas_datareader import data as web
        ff = web.DataReader("F-F_Research_Data_Factors_Daily", "famafrench")[0]
        ff.index = pd.to_datetime(ff.index)
        ff = ff.loc[(ff.index >= pd.to_datetime(start)) & (ff.index <= pd.to_datetime(end))]
        # Convert from percentages to decimals
        return ff.rename(columns={"Mkt-RF": "MKT_RF"})\
                 .rename(columns=str.strip)\
                 .rename_axis("Date")\
                 .rename(columns={"SMB":"SMB", "HML":"HML", "RF":"RF"})/100.0
    except Exception as e:
        print(f"[warn] pandas-datareader failed ({e}). Falling back to local CSV: data/ff_factors.csv")
        csv_path = Path("data/ff_factors.csv")
        if not csv_path.exists():
            raise FileNotFoundError("data/ff_factors.csv not found and famafrench download failed.")
        ff = pd.read_csv(csv_path)
        ff = _to_datetime_index(ff, "Date")
        # assume already in decimals; if in % switch to /100
        return ff[["Mkt-RF","SMB","HML","RF"]]\
                 .rename(columns={"Mkt-RF":"MKT_RF"})

def compute_daily_returns(prices: pd.Series) -> pd.Series:
    """Compute simple daily returns from Adj Close prices."""
    r = prices.pct_change().dropna()
    r.name = "asset_ret"
    return r

def run_ff3_regression(asset_excess: pd.Series, factors: pd.DataFrame):
    """Run OLS with Newey-West (lag=5) HAC errors: asset_excess ~ alpha + MKT_RF + SMB + HML"""
    df = pd.concat([asset_excess, factors[["MKT_RF","SMB","HML"]]], axis=1, join="inner").dropna()
    y = df["asset_ret"] - df["RF"] if "RF" in df else df["asset_ret"]
    X = sm.add_constant(df[["MKT_RF","SMB","HML"]])
    ols = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags":5})
    return ols, df

def annualize_alpha(alpha_daily: float, trading_days: int = 252) -> float:
    """Convert daily alpha to annualized (approx compounding)."""
    return (1 + alpha_daily) ** trading_days - 1

def summarize_results(model, trading_days: int = 252) -> pd.DataFrame:
    """Return a tidy one-row summary with coefficients and stats."""
    coefs = model.params.to_dict()
    tvals = model.tvalues.to_dict()
    pvals = model.pvalues.to_dict()

    alpha_ann = annualize_alpha(coefs.get("const", 0.0), trading_days)
    out = {
        "alpha_daily": coefs.get("const", np.nan),
        "alpha_annualized": alpha_ann,
        "beta_mkt": coefs.get("MKT_RF", np.nan),
        "beta_smb": coefs.get("SMB", np.nan),
        "beta_hml": coefs.get("HML", np.nan),
        "t_alpha": tvals.get("const", np.nan),
        "t_mkt": tvals.get("MKT_RF", np.nan),
        "t_smb": tvals.get("SMB", np.nan),
        "t_hml": tvals.get("HML", np.nan),
        "p_alpha": pvals.get("const", np.nan),
        "p_mkt": pvals.get("MKT_RF", np.nan),
        "p_smb": pvals.get("SMB", np.nan),
        "p_hml": pvals.get("HML", np.nan),
        "r2": model.rsquared,
        "n_obs": int(model.nobs),
    }
    return pd.DataFrame([out])

def main(args):
    prices = load_prices_yf(args.ticker, args.start, args.end)
    asset_ret = compute_daily_returns(prices["Adj Close"])

    ff = load_ff3_factors(args.start, args.end)
    # ensure RF exists and aligned
    if "RF" not in ff.columns:
        raise ValueError("Risk-free rate (RF) missing in factor data.")
    merged = pd.concat([asset_ret, ff], axis=1, join="inner").dropna()

    model, used_df = run_ff3_regression(merged["asset_ret"], merged)

    summary_df = summarize_results(model)
    print("\n=== Fama-French 3-Factor Results ===")
    print(summary_df.to_string(index=False, float_format=lambda x: f"{x:0.6f}"))

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True, parents=True)
    summary_path = out_dir / f"ff3_summary_{args.ticker}.csv"
    merged_path  = out_dir / f"ff3_merged_{args.ticker}.csv"

    summary_df.to_csv(summary_path, index=False)
    used_df.to_csv(merged_path)

    print(f"\nSaved summary  -> {summary_path}")
    print(f"Saved dataset  -> {merged_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Fama-French 3-Factor model (minimal GitHub-ready template)")
    p.add_argument("--ticker", type=str, default="AAPL")
    p.add_argument("--start", type=str, default="2020-01-01")
    p.add_argument("--end",   type=str, default="2025-08-01")
    args = p.parse_args()
    sys.exit(main(args))
