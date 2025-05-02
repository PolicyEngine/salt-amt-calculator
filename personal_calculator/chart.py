import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, LIGHT_GRAY, BLUE, TEAL_ACCENT, TEAL_LIGHT, TEAL_PRESSED


def create_reform_comparison_graph(summary_results, baseline_scenario):
    """Create a horizontal bar chart comparing household income across reforms"""
    if not summary_results:  # If no results, return empty figure
        fig = go.Figure()
        fig.update_layout(
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
                textfont=dict(size=18, color="white", family="Arial, sans-serif"),
            )
        )

        # Add difference annotation for reform
        if reform != baseline_scenario:
            # Calculate percentage change
            pct_change = (diff / baseline_value) * 100
            # Format dollar amount annotation
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

            # Add a separate annotation for the percentage in teal
            # Calculate an appropriate x-shift based on the dollar amount length
            dollar_text_length = len(text_outside)
            x_shift = 10 + (dollar_text_length * 8)  # Estimate 8px per character

            fig.add_annotation(
                y=reform,
                x=value,
                text=f"({abs(pct_change):.1f}%)",
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                xshift=x_shift,  # Dynamic position based on dollar amount length
                font=dict(
                    size=16,
                    color=BLUE,
                    weight="bold",
                ),
            )

    fig.update_layout(
        title=dict(
            font=dict(size=24),
        ),
        showlegend=False,
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


def adjust_chart_limits(fig: go.Figure) -> None:
    x_min, x_max, y_min, y_max = None, None, None, None
    for trace in fig.data:
        if x_min is None or min(trace.x) < x_min:
            x_min = min(trace.x)

        if x_max is None or max(trace.x) > x_max:
            x_max = max(trace.x)

        if y_min is None or min(trace.y) < y_min:
            y_min = min(trace.y)

        if y_max is None or max(trace.y) > y_max:
            y_max = max(trace.y)

    x_range = x_max - x_min
    SAFETY_MARGIN_FACTOR = 0.1
    y_range = y_max - y_min

    # Handle infinite values by setting reasonable maximums
    if y_max == float('inf'):
        y_max = 160_000  # Set a reasonable maximum for y-axis
        y_range = y_max - y_min

    fig.update_layout(
        xaxis_range=[0, int(x_max + SAFETY_MARGIN_FACTOR * x_range)],
        yaxis_range=[0, int(y_max + SAFETY_MARGIN_FACTOR * y_range)],
    )
