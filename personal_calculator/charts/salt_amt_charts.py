import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from policyengine_core.charts import format_fig
from constants import BLUE, DARK_GRAY, LIGHT_GRAY
from personal_calculator.dataframes.dataframes import (
    calculate_property_tax_df,
    calculate_effective_salt_cap_over_earnings,
    process_effective_cap_data,
    calculate_income_df,
    create_max_salt_dataset,
    process_effective_cap_over_property_tax_data,
    process_income_marginal_tax_data,
)


def display_salt_deduction_comparison_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    employment_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.

    Parameters:
    -----------
    show_current_policy : bool
        Whether to show the Current Policy line (default: False)
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["salt_deduction"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="SALT: $%{x:,.0f}<br>Current Law SALT Deduction: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Always add Current Policy line to the legend, but control its visibility
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["salt_deduction"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
                hovertemplate="SALT: $%{x:,.0f}<br>Current Policy SALT Deduction: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"SALT Deduction by SALT",
        title_font_size=16,
        xaxis_title="SALT ",
        yaxis_title="SALT Deduction ",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 100000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 120000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_notes():
    """Display notes section at the bottom of the app"""
    st.markdown("---")  # Add a horizontal line for visual separation

    with st.expander("Notes"):
        st.markdown(
            """
        - The calculator uses tax year 2026 for all calculations excluding budget window estimates
        - All computations are performed in $500 increments.
        - We limit the computation to the federal budgetary impact due to:
          - States with AMT parameters tied to federal AMT (e.g., California)
          - States with deductions for federal tax liability (e.g., Oregon)
          - Behavioral responses
        
        **Documentation:**
        - [How we model SALT](https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview)
        - [How we model AMT](https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview)
        """
        )


def display_effective_salt_cap_graph(
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    policy=None,
    reform_params=None,
    threshold=0.1,
):
    """Display the effective SALT cap graph using the two axes situation"""

    # Calculate for two axes (varying employment income)
    result_df = calculate_effective_salt_cap_over_earnings(
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        baseline_scenario=policy,
        reform_params=reform_params,
    )

    # Process the data to calculate marginal rates
    processed_df = process_effective_cap_data(result_df)

    # Create the graph
    fig = create_max_salt_line_graph(processed_df, policy=policy, threshold=threshold)

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return processed_df


def display_effective_salt_cap(
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    employment_income,
    policy=None,
    reform_params=None,
    threshold=0.1,
):

    # Calculate for single axis (fixed employment income)
    current_law_df = calculate_property_tax_df(
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        employment_income,
        reform_params=reform_params,
        baseline_scenario="Current Law",
    )

    current_policy_df = calculate_property_tax_df(
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        employment_income,
        reform_params=reform_params,
        baseline_scenario="Current Policy",
    )

    # Process the data to calculate marginal rates
    processed_law_df = process_effective_cap_over_property_tax_data(current_law_df)
    processed_policy_df = process_effective_cap_over_property_tax_data(
        current_policy_df
    )

    # Find the effective cap (maximum SALT where marginal rate > threshold)
    filtered_law_df = processed_law_df[
        processed_law_df["marginal_property_tax_rate"] > threshold
    ]
    filtered_policy_df = processed_policy_df[
        processed_policy_df["marginal_property_tax_rate"] > threshold
    ]
    effective_cap_law = float("inf")
    effective_cap_policy = float("inf")
    if not filtered_law_df.empty:
        effective_cap_law = filtered_law_df["salt_and_property_tax"].max()

    else:
        effective_cap_law = float("inf")

    if not filtered_policy_df.empty:
        effective_cap_policy = filtered_policy_df["salt_and_property_tax"].max()
        effective_cap_policy = min(effective_cap_policy, 10000)

    # Format the cap value (round to nearest 100)
    def format_cap(cap_value):
        if cap_value == float("inf"):
            return f"\$0"
        else:
            # Round to nearest 100
            rounded_cap = round(cap_value / 100) * 100
            return f"\${rounded_cap:,.0f}"

    # Get formatted value for display
    cap_display_law = format_cap(effective_cap_law)
    cap_display_policy = format_cap(effective_cap_policy)

    # Always return both values regardless of the policy parameter
    return cap_display_law, cap_display_policy


def display_regular_tax_and_amt_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing regular tax and AMT by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and tax amounts on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Policy lines
    if not current_policy_df.empty:
        # Regular tax under current policy (solid gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["regular_tax"],
                mode="lines",
                name="Regular Tax (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )
        # AMT under current policy (dotted gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["amt"],
                mode="lines",
                name="AMT (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Add Current Law lines
    if not current_law_df.empty:
        # Regular tax under current law (solid blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["regular_tax"],
                mode="lines",
                name="Regular Tax (Current Law)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )
        # AMT under current law (dotted blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["amt"],
                mode="lines",
                name="AMT (Current Law)",
                line=dict(color=BLUE, width=2, dash="dot"),
                hovertemplate="SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Regular Tax and AMT by Income Level",
        title_font_size=16,
        xaxis_title="SALT ",
        yaxis_title="Tax Amount ",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 100000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 120000],  # Adjust as needed to show your data
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_taxable_income_and_amti_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing regular tax and AMT by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and tax amounts on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Policy lines first (so they appear in the background)
    if not current_policy_df.empty:
        # Taxable Income under current policy (solid gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["taxable_income"],
                mode="lines",
                name="Taxable Income (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2),
                hovertemplate="SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )
        # AMTI under current policy (dotted gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["amt_income"],
                mode="lines",
                name="AMTI (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2, dash="dot"),
                hovertemplate="SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Add Current Law lines last (so they appear in the foreground)
    if not current_law_df.empty:
        # Taxable Income under current law (solid blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["taxable_income"],
                mode="lines",
                name="Taxable Income (Current Law)",
                line=dict(color=BLUE, width=2),
                hovertemplate="SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )
        # AMTI under current law (dotted blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["amt_income"],
                mode="lines",
                name="AMTI (Current Law)",
                line=dict(color=BLUE, width=2, dash="dot"),
                hovertemplate="SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Taxable Income and AMTI by SALT",
        title_font_size=16,
        xaxis_title="SALT ",
        yaxis_title="Taxable Income ",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 100000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 120000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_income_tax_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    employment_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
    threshold=0.1,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_property_tax_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["income_tax"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="SALT: $%{x:,.0f}<br>Income Tax: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["income_tax"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2),
                hovertemplate="SALT: $%{x:,.0f}<br>Income Tax: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Income Tax by SALT",
        title_font_size=16,
        xaxis_title="SALT ",
        yaxis_title="Income Tax ",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 100000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 120000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def create_max_salt_line_graph(df, policy="Current Law", threshold=0.1, y_max=150000):
    """
    Create a line graph showing the maximum SALT values where marginal_property_tax_rate <= threshold
    for each employment income increment.

    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the tax data
    policy : str
        Policy type (default: 'Current Law')
    threshold : float
        Threshold for marginal_property_tax_rate to be considered uncapped (default: 0.1)
    y_max : int
        Maximum value for y-axis (default: 150000)
    """
    # Filter to only include the specified policy
    df_filtered = df[df["policy"] == policy]

    # Filter data where marginal_property_tax_rate > threshold
    state_data = df_filtered[df_filtered["marginal_property_tax_rate"] > threshold]

    # Sort by employment income for line plotting
    state_data = state_data.sort_values("employment_income")

    # For each unique employment income, find the maximum SALT value
    max_salt_by_income = (
        state_data.groupby("employment_income")["salt_and_property_tax"]
        .max()
        .reset_index()
    )

    # Sort by income for proper line plotting
    max_salt_by_income = max_salt_by_income.sort_values("employment_income")

    # Create figure
    fig = go.Figure()

    # Add line trace
    fig.add_trace(
        go.Scatter(
            x=max_salt_by_income["employment_income"],
            y=max_salt_by_income["salt_and_property_tax"],
            mode="lines",
            line=dict(color=BLUE, width=1.5),
            name="Effective SALT Cap",
            hovertemplate="Effective SALT Cap at<br>Income: $%{x:,.0f}<br>SALT: $%{y:,.0f}<extra></extra>",
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Effective SALT cap under {policy}",
        title_font_size=16,
        xaxis_title="Employment Income ",
        yaxis_title="SALT ",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            range=[0, 200000],
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
        ),
        margin=dict(t=100, b=100),
        hovermode="closest",
        plot_bgcolor="white",
    )

    return fig


def display_regular_tax_comparison_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_df["employment_income"],
                y=current_law_df["regular_tax"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["employment_income"],
                y=current_policy_df["regular_tax"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=1,
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Regular Tax by Income",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Income Tax",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 200000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_amt_comparison_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_df["employment_income"],
                y=current_law_df["amt"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["employment_income"],
                y=current_policy_df["amt"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=1,
            )
        )

    # Update layout
    fig.update_layout(
        title=f"AMT by Income",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="AMT",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 200000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_gap_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_df["employment_income"],
                y=current_law_df["gap"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["employment_income"],
                y=current_policy_df["gap"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Gap by Income",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Gap between Regular Tax and AMT",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 200000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_marginal_rate_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing marginal tax rate by income level,
    comparing current policy vs current law.

    The graph shows employment income on x-axis and marginal tax rate on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    current_law_marginal_df = process_income_marginal_tax_data(current_law_df)
    current_policy_marginal_df = process_income_marginal_tax_data(current_policy_df)

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    if not current_law_marginal_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_law_marginal_df["employment_income"],
                y=current_law_marginal_df["marginal_tax_rate"],
                mode="lines",
                name="Current Law ",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Marginal Tax Rate: %{y:.1%}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy line
    if not current_policy_marginal_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_marginal_df["employment_income"],
                y=current_policy_marginal_df["marginal_tax_rate"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>Marginal Tax Rate: %{y:.1%}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Marginal Tax Rate by Income",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Marginal Tax Rate",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat=".1%",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 0.5],  # Adjust range as needed for tax rates
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_regular_tax_and_amt_by_income_chart(
    is_married=False,
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    show_current_policy=True,
):
    """
    Create and display a chart showing regular tax and AMT by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and tax amounts on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Law",
    )

    # Calculate data for Current Policy
    current_policy_df = calculate_income_df(
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        reform_params=None,
        baseline_scenario="Current Policy",
    )

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law lines
    if not current_law_df.empty:
        # Regular Tax under current law (solid blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["employment_income"],
                y=current_law_df["regular_tax"],
                mode="lines",
                name="Regular Tax (Current Law)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )
        # AMTI under current law (dotted blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["employment_income"],
                y=current_law_df["amt"],
                mode="lines",
                name="AMT (Current Law)",
                line=dict(color=BLUE, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=2,
            )
        )

    # Add Current Policy lines
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["employment_income"],
                y=current_policy_df["regular_tax"],
                mode="lines",
                name="Regular Tax (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )
        # AMTI under current policy (dotted gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["employment_income"],
                y=current_policy_df["amt"],
                mode="lines",
                name="AMT (Current Policy)",
                line=dict(color=LIGHT_GRAY, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible="legendonly",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Regular Tax and AMT by Income",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Tax Amount",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 200000],
        ),
        margin=dict(t=80, b=80),
        hovermode="closest",
        plot_bgcolor="white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    )

    # Format the chart
    fig = format_fig(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
