# Monte Carlo Call Option Pricer & Entry Helper

This project implements a **Monte Carlo simulation** for pricing European call options and assisting with trade entry decisions.

It:
- Fetches the latest stock close price as the starting underlying price (S₀) via `yfinance`.
- Estimates annualized volatility from historical log returns (or uses a supplied implied volatility).
- Prices the option under **risk-neutral Geometric Brownian Motion**.
- Computes:
  - Probability of finishing **in the money** (ITM)
  - Probability of making a profit given the premium
  - Expected value (discounted payoff − premium)
  - Decision signal: **ENTER**, **MAYBE**, or **SKIP** based on edge vs premium
- Plots the simulated terminal price distribution.

> **Disclaimer:** This is an educational tool. It does not constitute financial advice. Real-world options involve factors not modeled here (IV skew, jumps, early exercise for American options, transaction costs, etc.).

---

## Features

- **Colab-friendly**: Runs directly in Google Colab without argument parsing.
- **Historical Volatility Estimation**: Uses up to 3 years (configurable) of historical daily returns.
- **Customizable**: Override starting price (S₀) and volatility (`sigma`) for what-if analysis.
- **Visual Output**: Histogram of simulated terminal prices with strike line.

---

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/monte-carlo-option-pricer.git
cd monte-carlo-option-pricer
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Google Colab
- Open [Google Colab](https://colab.research.google.com/).
- Copy and paste the contents of `monte_carlo_option_pricer_colab.py` into a cell.
- Run the cell to load functions.
- Use the helper:
```python
_ = run_monte_carlo("AAPL", strike=220, premium=4.10, T=0.5, sims=100_000, seed=1)
```

### 2. Local Python Script
If you adapt the code for CLI usage:
```bash
python monte_carlo_option_pricer.py --ticker NVDA --strike 130 --premium 8.50 --T 0.5
```

---

## Example Output
Example for **NVDA**, strike 130, premium $8.50, 6 months to expiry:

| Metric | Value |
|--------|-------|
| MC Call Price | $9.12 |
| Prob(ITM) | 65.3% |
| Expected Value | $0.62 |
| Decision | ENTER |

---

## Parameters

| Parameter        | Description |
|------------------|-------------|
| `ticker`         | Stock symbol (string) |
| `strike`         | Option strike price (float) |
| `premium`        | Option price you would pay (float) |
| `T`              | Time to expiry in years (float) |
| `r`              | Risk-free interest rate (decimal) |
| `sims`           | Number of Monte Carlo simulations |
| `steps`          | Time steps per path |
| `lookback_years` | Years of history for volatility estimation |
| `S0`             | Override for starting price |
| `sigma`          | Override for volatility (e.g., IV) |
| `seed`           | Random seed for reproducibility |
| `plot`           | Whether to plot terminal distribution |

---

## Requirements
See `requirements.txt` for dependencies.

---

## License
MIT License
