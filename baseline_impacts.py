import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, LIGHT_GRAY, BLUE


class BaselineImpacts:
    def __init__(self):
        # Load both required CSV files
        try:
            self.budget_window_data = pd.read_csv(
                "nationwide_impacts/data/raw_budget_window_metrics.csv"
            )
            self.baseline_deficit = pd.read_csv(
                "nationwide_impacts/data/baseline_deficit.csv"
            )
        except Exception as e:
            st.error(f"Error loading baseline data: {str(e)}")
            self.budget_window_data = pd.DataFrame()
            self.baseline_deficit = pd.DataFrame()

    def get_baseline_data(self, baseline_type="current_law"):
        """Get time series data for either current law or current policy"""
        if self.baseline_deficit.empty:
            return pd.DataFrame()

        baseline_deficit = self.baseline_deficit.copy()

        if baseline_type == "current_law":
            # For current law, use values from baseline_deficit.csv
            baseline_deficit["total_income_change"] = baseline_deficit["deficit_total"]
            return baseline_deficit
        else:  # current policy
            # Calculate TCJA impact as difference between tcja_extension_baseline and baseline
            tcja_data = self.budget_window_data[
                self.budget_window_data["reform"] == "tcja_extension_baseline"
            ]["total_income_change"]
            baseline_data = self.budget_window_data[
                self.budget_window_data["reform"] == "baseline"
            ]["total_income_change"]
            tcja_impact = tcja_data.values - baseline_data.values

            # Add TCJA impact to baseline deficit
            baseline_deficit["total_income_change"] = (
                baseline_deficit["deficit_total"] + tcja_impact
            )
            return baseline_deficit

    def create_metric_chart(self, current_law_data, current_policy_data, metric):
        """Create a line chart comparing current law and policy for a given metric"""
        fig = go.Figure()

        years = current_law_data["year"]

        # Add traces for current law and current policy
        for data, name, color in zip(
            [current_law_data, current_policy_data],
            ["Current Law", "Current Policy"],
            [BLUE, DARK_GRAY],
        ):
            fig.add_trace(
                go.Scatter(
                    x=years,
                    y=data[metric],
                    name=name,
                    line=dict(color=color),
                )
            )

        title = (
            "Total Deficit"
            if metric == "total_income_change"
            else metric.replace("_", " ").title()
        )
        y_axis_title = title

        fig.update_layout(
            title=f"{title} Over Time",
            xaxis_title="Year",
            yaxis_title=y_axis_title,
            hovermode="x unified",
        )

        return format_fig(fig)


def display_baseline_impacts():
    """Main function to display baseline impacts section"""
    st.markdown(
        """
    ### Baseline Policy Impacts (2026-2035)
    
    The Tax Cuts and Jobs Act (TCJA) of 2017 capped the SALT deduction, applied the AMT to fewer households, and reformed several other parts of the individual and corporate tax code. 
    
    With most provisions sunsetting after 2025, policymakers are exploring extensions and comparing them against one of two baseline scenarios:
    - **Current Law**: Assumes TCJA provisions expire as scheduled in 2025
    - **Current Policy**: Assumes TCJA provisions are extended beyond 2025
    """
    )

    if "baseline_impacts" not in st.session_state:
        with st.spinner("Loading baseline data..."):
            st.session_state.baseline_impacts = BaselineImpacts()

    current_law_data = st.session_state.baseline_impacts.get_baseline_data(
        "current_law"
    )
    current_policy_data = st.session_state.baseline_impacts.get_baseline_data(
        "current_policy"
    )

    st.markdown(
        """
    The chart below shows how extending TCJA individual provisions would affect the deficit.

    """
    )

    if not current_law_data.empty and not current_policy_data.empty:
        available_metrics = [
            col for col in current_law_data.columns if col in ["total_income_change"]
        ]

        if available_metrics:
            selected_metric = "total_income_change"
            fig = st.session_state.baseline_impacts.create_metric_chart(
                current_law_data, current_policy_data, selected_metric
            )
            st.plotly_chart(format_fig(fig), use_container_width=False)
        else:
            st.error("No metrics available to display")
    else:
        st.error("Unable to load baseline impact data")

    st.markdown("Now what happens if we change the SALT and AMT provisions?")
