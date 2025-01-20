import streamlit as st
import pandas as pd


def display_summary_metrics(impact_data, impact_type):
    """Display summary metrics based on impact type (single_year or budget_window)"""
    # Only show the title if this is the first display
    if impact_type == "current_law":
        st.write("### Current Law Impacts")
    elif impact_type == "single_year":
        st.write("### Single Year Impacts")
    elif impact_type == "budget_window":
        st.write("### Budget Window Impacts")

    # Check if impact_data is a DataFrame
    if isinstance(impact_data, pd.DataFrame):
        total_income_change = impact_data["total_income_change"].iloc[0]
        percent_better = impact_data["percent_better_off"].iloc[0]
        percent_worse = impact_data["percent_worse_off"].iloc[0]
    else:
        # If impact_data is already a single value or series
        total_income_change = impact_data["total_income_change"]
        percent_better = impact_data["percent_better_off"]
        percent_worse = impact_data["percent_worse_off"]

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    # Calculate revenue display value
    if impact_type == "budget_window":
        revenue_display = (
            f"${budget_window_impacts_temporary['total_income_change'].sum()/1e9:,.0f}B"
        )
    else:
        revenue_display = f"${total_income_change/1e9:,.0f}B"

    with col1:
        st.metric(
            "Revenue Impact",
            revenue_display,
            help="Change in federal revenue (billions)"
            + (" - 10 year sum" if impact_type == "budget_window" else ""),
        )

    with col2:
        st.metric(
            "Percent of Households Better Off in 2026",
            f"{percent_better:.1f}%",
            help="Percentage of households with increased household net income",
        )

    with col3:
        st.metric(
            "Percent of Households Worse Off in 2026",
            f"{percent_worse:.1f}%",
            help="Percentage of households with reduced household net income",
        )

    return impact_data
