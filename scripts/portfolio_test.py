import pandas as pd
import yfinance as yf

holdings = pd.read_csv("data/holdings.csv")

current_prices = []

for ticker in holdings["Ticker"]:

    try:
        stock = yf.Ticker(ticker)

        price = stock.history(period="1d")["Close"].iloc[-1]

        print(f"{ticker}: {price}")

        current_prices.append(price)

    except Exception as e:

        print(f"Error: {ticker} - {e}")

        current_prices.append(None)