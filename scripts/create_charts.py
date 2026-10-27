from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Set project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = PROJECT_ROOT / "outputs" / "portfolio_snapshot.csv"
CHARTS_FOLDER = PROJECT_ROOT / "outputs" / "charts"
CHART_FILE = CHARTS_FOLDER / "annual_income_by_holding.png"


# Check that the portfolio snapshot exists
if not SNAPSHOT_FILE.exists():
    raise FileNotFoundError(
        f"Portfolio snapshot not found: {SNAPSHOT_FILE}\n"
        "Run the portfolio update script first."
    )


# Create the charts folder if it does not already exist
CHARTS_FOLDER.mkdir(parents=True, exist_ok=True)


# Read the latest portfolio snapshot
portfolio = pd.read_csv(SNAPSHOT_FILE)


# Check the required columns exist
required_columns = ["Company", "Annual_Income_GBP"]

missing_columns = [
    column for column in required_columns
    if column not in portfolio.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# Prepare the data
chart_data = portfolio[
    ["Company", "Annual_Income_GBP"]
].copy()

chart_data["Annual_Income_GBP"] = pd.to_numeric(
    chart_data["Annual_Income_GBP"],
    errors="coerce"
)

chart_data = chart_data.dropna(
    subset=["Company", "Annual_Income_GBP"]
)

chart_data = chart_data.sort_values(
    "Annual_Income_GBP",
    ascending=True
)


# Create a horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 14))

bars = ax.barh(
    chart_data["Company"],
    chart_data["Annual_Income_GBP"],
    color="#2F5597"
)


# Add income labels to each bar
for bar in bars:
    income = bar.get_width()

    ax.text(
        income,
        bar.get_y() + bar.get_height() / 2,
        f" £{income:,.2f}",
        va="center",
        fontsize=8
    )


# Format the chart
ax.set_title(
    "Estimated Annual Dividend Income by Holding",
    fontsize=16,
    fontweight="bold",
    pad=15
)

ax.set_xlabel("Estimated Annual Dividend Income (£)")
ax.set_ylabel("Company")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.4
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()


# Save and close the chart
plt.savefig(
    CHART_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# Display confirmation
total_income = chart_data["Annual_Income_GBP"].sum()

print("\n" + "=" * 42)
print("ISA DIVIDEND INCOME CHART")
print("=" * 42)
print(f"Holdings charted: {len(chart_data)}")
print(f"Total annual income: £{total_income:,.2f}")
print("\nSaved:")
print(CHART_FILE.relative_to(PROJECT_ROOT))