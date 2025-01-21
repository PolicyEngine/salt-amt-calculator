import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig

# Define colors - using more neutral shades that work in both modes
DARK_GRAY = "rgba(74, 74, 74, 0.9)"  # More transparent dark gray
LIGHT_GRAY = "rgba(124, 124, 124, 0.9)"  # More transparent light gray
BLUE_SHADES = [
    "rgba(44, 107, 255, 0.9)",  # Bright blue
    "rgba(0, 82, 204, 0.9)",  # Darker blue
    "rgba(0, 61, 153, 0.9)",  # Even darker blue
]


def create_reform_comparison_graph(summary_results):
    """Create a horizontal bar chart comparing household income across reforms"""
    if not summary_results:  # If no results, return empty figure
        fig = go.Figure()
        fig.update_layout(
            title="Household Income by Reform",
            showlegend=False,
            height=400,
        )
        return format_fig(fig)

    # Convert to DataFrame and sort
    df = pd.DataFrame(summary_results.items(), columns=["reform", "income"])

    # Custom sorting function to ensure Current Law always shows up on top
    def custom_sort(row):
        if row.reform == "Current Law":
            return (2, -row.income)
        elif row.reform == "Current Policy":
            return (1, -row.income)
        else:
            return (0, -row.income)

    # Sort the DataFrame using the custom sorting function
    df_sorted = df.sort_values(
        by=["reform", "income"],
        key=lambda x: pd.Series(
            [custom_sort(row) for row in df.itertuples(index=False)]
        ),
    )

    fig = go.Figure()

    # Get baseline (Current Law) value for calculating differences
    baseline_value = summary_results["Current Law"]

    # Counter for custom reforms to assign different shades of blue
    reform_counter = 0

    # Add bars for each reform
    for reform, value in zip(df_sorted["reform"], df_sorted["income"]):
        # Calculate difference from baseline
        diff = value - baseline_value

        # Format text labels
        text_inside = f"${round(value):,}"
        text_outside = f"+${round(diff):,}" if diff >= 0 else f"-${round(-diff):,}"

        # Set color based on reform type
        if reform == "Current Law":
            color = DARK_GRAY
        elif reform == "Current Policy":
            color = LIGHT_GRAY
        else:
            # Assign different shades of blue to custom reforms
            color = BLUE_SHADES[reform_counter % len(BLUE_SHADES)]
            reform_counter += 1

        # Add bar with black text for reform names
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

        # Add difference annotation in matching bar color for non-baseline reforms
        if reform != "Current Law":
            fig.add_annotation(
                y=reform,
                x=value,
                text=text_outside,
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                xshift=5,
                font=dict(size=16, color=color),  # Match the bar color
            )

    # Update layout without specifying text colors
    fig.update_layout(
        title=dict(
            text="Household Income by Reform",
            font=dict(size=24),  # Remove color to inherit from theme
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
