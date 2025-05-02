import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from policyengine_core.charts import format_fig as format_fig_


def format_fig(fig):
    return format_fig_(fig).update_layout(
        margin_r=100,
    )


from constants import BLUE, DARK_GRAY, LIGHT_GRAY
from personal_calculator.dataframes.dataframes import (
    calculate_property_tax_df,
    calculate_effective_salt_cap_over_earnings,
    process_effective_cap_data,
    calculate_income_df,
    process_income_marginal_tax_data,
    display_effective_salt_cap,
    calculate_df_without_axes,
    calculate_salt_income_tax_reduction,
)
from personal_calculator.chart import adjust_chart_limits


def display_salt_deduction_comparison_chart(
    is_married=False,
    state_code="CA",
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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
                x=current_law_df["reported_salt"],
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
                x=current_policy_df["reported_salt"],
                y=current_policy_df["salt_deduction"],
                mode="lines",
                name="Current Policy ",
                line=dict(color=LIGHT_GRAY, width=2, dash="solid"),
                hovertemplate="SALT: $%{x:,.0f}<br>Current Policy SALT Deduction: $%{y:,.0f}<extra></extra>",
                zorder=1,
                visible=show_current_policy,
            )
        )

    # Update layout
    fig.update_layout(
        title="",
        title_font_size=16,
        xaxis_title="Reported SALT ",
        yaxis_title="SALT Deduction (2026) ",
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

    fig.update_layout(
        xaxis_range=[0, 100_000],
    )
    user_values_law = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Law",
        reform_params=None,
    )

    # Then calculate the same values for Current Policy
    user_values_policy = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Policy",
        reform_params=None,
    )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["salt_deduction"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>SALT Deduction: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["salt_deduction"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>SALT Deduction: $%{y:,.0f}<extra></extra>",
                visible=show_current_policy,  # Only show if Current Policy is shown
            )
        )

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
    state_code,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    employment_income,  # Add this parameter
    policy=None,
    reform_params=None,
    threshold=0.1,
):
    """Display the effective SALT cap graph using the two axes situation"""

    # Calculate for two axes (varying employment income)
    result_df = calculate_effective_salt_cap_over_earnings(
        is_married,
        state_code,
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

    # Calculate the user's effective SALT cap
    user_salt_data = calculate_salt_income_tax_reduction(
        is_married,
        state_code,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        employment_income,
        baseline_scenario=policy,
        reform_params=reform_params,
        threshold=threshold,
    )

    # Create user data dictionary
    user_data = {
        "employment_income": employment_income,
        "effective_salt_cap": (
            user_salt_data["effective_salt_cap"]
            if not user_salt_data["indefinite_reduction"]
            else float("inf")
        ),
    }

    # Create the graph with user data
    fig = create_max_salt_line_graph(
        processed_df, policy=policy, threshold=threshold, user_data=user_data
    )

    adjust_chart_limits(fig)

    fig.update_layout(
        yaxis_title="Effective SALT cap (2026) ",
    )
    fig.update_layout(
        xaxis_range=[0, 1_000_000],
        xaxis_title="Wages and salaries",
    )

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return processed_df


def display_regular_tax_and_amt_chart(
    is_married=False,
    state_code="CA",
    num_children=0,
    child_ages=[],
    employment_income=0,
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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
                x=current_policy_df["reported_salt"],
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
                x=current_policy_df["reported_salt"],
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
                x=current_law_df["reported_salt"],
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
                x=current_law_df["reported_salt"],
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
        title="",
        title_font_size=16,
        xaxis_title="Reported SALT ",
        yaxis_title="Tax Amount (2026) ",
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

    user_values_law = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Law",
        reform_params=None,
    )

    # Then calculate the same values for Current Policy
    user_values_policy = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Policy",
        reform_params=None,
    )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["regular_tax"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["regular_tax"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["amt"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["amt"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Format the chart
    fig = format_fig(fig)

    adjust_chart_limits(fig)
    fig.update_layout(
        xaxis_range=[0, 100_000],
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_taxable_income_and_amti_chart(
    is_married=False,
    state_code="CA",
    num_children=0,
    child_ages=[],
    employment_income=0,
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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
                x=current_policy_df["reported_salt"],
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
                x=current_policy_df["reported_salt"],
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
                x=current_law_df["reported_salt"],
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
                x=current_law_df["reported_salt"],
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
        title="",
        title_font_size=16,
        xaxis_title="Reported SALT ",
        yaxis_title="Taxable Income (2026) ",
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

    user_values_law = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Law",
        reform_params=None,
    )

    # Then calculate the same values for Current Policy
    user_values_policy = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Policy",
        reform_params=None,
    )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["taxable_income"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["taxable_income"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>Taxable Income: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["amt_income"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["amt_income"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>AMTI: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Format the chart
    fig = format_fig(fig)

    adjust_chart_limits(fig)
    fig.update_layout(
        xaxis_range=[0, 100_000],
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_income_tax_chart(
    is_married=False,
    state_code="CA",
    num_children=0,
    child_ages=[],
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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
                x=current_law_df["reported_salt"],
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
                x=current_policy_df["reported_salt"],
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
        title="",
        title_font_size=16,
        xaxis_title="Reported SALT ",
        yaxis_title="Income Tax (2026) ",
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

    user_values_law = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Law",
        reform_params=None,
    )

    # Then calculate the same values for Current Policy
    user_values_policy = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        employment_income=employment_income,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        scenario="Current Policy",
        reform_params=None,
    )

    fig.add_trace(
        go.Scatter(
            x=[user_values_law["reported_salt"]],
            y=[user_values_law["federal_income_tax"]],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>SALT: $%{x:,.0f}<br>Federal Income Tax: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_values_policy["reported_salt"]],
                y=[user_values_policy["federal_income_tax"]],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>SALT: $%{x:,.0f}<br>Federal Income Tax: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Format the chart
    fig = format_fig(fig)

    adjust_chart_limits(fig)
    fig.update_layout(
        xaxis_range=[0, 100_000],
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def create_max_salt_line_graph(
    df, policy="Current Law", threshold=0.1, y_max=150000, user_data=None
):
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
    user_data : dict, optional
        Dictionary containing user's household data with 'employment_income' and 'effective_salt_cap'
    """
    # Filter to only include the specified policy
    df_filtered = df[df["policy"] == policy]

    # Filter data where marginal_property_tax_rate > threshold
    state_data = df_filtered[df_filtered["marginal_property_tax_rate"] > threshold]

    # Sort by employment income for line plotting
    state_data = state_data.sort_values("employment_income")

    # For each unique employment income, find the maximum SALT value
    max_salt_by_income = (
        state_data.groupby("employment_income")["reported_salt"].max().reset_index()
    )

    # Sort by income for proper line plotting
    max_salt_by_income = max_salt_by_income.sort_values("employment_income")

    # Create figure
    fig = go.Figure()

    # Add line trace
    fig.add_trace(
        go.Scatter(
            x=max_salt_by_income["employment_income"],
            y=max_salt_by_income["reported_salt"],
            mode="lines",
            line=dict(color=BLUE, width=1.5),
            name="Effective SALT Cap",
            hovertemplate="Effective SALT Cap at<br>Income: $%{x:,.0f}<br>SALT: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add user's household data point if provided
    if user_data is not None:
        fig.add_trace(
            go.Scatter(
                x=[user_data["employment_income"]],
                y=[user_data["effective_salt_cap"]],
                mode="markers",
                name="Your household",
                marker=dict(color=BLUE, size=10, symbol="circle"),
                hovertemplate="Your household<br>Income: $%{x:,.0f}<br>Effective SALT Cap: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title="",
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


def display_gap_chart(
    is_married=False,
    num_children=0,
    state_code="CA",
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    employment_income=0,
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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

    # Find the closest point in the dataframe to the user's income
    # This ensures the dot falls exactly on the line
    def find_closest_value(df, income):
        idx = (df["employment_income"] - income).abs().idxmin()
        return df.loc[idx]["employment_income"], df.loc[idx]["gap"]

    # Get exact points from the precalculated lines
    user_income_law, user_gap_law = find_closest_value(
        current_law_df, employment_income
    )
    user_income_policy, user_gap_policy = find_closest_value(
        current_policy_df, employment_income
    )

    # Add user's point for Current Law
    fig.add_trace(
        go.Scatter(
            x=[user_income_law],
            y=[user_gap_law],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add user's point for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_income_policy],
                y=[user_gap_policy],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>Income: $%{x:,.0f}<br>Gap: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Update layout
    fig.update_layout(
        title="",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Gap between Regular Tax and AMT (assuming no SALT)",
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
    fig.update_layout(
        xaxis_range=[0, 1_000_000],
        xaxis_title="Wages and salaries",
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_marginal_rate_chart(
    is_married=False,
    state_code="CA",
    num_children=0,
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    short_term_capital_gains=0,
    deductible_mortgage_interest=0,
    charitable_cash_donations=0,
    employment_income=0,  # Add this parameter
    real_estate_taxes=0,  # Add this parameter
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
        state_code=state_code,
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
        state_code=state_code,
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

    # Find the marginal tax rate for the user's income in the current_law_marginal_df
    user_income = employment_income
    # Find the closest income value in the dataframe
    closest_income_idx = (
        (current_law_marginal_df["employment_income"] - user_income).abs().idxmin()
    )
    user_marginal_rate_law = current_law_marginal_df.loc[
        closest_income_idx, "marginal_tax_rate"
    ]

    # Do the same for current policy
    closest_income_idx_policy = (
        (current_policy_marginal_df["employment_income"] - user_income).abs().idxmin()
    )
    user_marginal_rate_policy = current_policy_marginal_df.loc[
        closest_income_idx_policy, "marginal_tax_rate"
    ]

    # Add user's point for Current Law
    fig.add_trace(
        go.Scatter(
            x=[user_income],
            y=[user_marginal_rate_law],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>Income: $%{x:,.0f}<br>Marginal Tax Rate: %{y:.1%}<extra></extra>",
        )
    )

    # Add user's point for Current Policy (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_income],
                y=[user_marginal_rate_policy],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>Income: $%{x:,.0f}<br>Marginal Tax Rate: %{y:.1%}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Update layout
    fig.update_layout(
        title="",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Marginal Tax Rate (2026) ",
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
    fig.update_layout(
        xaxis_range=[0, 1_000_000],
        yaxis_range=[0, 1],
        xaxis_title="Wages and salaries",
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def display_regular_tax_and_amt_by_income_chart(
    is_married=False,
    num_children=0,
    state_code="CA",
    child_ages=[],
    qualified_dividend_income=0,
    long_term_capital_gains=0,
    employment_income=0,
    real_estate_taxes=0,
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
        state_code=state_code,
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
        state_code=state_code,
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
        title="",
        title_font_size=16,
        xaxis_title="Income",
        yaxis_title="Tax Amount (assuming no SALT, 2026)",
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

    # Find the closest point in the dataframe to the user's income for current law
    def find_closest_value(df, income, column):
        idx = (df["employment_income"] - income).abs().idxmin()
        return df.loc[idx]["employment_income"], df.loc[idx][column]

    # Get exact points from the regular tax line for current law
    user_income_law_regular, user_regular_tax_law = find_closest_value(
        current_law_df, employment_income, "regular_tax"
    )
    # Get exact points from the AMT line for current law
    user_income_law_amt, user_amt_law = find_closest_value(
        current_law_df, employment_income, "amt"
    )

    # Get exact points from the regular tax line for current policy
    user_income_policy_regular, user_regular_tax_policy = find_closest_value(
        current_policy_df, employment_income, "regular_tax"
    )
    # Get exact points from the AMT line for current policy
    user_income_policy_amt, user_amt_policy = find_closest_value(
        current_policy_df, employment_income, "amt"
    )

    # Add user's point for Current Law Regular Tax
    fig.add_trace(
        go.Scatter(
            x=[user_income_law_regular],
            y=[user_regular_tax_law],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>Employment Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy Regular Tax (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_income_policy_regular],
                y=[user_regular_tax_policy],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>Employment Income: $%{x:,.0f}<br>Regular Tax: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Add user's point for Current Law AMT
    fig.add_trace(
        go.Scatter(
            x=[user_income_law_amt],
            y=[user_amt_law],
            mode="markers",
            name="Your household (Current Law)",
            marker=dict(color=BLUE, size=10, symbol="circle"),
            hovertemplate="Your household (Current Law)<br>Employment Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
        )
    )

    # Add dot for Current Policy AMT (only if Current Policy is shown)
    if show_current_policy:
        fig.add_trace(
            go.Scatter(
                x=[user_income_policy_amt],
                y=[user_amt_policy],
                mode="markers",
                name="Your household (Current Policy)",
                marker=dict(color=LIGHT_GRAY, size=10, symbol="circle"),
                hovertemplate="Your household (Current Policy)<br>Employment Income: $%{x:,.0f}<br>AMT: $%{y:,.0f}<extra></extra>",
                visible="legendonly",  # Only show if Current Policy is shown
            )
        )

    # Format the chart
    fig = format_fig(fig)

    adjust_chart_limits(fig)
    fig.update_layout(
        xaxis_range=[0, 1_000_000],
        xaxis_title="Wages and salaries",
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def create_tax_savings_line_graph(df, policy="Current Law", user_data=None):
    """
    Create a line graph showing tax savings by income level for a specific policy.

    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the tax savings data
    policy : str
        Policy type (default: 'Current Law')
    user_data : dict, optional
        Dictionary containing user's household data with 'employment_income' and 'tax_savings'
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

    # Add user's household data point if provided
    if user_data is not None:
        fig.add_trace(
            go.Scatter(
                x=[user_data["employment_income"]],
                y=[user_data["tax_savings"]],
                mode="markers",
                name="Your household",
                marker=dict(color=BLUE, size=10, symbol="circle"),
                hovertemplate="Your household<br>Income: $%{x:,.0f}<br>Tax Savings: $%{y:,.0f}<extra></extra>",
            )
        )

    # Update layout
    fig.update_layout(
        title="",
        title_font_size=16,
        xaxis_title="Wages and salaries",
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
    state_code,
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
    """Display the tax savings chart showing the difference between income tax at 0 SALT and income tax at effective SALT cap"""

    # Calculate for two axes (varying employment income)
    result_df = calculate_effective_salt_cap_over_earnings(
        is_married,
        state_code,
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
        # Find income tax at 0 SALT (minimum reported_salt)
        min_salt_row = group.loc[group["reported_salt"].idxmin()]
        income_tax_at_zero_salt = min_salt_row["income_tax"]

        # Find the effective SALT cap (where marginal_property_tax_rate > threshold)
        effective_cap_group = group[group["marginal_property_tax_rate"] > threshold]

        if not effective_cap_group.empty:
            # Get the maximum SALT value where marginal rate exceeds threshold
            effective_cap = effective_cap_group["reported_salt"].max()

            # Find the row with the effective SALT cap
            effective_cap_row = group[group["reported_salt"] == effective_cap].iloc[0]
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

    # Find the closest point in the dataframe to the user's income
    def find_closest_value(df, income):
        if df.empty:
            return income, 0
        idx = (df["employment_income"] - income).abs().idxmin()
        return df.loc[idx]["employment_income"], df.loc[idx]["tax_savings"]

    # Get exact point from the pre-calculated line
    user_income, user_tax_savings = find_closest_value(
        tax_savings_df, employment_income
    )

    # Create user data dictionary using the point from the line
    user_data = {
        "employment_income": user_income,
        "tax_savings": user_tax_savings,
    }

    # Create the graph with user data
    fig = create_tax_savings_line_graph(
        tax_savings_df, policy=policy, user_data=user_data
    )

    adjust_chart_limits(fig)
    fig.update_layout(
        xaxis_range=[0, 1_000_000],
        xaxis_title="Wages and salaries",
    )

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return tax_savings_df


def display_sales_or_income_tax_table(
    state_code,
    real_estate_taxes,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    employment_income,
    reform_params=None,
):
    """Compare Current Law and Current Policy scenarios with simplified output"""
    # Calculate both scenarios
    current_law_results = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        employment_income=employment_income,
        scenario="Current Law",
        reform_params=None,
    )

    current_policy_results = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        is_married=is_married,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        employment_income=employment_income,
        scenario="Current Policy",
        reform_params=None,
    )

    # Determine which tax type is larger and create appropriate label
    state_tax_type = (
        "State Income Tax"
        if current_law_results["state_income_tax_over_sales_tax"]
        else "State Sales Tax"
    )
    state_tax_value = current_law_results["larger_of_state_sales_or_income_tax"]
    total_salt = state_tax_value + real_estate_taxes

    # Create simplified comparison DataFrame with formatted values
    comparison_data = {
        "Metric": [state_tax_type, "Property Taxes", "Total SALT"],
        "Current Law": [
            f"${state_tax_value:,.0f}",
            f"${real_estate_taxes:,.0f}",
            f"${total_salt:,.0f}",
        ],
    }

    df = pd.DataFrame(comparison_data)
    return df.set_index("Metric")
