"""
Financial Risk Assessment Engine
===============================

This script calculates basic market risk metrics for a portfolio of
securities.  It reads historical price data, computes daily returns,
estimates volatility and Value at Risk (VaR) and outputs a summary
report.  The VaR calculation here uses the historical method but can
be extended to Monte‑Carlo or parametric approaches.

Dependencies:
    pandas, numpy
"""

import argparse
import pandas as pd
import numpy as np


def load_prices(path: str) -> pd.DataFrame:
    """Load historical price data for multiple tickers.

    The CSV should have columns: Date, Ticker, Close
    """
    df = pd.read_csv(path, parse_dates=['Date'])
    return df


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily log returns for each ticker."""
    df = df.sort_values(['Ticker', 'Date'])
    df['Return'] = df.groupby('Ticker')['Close'].pct_change().apply(lambda x: np.log1p(x))
    return df.dropna(subset=['Return'])


def calculate_var(returns: pd.Series, alpha: float = 0.05) -> float:
    """Calculate historical Value at Risk (VaR) at the given confidence level."""
    return -np.quantile(returns, alpha)


def build_risk_report(df: pd.DataFrame) -> pd.DataFrame:
    """Build a summary DataFrame with volatility and VaR per ticker."""
    report = []
    for ticker, group in df.groupby('Ticker'):
        vol = group['Return'].std() * np.sqrt(252)  # annualised volatility
        var95 = calculate_var(group['Return'], 0.05)
        report.append({'Ticker': ticker, 'AnnualVolatility': vol, 'VaR95': var95})
    return pd.DataFrame(report)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute basic risk metrics from price data.")
    parser.add_argument("--prices", required=True, help="CSV of historical prices (Date, Ticker, Close)")
    parser.add_argument("--output", required=True, help="Path to save the risk report CSV")
    args = parser.parse_args()

    prices = load_prices(args.prices)
    returns = compute_returns(prices)
    report = build_risk_report(returns)
    report.to_csv(args.output, index=False)
    print(f"Risk report saved to {args.output}")


if __name__ == '__main__':
    main()