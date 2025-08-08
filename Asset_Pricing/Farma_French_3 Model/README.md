# Fama-French 3-Factor — Minimal Template

**What this is:** a clean, GitHub-ready FF3 script you can run or adapt for your own repo.

## Quick Start

```bash
pip install -r requirements.txt
python ff3_simple.py --ticker AAPL --start 2020-01-01 --end 2025-08-01
```

Outputs go to `output/`:
- `ff3_summary_<TICKER>.csv` — tidy table with alpha (daily + annualized), betas, t-stats, p-values, R², N
- `ff3_merged_<TICKER>.csv` — the aligned dataset used for the regression

## Local CSV Fallback (if you're offline)

If downloads fail, put files in `data/`:

- `asset_prices.csv` with columns: `Date, Adj Close`
- `ff_factors.csv` with columns: `Date, Mkt-RF, SMB, HML, RF` (decimals preferred; if in %, adjust to /100)

Dates should be YYYY-MM-DD.

## Why this template?

- Simple: one script, clear functions, no notebook sprawl
- Robust: tries to download; gracefully falls back to local CSVs
- Sound: Newey–West (HAC) standard errors by default

## Notes

- Factors are daily from the Ken French library via `pandas-datareader`.
- Asset prices are daily adjusted close from `yfinance`.
- Daily alpha is annualized using geometric compounding (≈252 trading days).
