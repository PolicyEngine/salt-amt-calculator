import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, LIGHT_GRAY, BLUE, TEAL_ACCENT, TEAL_LIGHT, TEAL_PRESSED


class BaselineImpacts:
    def __init__(self):
        # Load both required CSV files
        try:
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

        # Map the column names based on baseline type
        column_name = (
            "Current Law" if baseline_type == "current_law" else "Current Policy"
        )

        # Create total_income_change from the appropriate column
        baseline_deficit["total_income_change"] = baseline_deficit[column_name]

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
            title=f"Figure 6: {title} Over Time",
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

    **Current Law** deficit projections are sourced directly from the Congressional Budget Office (CBO), which provides detailed forecasts of the federal budget and economic outlook.

    You can view the full report by the CBO [here](https://www.cbo.gov/publication/60870#:~:text=The%20Budget%20Outlook,-Deficits&text=In%20CBO's%20projections%2C%20the%20federal%20budget%20deficit%20in%20fiscal%20year,to%20%242.7%20trillion%20by%202035).

    **Current Policy** projections are computed using the budgetary impact from the PolicyEngine microsimulation model, estimating the effects of extending the Tax Cuts and Jobs Act provisions beyond 2025.
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
