import pandas as pd
import yfinance as yf

holdings = pd.read_csv("data/holdings.csv")

for ticker in holdings["Ticker"]:

    if pd.isna(ticker):
        continue

    stock = yf.Ticker(ticker)

    info = stock.info

    print(
        ticker,
        info.get("currentPrice"),
        info.get("dividendYield")
    )