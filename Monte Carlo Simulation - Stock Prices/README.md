# Monte Carlo Stock Price Simulation

This repository contains a Python implementation of a **Monte Carlo Simulation** for forecasting stock prices using historical data and Geometric Brownian Motion (GBM).  

The script downloads stock data from **Yahoo Finance**, calculates historical returns, and simulates multiple possible future price paths. It also estimates the probability distribution of the stock price at a chosen future date.

---

## **Features**
- Downloads historical stock data using `yfinance`
- Calculates daily returns, mean return, and volatility
- Runs a **Random Walk simulation** based on GBM assumptions
- Plots multiple simulated price paths
- Computes and visualizes the **probability distribution** of final stock prices
- Calculates **Value at Risk (VaR)** at a chosen confidence level

---

## **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/montecarlo-stock-simulation.git
   cd montecarlo-stock-simulation
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**
1. Open the script `montecarlo_stock_prices.py`.
2. Edit the following variables:
   - **Start and end dates** for historical data
   - **Ticker symbol** (e.g., `'NVDA'`, `'AAPL'`, `'GOOG'`)
   - **Start price date** for your simulation
3. Run the script:
   ```bash
   python montecarlo_stock_prices.py
   ```

---

## **Example Output**
- **Line chart** showing multiple simulated stock price paths
- **Histogram** showing the final simulated price distribution
- **Value at Risk (VaR)** calculation for a given confidence interval

---

## **Mathematical Model**
The simulation assumes stock prices follow a **Geometric Brownian Motion**:

\[
\frac{\Delta P}{P} = \mu \Delta t + \sigma \tilde{\epsilon} \Delta t
\]
\[
P_{t+1} = P_t \times (1+\tilde{\epsilon})
\]
Where:
- \( \mu \) = mean daily return
- \( \sigma \) = standard deviation of returns
- \( \tilde{\epsilon} \) = random shock ~ N(μ, σ²)

---

## **Requirements**
See [requirements.txt](requirements.txt) for the complete list of dependencies.

---

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Author**
- [Your Name](https://github.com/yourusername)
