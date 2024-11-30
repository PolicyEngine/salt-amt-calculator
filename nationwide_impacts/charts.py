import plotly.graph_objects as go
import pandas as pd

class ImpactCharts:
    @staticmethod
    def plot_distributional_analysis(impact_data):
        """Create distributional analysis charts"""
        # Convert decile data to labels and values
        decile_labels = [
            'Bottom 10%', '10-20%', '20-30%', '30-40%', '40-50%',
            '50-60%', '60-70%', '70-80%', '80-90%', 'Top 10%'
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=decile_labels,
            y=impact_data.values,
            name='Average Impact',
            text=[f'${x:,.0f}' for x in impact_data.values],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Average Impact by Income Group",
            xaxis_title="Income Group",
            yaxis_title="Impact ($)",
            template="simple_white",
            showlegend=False,
            height=500,
            yaxis=dict(tickformat="$,.0f")
        )
        
        return fig

    @staticmethod
    def plot_time_series(impact_data):
        """Create time series visualization"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=impact_data.index,
            y=impact_data.values / 1e9,  # Convert to billions
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title="Revenue Impact Over Time",
            xaxis_title="Year",
            yaxis_title="Impact ($B)",
            template="simple_white",
            showlegend=False,
            height=500,
            yaxis=dict(tickformat="$,.0f")
        )
        
        return fig