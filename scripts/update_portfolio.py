import pandas as pd
import yfinance as yf

holdings = pd.read_csv("data/holdings.csv")

results = []

for _, row in holdings.iterrows():

    ticker = row["Ticker"]

    stock = yf.Ticker(ticker)

    try:
        info = stock.info

        current_price = info.get("currentPrice")

        dividend_yield = info.get("dividendYield")

        results.append(
            {
                "Ticker": ticker,
                "Shares": row["Shares"],
                "Current_Price": current_price,
                "Dividend_Yield": dividend_yield
            }
        )

    except Exception as e:

        print(f"Error with {ticker}: {e}")

portfolio = pd.DataFrame(results)

print(portfolio)