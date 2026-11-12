"""Stock market data API: prices, top movers, news, options, short interest and insider trades

Runnable examples: each one is a single request to the DataPorium API.

    python examples.py                      # list the examples
    python examples.py daily-prices
    python examples.py daily-prices --csv out.csv
    python examples.py daily-prices --json       # the raw answer

Needs a DataPorium API key in the DATAPORIUM_API_KEY environment variable.
"""
from __future__ import annotations

import argparse
import json
import sys

from dataporium import DataPorium, to_frame

# name: (question, method, parameters, key of the rows inside the answer)
EXAMPLES = {
    'daily-prices': ('Daily prices of a stock (open, high, low, close, volume)', 'stock_price_1d', {'ticker': 'AAPL'}, 'price_history'),
    'index-prices': ('Daily prices of the S&P 500 index', 'stock_price_1d', {'ticker': '^GSPC'}, 'price_history'),
    'crypto-prices': ('Daily Bitcoin prices', 'stock_price_1d', {'ticker': 'BTC-USD'}, 'price_history'),
    'intraday': ('5-minute prices for day trading', 'stock_price_5m', {'ticker': 'SPY'}, None),
    'commodities': ('Gold futures, daily', 'commodity_price_1d', {'symbol': 'GC=F'}, 'price_history'),
    'forex': ('US dollar to euro, daily', 'fx', {'currency_conversion': 'USD-EUR', 'one_day_interval': '1d'}, None),
    'top-gainers': ('Top gainers', 'gain_loss', {'status': 'gainer'}, None),
    'sector-performance': ('Sector performance on Nasdaq', 'sector_performance', {'exchange': 'NASDAQ'}, None),
    'industry-performance': ('Performance of one industry', 'industry_performance', {'industry': 'Biotechnology'}, None),
    'stock-news': ('Latest news about a stock', 'stock_news', {'ticker': 'NVDA'}, None),
    'press-releases': ('Company press releases', 'press_release', {'symbol': 'NVDA'}, None),
    'earnings-dates': ('Earnings dates, splits and dividends of a stock', 'earnings_split_calendar', {'symbol': 'MSFT'}, None),
    'ipo-calendar': ('Recent and upcoming IPOs', 'ipo_calendar', {}, None),
    'options-chain': ('Options chain: calls and puts with strikes, prices and Greeks', 'options_callsputs', {'symbol': 'AAPL'}, None),
    'short-interest': ('Short interest of a stock over time, with days to cover', 'short_interest', {'symbol': 'GME', 'date_from': '2025-01-01'}, None),
    'most-shorted': ('Most shorted stocks over $1 billion market cap', 'short_interest_ranking', {'min_market_cap': 1000000000, 'sort': 'short_pct', 'order': 'desc', 'limit': 25}, None),
    'insider-trades': ('Insider buys and sells of a company', 'insider_transaction_history', {'symbol': 'TSLA'}, None),
    'insider-summary': ('Insider ownership summary', 'insider_holdings_summary', {'symbol': 'TSLA'}, None),
    'shareholders': ('Who owns a stock: institutions, retail, insiders', 'shareholders_by_type', {'symbol': 'AAPL'}, None),
    'find-ticker': ('Find a ticker by company name', 'symbols_list', {'company_name': 'Nvidia'}, None),
}


def rows(answer, key=None):
    """The answer as a DataFrame, or None when it has no table in it."""
    try:
        frame = to_frame(answer, key=key)
    except (KeyError, TypeError):
        return None
    return frame if len(frame) > 1 else None  # one record reads better as JSON


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("example", nargs="?", help="Name of the example; leave out to list them")
    parser.add_argument("--csv", help="Save the rows to this CSV file")
    parser.add_argument("--json", action="store_true", help="Print the raw JSON answer")
    parser.add_argument("--rows", type=int, default=20, help="Rows to print (default 20)")
    args = parser.parse_args(argv)

    if not args.example:
        width = max(len(name) for name in EXAMPLES)
        for name, (question, *_rest) in EXAMPLES.items():
            print(f"{name:<{width}}  {question}")
        return 0
    if args.example not in EXAMPLES:
        parser.error(f"unknown example {args.example!r}; run without arguments to list them")

    question, method, params, key = EXAMPLES[args.example]
    print(f"{question}\n  dp.{method}({', '.join(f'{k}={v!r}' for k, v in params.items())})\n")
    answer = DataPorium().call(method, **params)

    frame = None if args.json else rows(answer, key)
    if frame is None:
        print(json.dumps(answer, indent=2, default=str)[:20000])
    else:
        print(frame.head(args.rows).to_string(max_colwidth=40))
        print(f"\n{len(frame)} rows")
    if args.csv:
        if frame is None:
            frame = rows(answer, key)
        if frame is None:
            print("This answer has no table to save.", file=sys.stderr)
            return 1
        frame.to_csv(args.csv, index=False)
        print(f"Saved {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
