import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import BLUE, TEAL_ACCENT, TEAL_LIGHT, TEAL_PRESSED


class ImpactCharts:
    @staticmethod
    def plot_distributional_analysis(impact_data):
        """Create distributional analysis charts"""
        # Check if data is empty
        if impact_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            fig.update_layout(
                title="Average household impact by income decile in 2026",
                template="simple_white",
                height=500,
            )
            return format_fig(fig)

        # Convert decile data to labels and values
        decile_labels = [
            "Bottom 10%",
            "10-20%",
            "20-30%",
            "30-40%",
            "40-50%",
            "50-60%",
            "60-70%",
            "70-80%",
            "80-90%",
            "Top 10%",
        ]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=decile_labels,
                y=impact_data.values,
                name="Average Impact",
                text=[f"${x:,.0f}" for x in impact_data.values],
                textposition="auto",
                marker_color=BLUE,
            )
        )

        fig.update_layout(
            xaxis_title="Income group",
            yaxis_title="Average household net income change ($)",
            template="simple_white",
            showlegend=False,
            height=500,
            yaxis=dict(tickformat="$,.0f"),
        )

        return format_fig(fig)

    @staticmethod
    def plot_time_series(impact_data):
        """Create time series visualization"""
        # Check if data is empty
        if impact_data.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            fig.update_layout(
                title="Revenue Impact Over Time", template="simple_white", height=500
            )
            return format_fig(fig)

        # Ensure total_income_change is numeric and convert to billions
        try:
            y_values = pd.to_numeric(impact_data["total_income_change"]) / 1e9
        except (KeyError, ValueError):
            # Handle case where total_income_change column doesn't exist or contains invalid data
            fig = go.Figure()
            fig.add_annotation(
                text="Invalid revenue impact data",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            fig.update_layout(
                title="Revenue Impact Over Time", template="simple_white", height=500
            )
            return format_fig(fig)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=impact_data["year"],
                y=y_values,
                mode="lines+markers",
                line=dict(color=BLUE),
                marker=dict(color=BLUE),
            )
        )

        fig.update_layout(
            title="Revenue Impact Over Time",
            xaxis_title="Year",
            yaxis_title="Impact ($B)",
            template="simple_white",
            showlegend=False,
            height=500,
            yaxis=dict(tickformat="$,.0f"),
        )

        return format_fig(fig)
