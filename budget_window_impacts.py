import pandas as pd
import numpy as np


def create_budget_window_impacts():
    # Read the single year impacts
    df = pd.read_csv("nationwide_impacts/data/single_year_impacts.csv")

    # Create empty list to store rows
    rows = []

    # Years to duplicate across
    years = range(2026, 2036)  # 2026-2035 inclusive

    # For each reform in the original data
    for _, row in df.iterrows():
        # Create a row for each year
        for year in years:
            new_row = row.copy()
            new_row["year"] = year
            rows.append(new_row)

    # Create new dataframe
    budget_window_df = pd.DataFrame(rows)

    # Save to CSV
    budget_window_df.to_csv(
        "nationwide_impacts/data/budget_window_impacts_temporary.csv", index=False
    )


if __name__ == "__main__":
    create_budget_window_impacts()
