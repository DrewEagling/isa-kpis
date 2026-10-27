from datetime import date
from pathlib import Path

import pandas as pd


# Set project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = PROJECT_ROOT / "outputs" / "portfolio_snapshot.csv"
HISTORY_FILE = PROJECT_ROOT / "data" / "portfolio_history.csv"


# Check that the portfolio snapshot exists
if not SNAPSHOT_FILE.exists():
    raise FileNotFoundError(
        f"Portfolio snapshot not found: {SNAPSHOT_FILE}\n"
        "Run the portfolio update script first."
    )


# Read the latest portfolio snapshot
portfolio = pd.read_csv(SNAPSHOT_FILE)


# Calculate portfolio totals
portfolio_value = portfolio["Market_Value_GBP"].sum()
annual_income = portfolio["Annual_Income_GBP"].sum()

if portfolio_value > 0:
    portfolio_yield = (annual_income / portfolio_value) * 100
else:
    portfolio_yield = 0


# Create today's history record
today = date.today().isoformat()

new_record = pd.DataFrame(
    {
        "Date": [today],
        "Portfolio_Value_GBP": [round(portfolio_value, 2)],
        "Annual_Income_GBP": [round(annual_income, 2)],
        "Monthly_Income_GBP": [round(annual_income / 12, 2)],
        "Portfolio_Yield_%": [round(portfolio_yield, 2)],
        "Number_of_Holdings": [len(portfolio)],
    }
)


# Read existing history or create a new history table
if HISTORY_FILE.exists():
    history = pd.read_csv(HISTORY_FILE)

    # Remove an existing record for today to prevent duplicates
    history = history[history["Date"].astype(str) != today]

    # Add today's updated record
    history = pd.concat([history, new_record], ignore_index=True)
else:
    history = new_record


# Sort history chronologically and save it
history["Date"] = pd.to_datetime(history["Date"])
history = history.sort_values("Date")
history["Date"] = history["Date"].dt.strftime("%Y-%m-%d")

history.to_csv(HISTORY_FILE, index=False)


# Display confirmation
print("\n" + "=" * 34)
print("ISA PORTFOLIO HISTORY")
print("=" * 34)
print(f"Date: {today}")
print(f"Portfolio Value: £{portfolio_value:,.2f}")
print(f"Annual Income: £{annual_income:,.2f}")
print(f"Monthly Income: £{annual_income / 12:,.2f}")
print(f"Portfolio Yield: {portfolio_yield:.2f}%")
print(f"Number of Holdings: {len(portfolio)}")
print("\nSaved:")
print(HISTORY_FILE.relative_to(PROJECT_ROOT))