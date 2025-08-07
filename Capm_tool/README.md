# Capital Asset Pricing Model (CAPM) Tool

This Python script downloads stock and market data from Yahoo Finance, estimates CAPM parameters, and plots the Security Market Line.

## Features
- User inputs ticker and date range
- Downloads asset + S&P 500 prices
- Uses fixed annual risk-free rate (editable in code)
- Calculates Beta, Alpha, R², CAPM expected return, and Jensen's Alpha
- Plots the Security Market Line (SML)

## How to Run
```bash
pip install -r requirements.txt
python capm_tool.py

