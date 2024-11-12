import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def format_fig(fig):
    """Apply PolicyEngine styling to a Plotly figure"""
    fig.update_layout(
        font_family="Roboto",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(
            gridcolor="lightgray",
            zerolinecolor="lightgray",
            tickformat="$,.0f",
        ),
        xaxis=dict(
            gridcolor="lightgray",
            zerolinecolor="lightgray",
        ),
    )
    
    # Add light horizontal grid lines
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def create_reform_comparison_graph(summary_results):
    """Create a bar chart comparing household income across reforms"""
    if not summary_results:  # If no results, return empty figure
        fig = go.Figure()
        fig.update_layout(
            title="Household Income by Reform",
            yaxis_title="Household Income",
            showlegend=False,
            height=400,
        )
        return format_fig(fig)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(summary_results.keys()),
        y=list(summary_results.values()),
        text=[f"${val:,.0f}" for val in summary_results.values()],
        textposition='auto',
        marker_color='#2C6BFF',  # PolicyEngine blue
        hovertemplate='%{x}<br>Income: %{y:$,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Household Income by Reform",
        yaxis_title="Household Income",
        showlegend=False,
        height=400,
    )
    
    # Apply PolicyEngine formatting
    fig = format_fig(fig)
    
    return fig

def initialize_results_tracking():
    """Initialize empty DataFrame and dictionary for tracking results"""
    return pd.DataFrame(columns=["Household Income"]), {}

def reset_results():
    """Reset results tracking to empty state"""
    st.session_state.results_df, st.session_state.summary_results = initialize_results_tracking()

def update_results(df, summary_results, reform_name, income_value):
    """Update both the DataFrame and summary results dictionary with new values"""
    df.loc[reform_name] = income_value
    summary_results[reform_name] = income_value
    return df, summary_results