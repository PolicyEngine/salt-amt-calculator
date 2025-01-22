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
    # Determine the impact type based on the input data
    if isinstance(impact_data, pd.DataFrame):
        if "year" in impact_data.columns:
            impact_type = "budget_window"
        else:
            impact_type = "single_year"
    else:
        impact_type = "single_year"

    # Display the appropriate title
    if impact_type == "single_year":
        st.write("### Nationwide Impacts")
    elif impact_type == "budget_window":
        st.write("### Budget Window Impacts")

    # Check if impact_data is a DataFrame
    if isinstance(impact_data, pd.DataFrame):
        if impact_type == "budget_window":
            # Sum the total_income_change for all years in the budget window
            if "total_income_change" in impact_data.columns:
                total_income_change = impact_data["total_income_change"].sum()
            else:
                st.error("Column 'total_income_change' not found in the data.")
                return impact_data
        else:
            # For single-year impacts, extract the first row
            if "total_income_change" in impact_data.columns:
                total_income_change = impact_data["total_income_change"].iloc[0]
                percent_better = impact_data["percent_better_off"].iloc[0]
                percent_worse = impact_data["percent_worse_off"].iloc[0]
            else:
                st.error("Column 'total_income_change' not found in the data.")
                return impact_data
    else:
        # If impact_data is already a single value or series
        if "total_income_change" in impact_data:
            total_income_change = impact_data["total_income_change"]
            percent_better = impact_data["percent_better_off"]
            percent_worse = impact_data["percent_worse_off"]
        else:
            st.error("Key 'total_income_change' not found in the data.")
            return impact_data

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    # Calculate revenue display value
    if impact_type == "budget_window":
        revenue_display = f"${total_income_change / 1e9:,.0f}B"
    else:
        revenue_display = f"${total_income_change / 1e9:,.0f}B"

    with col1:
        st.metric(
            "Revenue Impact",
            revenue_display,
            help="Change in federal revenue (billions)"
            + (" - 10 year sum" if impact_type == "budget_window" else ""),
        )

    if impact_type != "budget_window":
        with col2:
            st.metric(
                "Percent of Households Better Off",
                f"{percent_better:.1f}%",
                help="Percentage of households with increased household net income",
            )

        with col3:
            st.metric(
                "Percent of Households Worse Off",
                f"{percent_worse:.1f}%",
                help="Percentage of households with reduced household net income",
            )

    return impact_data