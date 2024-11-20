import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Define colors
DARK_GRAY = "#4A4A4A"
LIGHT_GRAY = "#7C7C7C"
REFORM_BLUE = "#2C6BFF"


def format_fig(fig):
    """Apply PolicyEngine styling to a Plotly figure"""
    fig.update_layout(
        font_family="Roboto",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        bargap=0.2,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        showlegend=False,
        xaxis=dict(
            title=None,
            tickformat="$,.0f",
            tickfont=dict(size=14),
            gridcolor="lightgray",
            zerolinecolor="lightgray",
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=18),
        ),
    )
    return fig


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
            color = REFORM_BLUE

        # Add bar
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

        # Add difference annotation for non-baseline reforms
        if reform != "Current Law":
            fig.add_annotation(
                y=reform,
                x=value,
                text=text_outside,
                showarrow=False,
                xanchor="left",
                yanchor="middle",
                xshift=5,
                font=dict(size=16),
            )

    # Update layout
    fig.update_layout(
        title=dict(
            text="Household Income by Reform",
            font=dict(size=24),
        ),
    )

    # Apply PolicyEngine formatting
    fig = format_fig(fig)

    return fig


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
