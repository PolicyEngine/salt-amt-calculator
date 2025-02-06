import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, LIGHT_GRAY, BLUE


def create_reform_comparison_graph(summary_results, baseline_scenario):
    """Create a horizontal bar chart comparing household income across reforms"""
    if not summary_results:  # If no results, return empty figure
        fig = go.Figure()
        fig.update_layout(
            title="Household Net Income after Income Taxes and Transfers by Reform",
            showlegend=False,
            height=400,
        )
        return format_fig(fig)

    # Convert to DataFrame and sort
    df = pd.DataFrame(summary_results.items(), columns=["reform", "income"])

    # Custom sorting function to prioritize baseline
    def custom_sort(row):
        if row.reform == baseline_scenario:
            return (2, -row.income)
        else:
            return (0, -row.income)

    # Sort the DataFrame
    df_sorted = df.sort_values(
        by=["reform", "income"],
        key=lambda x: pd.Series(
            [custom_sort(row) for row in df.itertuples(index=False)]
        ),
    )

    fig = go.Figure()
    baseline_value = summary_results[baseline_scenario]

    for reform, value in zip(df_sorted["reform"], df_sorted["income"]):
        diff = value - baseline_value
        text_inside = f"${round(value):,}"
        text_outside = f"+${round(diff):,}" if diff >= 0 else f"-${round(-diff):,}"

        # Set colors - baseline gets dark gray, reform gets blue
        color = DARK_GRAY if reform == baseline_scenario else BLUE

        fig.add_trace(
            go.Bar(
                y=[reform],
                x=[value],
                name=reform,
                orientation="h",
                marker_color=color,
                text=text_inside,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(size=18, color="white", weight="bold"),
            )
        )

        # Add difference annotation for reform
        if reform != baseline_scenario:
            fig.add_annotation(
                y=reform,
                x=value,
                text=text_outside,
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                xshift=5,
                font=dict(size=16, color=color),
            )

    fig.update_layout(
        title=dict(
            text=f"Household Net Income vs {baseline_scenario}", font=dict(size=24)
        ),
    )

    return format_fig(fig)


def initialize_results_tracking():
    """Initialize empty DataFrame and dictionary for tracking results"""
    return pd.DataFrame(columns=["Household Income"]), {}


def reset_results():
    """Reset results tracking to empty state"""
    st.session_state.results_df, st.session_state.summary_results = (
        initialize_results_tracking()
    )


def update_results(df, summary_results, reform_name, income_value):
    """Update both the DataFrame and summary results dictionary with new values"""
    df.loc[reform_name] = income_value
    summary_results[reform_name] = income_value
    return df, summary_results
