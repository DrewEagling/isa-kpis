from pathlib import Path
import subprocess
import sys


# Set project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_FOLDER = PROJECT_ROOT / "scripts"


# Scripts run in this order
SCRIPTS_TO_RUN = [
    "update_portfolio.py",
    "record_history.py",
    "create_charts.py",
]


print("\n" + "=" * 46)
print("RUNNING ISA PORTFOLIO TRACKER")
print("=" * 46)


for script_name in SCRIPTS_TO_RUN:
    script_path = SCRIPTS_FOLDER / script_name

    if not script_path.exists():
        print(f"\nERROR: Script not found: {script_path}")
        sys.exit(1)

    print(f"\nRunning: {script_name}")
    print("-" * 46)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print("\n" + "=" * 46)
        print("ISA TRACKER STOPPED")
        print("=" * 46)
        print(f"Failed script: {script_name}")
        print("Fix the error above before running again.")
        sys.exit(result.returncode)

    print(f"\nCompleted: {script_name}")


print("\n" + "=" * 46)
print("ISA PORTFOLIO TRACKER COMPLETE")
print("=" * 46)
print("\nUpdated files:")

output_files = [
    PROJECT_ROOT / "outputs" / "portfolio_snapshot.csv",
    PROJECT_ROOT / "data" / "portfolio_history.csv",
    PROJECT_ROOT
    / "outputs"
    / "charts"
    / "annual_income_by_holding.png",
]

for output_file in output_files:
    if output_file.exists():
        print(f"✓ {output_file.relative_to(PROJECT_ROOT)}")
    else:
        print(f"⚠ Not found: {output_file.relative_to(PROJECT_ROOT)}")
