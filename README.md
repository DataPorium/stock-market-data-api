# Stock market data API: prices, top movers, news, options, short interest and insider trades

Get daily and 5-minute prices for US stocks, ETFs, indexes and crypto, the day's top gainers and losers, sector performance, company news, options chains, short interest and insider trades, plus commodities, currencies and the earnings calendar. Every example is one request to the [DataPorium](https://dataporium.tech) REST API, shown in Python and curl.

## Quick start

```bash
pip install git+https://github.com/DataPorium/dataporium-python.git
export DATAPORIUM_API_KEY="YOUR_API_KEY"
```

```python
from dataporium import DataPorium, to_frame

dp = DataPorium()   # reads DATAPORIUM_API_KEY
answer = dp.stock_price_1d(ticker="AAPL")
print(to_frame(answer, key="price_history").head())
```

Or run any example below from this repository:

```bash
git clone https://github.com/DataPorium/stock-market-data-api.git
cd stock-market-data-api
pip install -r requirements.txt
python examples.py           # list the examples
python examples.py daily-prices     # run one
python examples.py daily-prices --csv out.csv
```

## What you can get

| Question | Example | Endpoint |
|---|---|---|
| Daily prices of a stock (open, high, low, close, volume) | [`daily-prices`](#daily-prices) | `GET /stock-price-1d` |
| Daily prices of the S&P 500 index | [`index-prices`](#index-prices) | `GET /stock-price-1d` |
| Daily Bitcoin prices | [`crypto-prices`](#crypto-prices) | `GET /stock-price-1d` |
| 5-minute prices for day trading | [`intraday`](#intraday) | `GET /stock-price-5m` |
| Gold futures, daily | [`commodities`](#commodities) | `GET /commodity-price-1d` |
| US dollar to euro, daily | [`forex`](#forex) | `GET /fx` |
| Top gainers | [`top-gainers`](#top-gainers) | `GET /gain-loss` |
| Sector performance on Nasdaq | [`sector-performance`](#sector-performance) | `GET /sector-performance` |
| Performance of one industry | [`industry-performance`](#industry-performance) | `GET /industry-performance` |
| Latest news about a stock | [`stock-news`](#stock-news) | `GET /stock-news` |
| Company press releases | [`press-releases`](#press-releases) | `GET /press-release` |
| Earnings dates, splits and dividends of a stock | [`earnings-dates`](#earnings-dates) | `GET /earnings-split-calendar` |
| IPO calendar entry of one company | [`ipo-calendar`](#ipo-calendar) | `GET /ipo-calendar` |
| Options chain: calls and puts with strikes, prices and Greeks | [`options-chain`](#options-chain) | `GET /options-callsputs` |
| Short interest of a stock over time, with days to cover | [`short-interest`](#short-interest) | `GET /short-interest` |
| Most shorted stocks over $1 billion market cap | [`most-shorted`](#most-shorted) | `GET /short-interest/ranking` |
| Insider buys and sells of a company | [`insider-trades`](#insider-trades) | `GET /insider-transaction-history` |
| Insider ownership summary | [`insider-summary`](#insider-summary) | `GET /insider-holdings-summary` |
| Who owns a stock: institutions, retail, insiders | [`shareholders`](#shareholders) | `GET /shareholders-by-type` |
| Find a ticker by company name | [`find-ticker`](#find-ticker) | `GET /symbols-list` |

## Prices

<a id="daily-prices"></a>
### Daily prices of a stock (open, high, low, close, volume)

```python
dp.stock_price_1d(ticker="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/stock-price-1d?ticker=AAPL"
```

The bars are in `price_history`, newest first. ETFs work the same way (`SPY`, `QQQ`).

<a id="index-prices"></a>
### Daily prices of the S&P 500 index

```python
dp.stock_price_1d(ticker="^GSPC")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/stock-price-1d?ticker=%5EGSPC"
```

Index tickers start with `^`; in a URL write it as `%5E`. Also `^DJI`, `^IXIC`, `^RUT`, `^VIX`.

<a id="crypto-prices"></a>
### Daily Bitcoin prices

```python
dp.stock_price_1d(ticker="BTC-USD")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/stock-price-1d?ticker=BTC-USD"
```

Crypto uses `-USD` after the symbol.

<a id="intraday"></a>
### 5-minute prices for day trading

```python
dp.stock_price_5m(ticker="SPY")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/stock-price-5m?ticker=SPY"
```

<a id="commodities"></a>
### Gold futures, daily

```python
dp.commodity_price_1d(symbol="GC=F")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/commodity-price-1d?symbol=GC%3DF"
```

Crude oil is `CL=F`.

<a id="forex"></a>
### US dollar to euro, daily

```python
dp.fx(currency_conversion="USD-EUR", one_day_interval="1d")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/fx?currency_conversion=USD-EUR&one_day_interval=1d"
```

## Market movers

<a id="top-gainers"></a>
### Top gainers

```python
dp.gain_loss(status="gainer")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/gain-loss?status=gainer"
```

`status=loser` for the top losers.

<a id="sector-performance"></a>
### Sector performance on Nasdaq

```python
dp.sector_performance(exchange="NASDAQ")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/sector-performance?exchange=NASDAQ"
```

<a id="industry-performance"></a>
### Performance of one industry

```python
dp.industry_performance(industry="Biotechnology")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/industry-performance?industry=Biotechnology"
```

## News and events

<a id="stock-news"></a>
### Latest news about a stock

```python
dp.stock_news(ticker="NVDA")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/stock-news?ticker=NVDA"
```

<a id="press-releases"></a>
### Company press releases

```python
dp.press_release(symbol="NVDA")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/press-release?symbol=NVDA"
```

<a id="earnings-dates"></a>
### Earnings dates, splits and dividends of a stock

```python
dp.earnings_split_calendar(symbol="MSFT")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/earnings-split-calendar?symbol=MSFT"
```

<a id="ipo-calendar"></a>
### IPO calendar entry of one company

```python
dp.ipo_calendar(symbol="WMT")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/ipo-calendar?symbol=WMT"
```

Without a symbol, the answer lists the recent and upcoming IPOs, newest first.

## Options, short interest and insiders

<a id="options-chain"></a>
### Options chain: calls and puts with strikes, prices and Greeks

```python
dp.options_callsputs(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/options-callsputs?symbol=AAPL"
```

<a id="short-interest"></a>
### Short interest of a stock over time, with days to cover

```python
dp.short_interest(symbol="GME", date_from="2025-01-01")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/short-interest?symbol=GME&date_from=2025-01-01"
```

Reported twice a month.

<a id="most-shorted"></a>
### Most shorted stocks over $1 billion market cap

```python
dp.short_interest_ranking(min_market_cap=1000000000, sort="short_pct", order="desc", limit=25)
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/short-interest/ranking?min_market_cap=1000000000&sort=short_pct&order=desc&limit=25"
```

<a id="insider-trades"></a>
### Insider buys and sells of a company

```python
dp.insider_transaction_history(symbol="TSLA")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/insider-transaction-history?symbol=TSLA"
```

<a id="insider-summary"></a>
### Insider ownership summary

```python
dp.insider_holdings_summary(symbol="TSLA")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/insider-holdings-summary?symbol=TSLA"
```

<a id="shareholders"></a>
### Who owns a stock: institutions, retail, insiders

```python
dp.shareholders_by_type(symbol="AAPL")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/shareholders-by-type?symbol=AAPL"
```

## Look up a ticker

<a id="find-ticker"></a>
### Find a ticker by company name

```python
dp.symbols_list(company_name="Nvidia")
```

```bash
curl -H "apikey: $DATAPORIUM_API_KEY" "https://api.dataporium.io/symbols-list?company_name=Nvidia"
```

Also by `cik`.

## Answers

Every answer is JSON. Many are a list of rows; paged answers hold their rows under `rows` with `total`, `limit` and `offset`. `to_frame(answer)` in the Python library finds the rows and returns a pandas DataFrame. Each endpoint and all of its parameters are described in the [API documentation](https://dataporium.tech/api-docs), and `print(dp.describe("<method>"))` shows them in Python.

## Use it in Claude, ChatGPT or Cursor

With the [DataPorium MCP server](https://github.com/DataPorium/dataporium-mcp), Claude, ChatGPT or Cursor can screen about 45,000 companies (`screen_stocks`) and pull prices, news and short interest for the results, all from one question.

## Ready-made scripts

- [stock-price-history-to-csv](https://github.com/DataPorium/stock-price-history-to-csv): save price history of many tickers to CSV

## Get an API key

Sign up at [dataporium.tech](https://dataporium.tech/pricing) and subscribe to the Premium plan; the key is in your account settings. It works for the REST API (600 requests per minute) and the MCP server. Send it in the `apikey` header, as above; a `?apikey=` query parameter also works, but a key in a URL can end up in logs. Keep the key out of code you commit or share.

## More

- Python library: [dataporium-python](https://github.com/DataPorium/dataporium-python)
- JavaScript and TypeScript library: [dataporium-js](https://github.com/DataPorium/dataporium-js)
- Examples in curl, R, Google Sheets and Excel: [financial-data-api](https://github.com/DataPorium/financial-data-api)
- AI assistants: [dataporium-mcp](https://github.com/DataPorium/dataporium-mcp)
- API documentation: <https://dataporium.tech/api-docs>

## License

The code in this repository is released under the [MIT License](LICENSE). Use of the API and its data is governed by the DataPorium [Terms of Use](https://dataporium.tech/terms-of-use). Data is for information only and is not investment advice.
