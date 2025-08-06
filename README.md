# Financial Risk Assessment Engine

A minimal tool to compute basic market risk metrics for portfolios of equities or other instruments. It reads historical price series, computes log returns, estimates volatility, and calculates Value at Risk (VaR) at a chosen confidence level. Results are exported to a CSV for further analysis or reporting.

## Features

- Read price data (Date, Ticker, Close) from CSV.
- Calculate daily log returns per ticker.
- Compute annualised volatility.
- Compute historical VaR at 95% confidence.
- Output a concise risk report CSV with metrics per ticker.
