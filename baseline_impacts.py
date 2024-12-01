import streamlit as st
import plotly.graph_objects as go
import pandas as pd


class BaselineImpacts:
    def __init__(self):
        # Read CSV directly instead of using NationwideImpacts
        self.data = pd.read_csv("nationwide_impacts/data/raw_budget_window_metrics.csv")

    def get_baseline_data(self, baseline_type="current_law"):
        """Get time series data for either current law or current policy"""
        if baseline_type == "current_law":
            reform_name = "baseline"
        else:  # current policy
            reform_name = "tcja_extension_baseline"

        # Filter the dataframe for the specific reform
        return self.data[self.data["reform"] == reform_name]

    def create_metric_chart(self, current_law_data, current_policy_data, metric):
        """Create a line chart comparing current law and policy for a given metric"""
        fig = go.Figure()

        # Create year range for x-axis (2026-2035)
        years = list(range(2026, 2036))

        # Add current law line
        fig.add_trace(
            go.Scatter(
                x=years,
                y=current_law_data[metric],
                name="Current Law",
                line=dict(color="blue"),
            )
        )

        # Add current policy line
        fig.add_trace(
            go.Scatter(
                x=years,
                y=current_policy_data[metric],
                name="Current Policy (TCJA)",
                line=dict(color="red"),
            )
        )

        # Update layout
        fig.update_layout(
            title=f"{metric.replace('_', ' ').title()} Over Time",
            xaxis_title="Year",
            yaxis_title=metric.replace("_", " ").title(),
            hovermode="x unified",
        )

        return fig


def display_baseline_impacts():
    """Main function to display baseline impacts section"""
    st.markdown(
        """
    ### Baseline Policy Impacts (2026-2035)
    
    The Tax Cuts and Jobs Act (TCJA) of 2017 made significant changes to the tax code, including modifications 
    to the State and Local Tax (SALT) deduction. However, many provisions of TCJA are set to expire at the end 
    of 2025.

    This creates two possible baseline scenarios for analyzing future tax policies:
    - **Current Law**: Assumes TCJA provisions expire as scheduled in 2025
    - **Current Policy**: Assumes TCJA provisions are extended beyond 2025
    """
    )

    # Initialize baseline impacts
    if "baseline_impacts" not in st.session_state:
        with st.spinner("Loading baseline data..."):
            st.session_state.baseline_impacts = BaselineImpacts()

    # Get data
    current_law_data = st.session_state.baseline_impacts.get_baseline_data(
        "current_law"
    )
    current_policy_data = st.session_state.baseline_impacts.get_baseline_data(
        "current_policy"
    )

    st.markdown(
        """
    The chart below compares these two baseline scenarios across different metrics for the 
    10-year budget window from 2026-2035.
    """
    )

    if not current_law_data.empty and not current_policy_data.empty:
        # Metric selector above the chart
        available_metrics = ["revenue_impact", "poverty_rate", "inequality_rate"]
        selected_metric = st.selectbox(
            "Select Metric",
            available_metrics,
            format_func=lambda x: x.replace("_", " ").title(),
        )

        # Create and display chart
        fig = st.session_state.baseline_impacts.create_metric_chart(
            current_law_data, current_policy_data, selected_metric
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Unable to load baseline impact data")
