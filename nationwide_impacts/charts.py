import plotly.graph_objects as go
import pandas as pd


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
                title="Average Impact by Income Group",
                template="simple_white",
                height=500,
            )
            return fig

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
            )
        )

        fig.update_layout(
            title="Average Impact by Income Group",
            xaxis_title="Income Group",
            yaxis_title="Impact ($)",
            template="simple_white",
            showlegend=False,
            height=500,
            yaxis=dict(tickformat="$,.0f"),
        )

        return fig

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
            return fig

        # Ensure revenue_impact is numeric and convert to billions
        try:
            y_values = pd.to_numeric(impact_data["revenue_impact"]) / 1e9
        except (KeyError, ValueError):
            # Handle case where revenue_impact column doesn't exist or contains invalid data
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
            return fig

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=impact_data["year"], y=y_values, mode="lines+markers")
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

        return fig
