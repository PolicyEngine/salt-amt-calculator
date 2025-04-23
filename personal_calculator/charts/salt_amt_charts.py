import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from policyengine_core.charts import format_fig
from constants import BLUE, DARK_GRAY
from personal_calculator.dataframes.dataframes import (
    calculate_property_tax_df,
    calculate_effective_salt_cap_over_earnings,
    process_effective_cap_data,
    calculate_income_df,
    create_max_salt_dataset,
    process_effective_cap_over_property_tax_data,
)
from personal_calculator.dataframes.situations import (
    create_situation_with_one_property_tax_axes,
    create_situation_with_one_income_axes,
    create_situation_with_two_axes,
)


def display_salt_deduction_comparison_chart(
    state_code,
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    employment_income=0,
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
    current_law_df = calculate_property_tax_df(
        state_code=state_code,
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
        state_code=state_code,
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
                name="Current Law (2026)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["salt_deduction"],
                mode="lines",
                name="Current Policy (2025)",
                line=dict(color="#777777", width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Effective SALT Cap by Income Level ({state_code})",
        title_font_size=16,
        xaxis_title="Employment Income ($)",
        yaxis_title="Effective SALT Cap ($)",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
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


def display_salt_cap_comparison_chart(
    state_code,
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    threshold=0.1,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_effective_salt_cap_over_earnings(
        state_code=state_code,
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
    current_policy_df = calculate_effective_salt_cap_over_earnings(
        state_code=state_code,
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

    # Process data to calculate marginal rates
    processed_law_df = process_effective_cap_data(current_law_df)
    processed_policy_df = process_effective_cap_data(current_policy_df)

    # Create a combined figure
    fig = go.Figure()

    # Add Current Law line
    law_max_salt = create_max_salt_dataset(processed_law_df, threshold)
    if not law_max_salt.empty:
        fig.add_trace(
            go.Scatter(
                x=law_max_salt["employment_income"],
                y=law_max_salt["salt_and_property_tax"],
                mode="lines",
                name="Current Law (2026)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Add Current Policy line
    policy_max_salt = create_max_salt_dataset(processed_policy_df, threshold)
    if not policy_max_salt.empty:
        fig.add_trace(
            go.Scatter(
                x=policy_max_salt["employment_income"],
                y=policy_max_salt["salt_and_property_tax"],
                mode="lines",
                name="Current Policy (2025)",
                line=dict(color="#777777", width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Effective SALT Cap by Income Level ({state_code})",
        title_font_size=16,
        xaxis_title="Employment Income ($)",
        yaxis_title="Effective SALT Cap ($)",
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
            range=[0, 200000],  # Adjust as needed to show your data
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
        - The marginal subsidy rate is computed in $500 increments of property taxes
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
    state_code,
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
        state_code,
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
    state_code,
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
    result_df = create_situation_with_one_property_tax_axes(
        state_code,
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        employment_income,
        baseline_scenario="Current Law",
        reform_params=reform_params,
    )

    # Process the data to calculate marginal rates
    processed_df = process_effective_cap_over_property_tax_data(result_df)

    # Find the effective cap (maximum SALT where marginal rate > threshold)
    filtered_df = processed_df[processed_df["marginal_property_tax_rate"] > threshold]

    if not filtered_df.empty:
        effective_cap = filtered_df["salt_and_property_tax"].max()
        has_cap = True
    else:
        effective_cap = float("inf")
        has_cap = False

    # Format the cap value (round to nearest 100)
    def format_cap(cap_value):
        if cap_value == float("inf"):
            return None
        else:
            # Round to nearest 100
            rounded_cap = round(cap_value / 100) * 100
            return f"${rounded_cap:,.0f}"

    # Get formatted value for display
    cap_display = format_cap(effective_cap)

    # Display the effective cap message
    st.markdown(
        f"""
        <div style="text-align: center; margin: 5px 0;">
            <h3 style="color: #777777;">Your household faces {f'an effective SALT cap of <span style="color: {BLUE}; font-weight: bold;">{cap_display}</span>' if has_cap else 'no effective SALT cap'} under {policy}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return effective_cap


def display_regular_tax_and_amt_chart(
    state_code,
    is_married=False,
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
):
    """
    Create and display a chart showing regular tax and AMT by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and tax amounts on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        state_code=state_code,
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
        state_code=state_code,
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
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
            )
        )

    # Add Current Policy lines
    if not current_policy_df.empty:
        # Regular tax under current policy (solid gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["regular_tax"],
                mode="lines",
                name="Regular Tax (Current Policy)",
                line=dict(color=DARK_GRAY, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
            )
        )
        # AMT under current policy (dotted gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["amt"],
                mode="lines",
                name="AMT (Current Policy)",
                line=dict(color=DARK_GRAY, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Regular Tax and AMT by Income Level ({state_code})",
        title_font_size=16,
        xaxis_title="Employment Income ($)",
        yaxis_title="Tax Amount ($)",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],  # Adjust as needed to show your data
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
    state_code,
    is_married=False,
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
):
    """
    Create and display a chart showing regular tax and AMT by income level,
    comparing current policy vs current law.

    Parameters match those used in calculate_effective_salt_cap_over_earnings.

    The graph shows employment income on x-axis and tax amounts on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        state_code=state_code,
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
        state_code=state_code,
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

    # Add Current Law lines
    if not current_law_df.empty:
        # Regular tax under current law (solid blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["taxable_income"],
                mode="lines",
                name="Regular Tax (Current Law)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
            )
        )
        # AMT under current law (dotted blue)
        fig.add_trace(
            go.Scatter(
                x=current_law_df["salt_and_property_tax"],
                y=current_law_df["amt_income"],
                mode="lines",
                name="AMT (Current Law)",
                line=dict(color=BLUE, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
            )
        )

    # Add Current Policy lines
    if not current_policy_df.empty:
        # Regular tax under current policy (solid gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["taxable_income"],
                mode="lines",
                name="Regular Tax (Current Policy)",
                line=dict(color=DARK_GRAY, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
            )
        )
        # AMT under current policy (dotted gray)
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["amt_income"],
                mode="lines",
                name="AMT (Current Policy)",
                line=dict(color=DARK_GRAY, width=2, dash="dot"),
                hovertemplate="Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Taxable Income and AMTI by SALT ({state_code})",
        title_font_size=16,
        xaxis_title="SALT ($)",
        yaxis_title="Taxable Income ($)",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
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
    state_code,
    is_married=False,
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    employment_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    threshold=0.1,
):
    """
    Create and display a chart showing effective SALT cap by income level,
    comparing current policy vs current law.


    The graph shows employment income on x-axis and effective SALT cap on y-axis.
    """
    # Calculate data for Current Law
    current_law_df = calculate_property_tax_df(
        state_code=state_code,
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
        state_code=state_code,
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
                name="Current Law (2026)",
                line=dict(color=BLUE, width=2),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Add Current Policy line
    if not current_policy_df.empty:
        fig.add_trace(
            go.Scatter(
                x=current_policy_df["salt_and_property_tax"],
                y=current_policy_df["income_tax"],
                mode="lines",
                name="Current Policy (2025)",
                line=dict(color="#777777", width=2, dash="dash"),
                hovertemplate="Income: $%{x:,.0f}<br>SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title=f"Income Tax by SALT ({state_code})",
        title_font_size=16,
        xaxis_title="SALT ($)",
        yaxis_title="Income Tax ($)",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 150000],
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
            hovertemplate="Income: $%{x:,.0f}<br>SALT: $%{y:,.0f}<extra></extra>",
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Effective SALT cap under {policy}",
        title_font_size=16,
        xaxis_title="Employment Income ($)",
        yaxis_title="SALT ($)",
        xaxis=dict(
            tickformat="$,.0f",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, 1000000],
        ),
        yaxis=dict(
            tickformat="$,.0f",
            range=[0, min(y_max, max_salt_by_income["employment_income"].max() * 1.1)],
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
        ),
        margin=dict(t=100, b=100),
        hovermode="closest",
        plot_bgcolor="white",
    )

    return fig
