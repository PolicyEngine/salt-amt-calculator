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
        revenue_impact = impact_data["revenue_impact"].iloc[0]
        poverty_impact = impact_data["poverty_rate_impact"].iloc[0]
        inequality_impact = impact_data["inequality_impact"].iloc[0]
    else:
        # If impact_data is already a single value or series
        revenue_impact = impact_data["revenue_impact"]
        poverty_impact = impact_data["poverty_rate_impact"]
        inequality_impact = impact_data["inequality_impact"]

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    # Calculate values based on impact type
    if impact_type == "budget_window":
        revenue_display = f"${budget_window_impacts_temporary['revenue_impact'].sum()/1e9:,.0f}B"
        poverty_display = f"{budget_window_impacts_temporary['poverty_rate_impact'].mean():+.2f}pp"
        inequality_display = f"{budget_window_impacts_temporary['inequality_impact'].mean():+.2f}%"
    else:
        revenue_display = f"${revenue_impact/1e9:,.0f}B"
        poverty_display = f"{poverty_impact:+.2f}pp"
        inequality_display = f"{inequality_impact:+.2f}%"

    with col1:
        st.metric(
            "Revenue Impact",
            revenue_display,
            help="Change in federal revenue (billions)" + (" - 10 year sum" if impact_type == "budget_window" else ""),
        )

    with col2:
        st.metric(
            "Poverty Rate Impact",
            f"{poverty_display}",
            help="Change in poverty rate (percentage points)",
        )

    with col3:
        st.metric(
            "Inequality Impact",
            f"{inequality_display}",
            help="Change in income inequality (percent)",
        )

    return impact_data
