import streamlit as st
import pandas as pd
from constants import TEAL_ACCENT

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
    required_columns = [
        "total_income_change",
        "percent_better_off",
        "percent_worse_off",
    ]
    if not all(col in impact_data.columns for col in required_columns):
        st.error("Required columns not found in the data.")
        return impact_data

    # Get percentages (only needed for single year)
    percent_better = impact_data["percent_better_off"].iloc[0]
    percent_worse = impact_data["percent_worse_off"].iloc[0]

    st.markdown(
        f"""
        <div style="text-align: center; margin: 25px 0;">
            <h3 style="color: #777777;">This policy would increase the net income for <span style="color: {TEAL_ACCENT}; font-weight: bold;">{percent_better:.1f}%</span> of the 
            population and decrease it for <span style="color: {TEAL_ACCENT}; font-weight: bold;">{percent_worse:.1f}%</span> in 2026.</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return impact_data
