import streamlit as st
import pandas as pd


def display_summary_metrics(impact_data, baseline):
    """
    Display summary metrics for the selected reform and baseline scenario.

    Parameters:
        impact_data (pd.DataFrame or dict): The impact data for the selected reform.
        baseline (str): The baseline scenario ("Current Law" or "Current Policy").

    Returns:
        pd.DataFrame: The filtered impact data.
    """
    # Convert dict to DataFrame if necessary
    if not isinstance(impact_data, pd.DataFrame):
        impact_data = pd.DataFrame([impact_data])

    # Check for required columns
    required_columns = ['total_income_change', 'percent_better_off', 'percent_worse_off']
    if not all(col in impact_data.columns for col in required_columns):
        st.error("Required columns not found in the data.")
        return impact_data
    
    # Get percentages (only needed for single year)
    percent_better = impact_data["percent_better_off"].iloc[0]
    percent_worse = impact_data["percent_worse_off"].iloc[0]

    st.write(
        f"### This policy would increase the net income for {percent_better:.1f}% of the "
        f"population and decrease it for {percent_worse:.1f}% in 2026."
    )

    return impact_data
