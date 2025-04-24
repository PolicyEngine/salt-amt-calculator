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
    process_income_marginal_tax_data,
    display_effective_salt_cap,
)
from personal_calculator.chart import adjust_chart_limits


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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)
    
    fig.update_layout(
        yaxis_title="Effective SALT cap",
    )

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return processed_df


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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)

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

    adjust_chart_limits(fig)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def create_tax_savings_line_graph(df, policy="Current Law"):
    """
    Create a line graph showing tax savings by income level for a specific policy.

    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the tax savings data
    policy : str
        Policy type (default: 'Current Law')
    y_max : int
        Maximum value for y-axis (default: 50000)
    """
    # Filter to only include the specified policy
    df_filtered = df[df["policy"] == policy]

    # Sort by employment income for line plotting
    df_filtered = df_filtered.sort_values("employment_income")

    # Create figure
    fig = go.Figure()

    # Add line trace
    fig.add_trace(
        go.Scatter(
            x=df_filtered["employment_income"],
            y=df_filtered["tax_savings"],
            mode="lines",
            line=dict(color=BLUE, width=1.5),
            name="Tax Savings",
            hovertemplate="Income: $%{x:,.0f}<br>Tax Savings: $%{y:,.0f}<extra></extra>",
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Tax Savings from SALT under {policy}",
        title_font_size=16,
        xaxis_title="Employment Income",
        yaxis_title="Tax Savings",
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


def display_tax_savings_chart(
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
    """Display the tax savings chart showing the difference between income tax at 0 SALT and income tax at effective SALT cap"""

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

    # Group by employment income to find income tax at 0 SALT and at effective SALT cap
    tax_savings_data = []

    for income, group in processed_df.groupby("employment_income"):
        # Find income tax at 0 SALT (minimum salt_and_property_tax)
        min_salt_row = group.loc[group["salt_and_property_tax"].idxmin()]
        income_tax_at_zero_salt = min_salt_row["income_tax"]

        # Find the effective SALT cap (where marginal_property_tax_rate > threshold)
        effective_cap_group = group[group["marginal_property_tax_rate"] > threshold]

        if not effective_cap_group.empty:
            # Get the maximum SALT value where marginal rate exceeds threshold
            effective_cap = effective_cap_group["salt_and_property_tax"].max()

            # Find the row with the effective SALT cap
            effective_cap_row = group[
                group["salt_and_property_tax"] == effective_cap
            ].iloc[0]
            income_tax_at_effective_cap = effective_cap_row["income_tax"]

            # Calculate tax savings (capped at 0)
            tax_savings = max(0, income_tax_at_zero_salt - income_tax_at_effective_cap)
        else:
            # If no effective cap found, tax savings is 0
            tax_savings = 0

        tax_savings_data.append(
            {
                "employment_income": income,
                "tax_savings": tax_savings,
                "policy": group["policy"].iloc[0],
            }
        )

    # Create a new dataframe with tax savings
    tax_savings_df = pd.DataFrame(tax_savings_data)

    # Create the graph
    fig = create_tax_savings_line_graph(tax_savings_df, policy=policy)

    adjust_chart_limits(fig)

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return tax_savings_df
