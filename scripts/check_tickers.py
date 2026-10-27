import yfinance as yf

ticker = yf.Ticker("BTA.L")

print(ticker.info.get("currentPrice"))
print(ticker.info.get("dividendYield"))
print(ticker.info.get("dividendRate"))

