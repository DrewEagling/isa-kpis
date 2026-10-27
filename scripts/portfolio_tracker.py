import pandas as pd
import yfinance as yf
import time

# Load holdings
holdings = pd.read_csv("data/holdings.csv")

prices = []
yields = []
annual_income = []

for ticker, shares in zip(holdings["Ticker"], holdings["Shares"]):

    if pd.isna(ticker):
        prices.append(None)
        yields.append(None)
        annual_income.append(None)
        continue

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        price = info.get("currentPrice")
        div_yield = info.get("dividendYield")
        div_rate = info.get("dividendRate")

        prices.append(price)
        yields.append(div_yield)

        if div_rate:
            annual_income.append(div_rate * shares)
        else:
            annual_income.append(0)

        print(f"Downloaded: {ticker}")

        time.sleep(0.5)

    except Exception as e:

        print(f"Error: {ticker}")
        prices.append(None)
        yields.append(None)
        annual_income.append(None)

# Add calculations

holdings["Current_Price"] = prices
holdings["Dividend_Yield_%"] = yields
holdings["Annual_Income_GBP"] = annual_income

# Market value

holdings["Market_Value_GBP"] = (
    holdings["Shares"]
    * holdings["Current_Price"]
) / 100

# Portfolio KPIs

portfolio_value = holdings["Market_Value_GBP"].sum()
annual_income_total = holdings["Annual_Income_GBP"].sum()

portfolio_yield = (
    annual_income_total /
    portfolio_value
) * 100

print("\n==============================")
print("ISA PORTFOLIO SUMMARY")
print("==============================")

print(f"Portfolio Value: £{portfolio_value:,.2f}")
print(f"Annual Income: £{annual_income_total:,.2f}")
print(f"Monthly Income: £{annual_income_total/12:,.2f}")
print(f"Portfolio Yield: {portfolio_yield:.2f}%")

# Save

holdings.to_csv(
    "outputs/portfolio_snapshot.csv",
    index=False
)

print("\nSaved:")
print("outputs/portfolio_snapshot.csv")
