import streamlit as st
import plotly.graph_objects as go
import pandas as pd


class BaselineImpacts:
    def __init__(self):
        # Load both required CSV files
        self.budget_window_data = pd.read_csv(
            "nationwide_impacts/data/raw_budget_window_metrics.csv"
        )
        self.baseline_deficit = pd.read_csv(
            "nationwide_impacts/data/baseline_deficit.csv"
        )

    def get_baseline_data(self, baseline_type="current_law"):
        """Get time series data for either current law or current policy"""
        # Get baseline deficit data
        baseline_deficit = self.baseline_deficit.copy()

        if baseline_type == "current_law":
            # For current law, use values from baseline_deficit.csv
            baseline_deficit["revenue_impact"] = baseline_deficit["deficit_total"]
            return baseline_deficit
        else:  # current policy
            # Calculate TCJA impact as difference between tcja_extension_baseline and baseline
            tcja_data = self.budget_window_data[
                self.budget_window_data["reform"] == "tcja_extension_baseline"
            ]["revenue_impact"]
            baseline_data = self.budget_window_data[
                self.budget_window_data["reform"] == "baseline"
            ]["revenue_impact"]
            tcja_impact = tcja_data.values - baseline_data.values

            # Add TCJA impact to baseline deficit
            baseline_deficit["revenue_impact"] = (
                baseline_deficit["deficit_total"] + tcja_impact
            )
            return baseline_deficit

    def create_metric_chart(self, current_law_data, current_policy_data, metric):
        """Create a line chart comparing current law and policy for a given metric"""
        fig = go.Figure()

        # Create year range from the data
        years = current_law_data["year"]

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
                name="Current Policy (TCJA individual provisions)",
                line=dict(color="red"),
            )
        )

        # Get display title based on metric
        if metric == "revenue_impact":
            title = "Total Deficit"
            y_axis_title = "Total Deficit"
        else:
            title = metric.replace("_", " ").title()
            y_axis_title = title

        # Update layout
        fig.update_layout(
            title=f"{title} Over Time",
            xaxis_title="Year",
            yaxis_title=y_axis_title,
            hovermode="x unified",
        )

        return fig


def display_baseline_impacts():
    """Main function to display baseline impacts section"""
    st.markdown(
        """
    ### Baseline Policy Impacts (2026-2035)
    
    The Tax Cuts and Jobs Act (TCJA) of 2017 capped the SALT deduction, applied the AMT to fewer households, and reformed several other parts of the individual and corporate tax code. With most provisions sunsetting after 2025, policymakers are exploring extensions and comparing them against one of two baseline scenarios:
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
    The chart below shows how extending TCJA individual provisions would affect the deficit, using PolicyEngine's open-source microsimulation model.

    _NB: All 10-year impacts are currently 2026 impacts replicated. We will add full budget window impacts in future versions._
    _CBO has also not yet produced a 2035 baseline forecast, so we are using the 2034 forecast for 2035._
    """
    )

    if not current_law_data.empty and not current_policy_data.empty:
        # Only show metrics that exist in the data
        available_metrics = [
            col for col in current_law_data.columns if col in ["revenue_impact"]
        ]

        def format_metric_name(x):
            if x == "revenue_impact":
                return "Total Deficit"
            return x.replace("_", " ").title()

        if len(available_metrics) > 0:
            selected_metric = "revenue_impact"
            # selected_metric = st.selectbox(
            #     "Select Metric",
            #     available_metrics,
            #     format_func=format_metric_name,
            # )

            # Create and display chart
            fig = st.session_state.baseline_impacts.create_metric_chart(
                current_law_data, current_policy_data, selected_metric
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No metrics available to display")

    else:
        st.error("Unable to load baseline impact data")

    st.markdown(
        "Now what happens if we change the SALT and AMT provisions? Let's find out in the next section."
    )
