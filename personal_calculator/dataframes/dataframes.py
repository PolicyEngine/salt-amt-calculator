import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import PolicyReforms
from constants import BLUE, DARK_GRAY
from personal_calculator.dataframes.situations import (
    create_situation_with_one_property_tax_axes,
    create_situation_with_one_income_axes,
    create_situation_with_two_axes,
    create_situation_without_axes
)


@st.cache_data(show_spinner="Calculating...")
def calculate_property_tax_df(
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
    reform_params,
    baseline_scenario,
):
    """
    Calculate effective SALT cap for a single axis situation (fixed employment income)
    """
    # Create situation with employment income fixed
    situation = create_situation_with_one_property_tax_axes(
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
        baseline_scenario,
        reform_params,
    )

    # Create simulation based on baseline scenario
    if baseline_scenario == "Current Law":
        simulation = Simulation(situation=situation)
    elif baseline_scenario == "Current Policy":
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    elif reform_params:
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid scenario configuration")

    # Calculate values along the axis
    reported_salt = simulation.calculate(
        "reported_salt", map_to="household", period=2026
    )

    regular_tax = simulation.calculate(
        "regular_tax_before_credits", map_to="household", period=2026
    )
    amt = simulation.calculate("amt_base_tax", map_to="household", period=2026)
    salt_deduction = simulation.calculate(
        "salt_deduction", map_to="household", period=2026
    )
    sales_or_income_tax = simulation.calculate(
        "state_and_local_sales_or_income_tax", map_to="household", period=2026
    )
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate(
        "taxable_income", map_to="household", period=2026
    )
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    # Create DataFrame with data
    property_tax_df = pd.DataFrame(
        {
            "employment_income": employment_income,
            "reported_salt": reported_salt,
            "regular_tax": regular_tax,
            "amt": amt,
            "salt_deduction": salt_deduction,
            "sales_or_income_tax": sales_or_income_tax,
            "amt_binds": amt > regular_tax,
            "income_tax": income_tax,
            "taxable_income": taxable_income,
            "amt_income": amt_income,
        }
    )

    # Add policy information
    property_tax_df["policy"] = baseline_scenario if reform_params is None else "Reform"

    return property_tax_df


@st.cache_data(show_spinner="Calculating...")
def calculate_income_df(
    is_married,
    state_code,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    reform_params,
    baseline_scenario,
):
    """
    Calculate effective SALT cap for a single axis situation (fixed employment income)
    """
    # Create situation with employment income fixed
    situation = create_situation_with_one_income_axes(
        is_married,
        state_code,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
    )

    # Create simulation based on baseline scenario
    if baseline_scenario == "Current Law":
        simulation = Simulation(situation=situation)
    elif baseline_scenario == "Current Policy":
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    elif reform_params:
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid scenario configuration")

    # Calculate values along the axis
    employment_income = simulation.calculate(
        "employment_income", map_to="household", period=2026
    )

    regular_tax = simulation.calculate(
        "regular_tax_before_credits", map_to="household", period=2026
    )
    amt = simulation.calculate("amt_base_tax", map_to="household", period=2026)
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    # Create DataFrame with data
    income_df = pd.DataFrame(
        {
            "employment_income": employment_income,
            "regular_tax": regular_tax,
            "amt": amt,
            "gap": np.maximum(regular_tax - amt, 0),
            "income_tax": income_tax,
        }
    )

    # Add policy information
    income_df["policy"] = baseline_scenario if reform_params is None else "Reform"

    return income_df


@st.cache_data(show_spinner="Calculating...")
def calculate_effective_salt_cap_over_earnings(
    is_married,
    state_code,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    reform_params=None,
    baseline_scenario="Current Law",
):
    """
    Calculate effective SALT cap for varying property tax and income levels
    """
    # Create situation with two axes
    situation = create_situation_with_two_axes(
        is_married,
        state_code,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
    )

    # Create simulation based on baseline scenario
    if baseline_scenario == "Current Law":
        simulation = Simulation(situation=situation)
    elif baseline_scenario == "Current Policy":
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    elif reform_params:
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid scenario configuration")

    # Calculate values along the axes
    employment_income_axis = simulation.calculate(
        "employment_income", map_to="household", period=2026
    )
    reported_salt_axis = simulation.calculate(
        "reported_salt", map_to="household", period=2026
    )

    regular_tax = simulation.calculate(
        "regular_tax_before_credits", map_to="household", period=2026
    )
    amt = simulation.calculate("amt_base_tax", map_to="household", period=2026)
    salt_deduction = simulation.calculate(
        "salt_deduction", map_to="household", period=2026
    )
    sales_or_income_tax = simulation.calculate(
        "state_and_local_sales_or_income_tax", map_to="household", period=2026
    )
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate(
        "taxable_income", map_to="household", period=2026
    )
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    # Create DataFrame with data
    effective_caps_over_earnings = pd.DataFrame(
        {
            "employment_income": employment_income_axis,
            "reported_salt": reported_salt_axis,
            "regular_tax": regular_tax,
            "amt": amt,
            "salt_deduction": salt_deduction,
            "sales_or_income_tax": sales_or_income_tax,
            "amt_binds": amt > regular_tax,
            "income_tax": income_tax,
            "taxable_income": taxable_income,
            "amt_income": amt_income,
        }
    )

    # Add policy information
    effective_caps_over_earnings["policy"] = (
        baseline_scenario if reform_params is None else "Reform"
    )

    return effective_caps_over_earnings


def calculate_marginal_rate(group):
    """
    Calculate the marginal property tax rate for a group.
    If the group is already sorted by property_tax, simply calculate the rate.
    Otherwise, sort the group first.
    """
    # Check if group needs sorting
    needs_sorting = False
    if (
        isinstance(group, pd.DataFrame)
        and not group["reported_salt"].is_monotonic_increasing
    ):
        needs_sorting = True
        group = group.sort_values("reported_salt")

    # Calculate differences in income tax and property tax
    group["income_tax_diff"] = group["income_tax"].diff()
    group["reported_salt_diff"] = group["reported_salt"].diff()

    # Calculate the marginal rate (change in income tax / change in property tax)
    group["marginal_property_tax_rate"] = (
        -group["income_tax_diff"] / group["reported_salt_diff"]
    )

    # Handle edge cases (divide by zero, first row in group)
    group["marginal_property_tax_rate"] = group["marginal_property_tax_rate"].replace(
        [np.inf, -np.inf, np.nan], 0
    )

    # If we sorted the group, restore the original order
    if needs_sorting and "original_index" in group.columns:
        group = group.sort_values("original_index").drop("original_index", axis=1)

    return group


def process_effective_cap_data(effective_cap_df):
    """
    Process the effective cap data by calculating marginal rates for each income level
    """
    # Sort the dataframe
    processed_df = effective_cap_df.sort_values(
        by=["policy", "employment_income", "reported_salt"]
    )

    # Calculate the marginal property tax rate for each income level
    processed_df = (
        processed_df.groupby(["policy", "employment_income"])
        .apply(calculate_marginal_rate)
        .reset_index(drop=True)
    )

    return processed_df


def process_effective_cap_over_property_tax_data(effective_cap_df):
    """
    Process the effective cap data by calculating marginal rates for each income level
    """
    # Sort the dataframe
    # processed_df = effective_cap_df.sort_values(by=["policy", "employment_income"])

    # Calculate the marginal property tax rate for each income level
    effective_cap_df = (
        effective_cap_df.groupby(["policy", "employment_income"])
        .apply(calculate_marginal_rate)
        .reset_index(drop=True)
    )

    return effective_cap_df


def create_max_salt_dataset(df, threshold=0.1):
    """
    Create a dataset with values at each income level where
    the marginal property tax rate exceeds the threshold.

    Parameters:
    -----------
    df : pandas DataFrame
        Processed dataframe with marginal_property_tax_rate calculated
    threshold : float
        Threshold value for marginal_property_tax_rate

    Returns:
    --------
    pandas DataFrame
        DataFrame with values by income level for various metrics
    """
    # Filter to data where marginal rate exceeds threshold
    filtered_df = df[df["marginal_property_tax_rate"] > threshold]

    if filtered_df.empty:
        return pd.DataFrame()

    # Group by income level
    grouped = filtered_df.groupby("employment_income")

    # Get the index of maximum reported_salt for each income level
    idx_max = grouped["reported_salt"].idxmax()

    # Use these indices to get the corresponding rows
    # Include all columns needed for all four charts
    columns_to_keep = [
        "employment_income",
        "salt_deduction",
        "reported_salt",
        "regular_tax",
        "amt",
        "taxable_income",
        "amt_income",
        "income_tax",
    ]

    # Create DataFrame with only the columns we need
    max_salt_by_income = filtered_df.loc[idx_max][columns_to_keep]

    # Sort by income for proper plotting
    max_salt_by_income = max_salt_by_income.sort_values("employment_income")

    return max_salt_by_income


def create_values_by_income_dataset(df, threshold=0.1):
    """
    Create a dataset with values at each income level where
    the marginal property tax rate exceeds the threshold.

    Parameters:
    -----------
    df : pandas DataFrame
        Processed dataframe with marginal_property_tax_rate calculated
    threshold : float
        Threshold value for marginal_property_tax_rate

    Returns:
    --------
    pandas DataFrame
        DataFrame with values by income level for various metrics
    """
    # Filter to data where marginal rate exceeds threshold
    filtered_df = df[df["marginal_property_tax_rate"] > threshold]

    if filtered_df.empty:
        return pd.DataFrame()

    # Group by income level
    grouped = filtered_df.groupby("employment_income")

    # Get the index of maximum reported_salt for each income level
    idx_max = grouped["reported_salt"].idxmax()

    # Use these indices to get the corresponding rows
    # Include all columns needed for all four charts
    columns_to_keep = [
        "employment_income",
        "salt_deduction",
        "reported_salt",
        "regular_tax",
        "amt",
        "taxable_income",
        "amt_income",
        "income_tax",
    ]

    # Create DataFrame with only the columns we need
    max_salt_by_income = filtered_df.loc[idx_max][columns_to_keep]

    # Sort by income for proper plotting
    max_salt_by_income = max_salt_by_income.sort_values("employment_income")

    return max_salt_by_income


def calculate_marginal_tax_rate_by_income(
    df, tax_column="regular_tax", income_column="employment_income"
):
    """
    Calculate the marginal tax rate based on income increments.

    Parameters:
    -----------
    df : pandas DataFrame
        DataFrame containing tax and income data
    tax_column : str
        Column name for the tax value to calculate marginal rate for
    income_column : str
        Column name for the income value

    Returns:
    --------
    pandas DataFrame
        DataFrame with added marginal_tax_rate column
    """
    # Make a copy to avoid modifying the original
    result_df = df.copy()

    # Sort by income to ensure proper calculation
    result_df = result_df.sort_values(by=income_column)

    # Calculate the difference in tax values
    result_df["tax_diff"] = result_df[tax_column].diff()

    # Calculate the difference in income values
    result_df["income_diff"] = result_df[income_column].diff()

    # Calculate the marginal tax rate (change in tax / change in income)
    result_df["marginal_tax_rate"] = result_df["tax_diff"] / result_df["income_diff"]

    # Handle edge cases (divide by zero, first row)
    result_df["marginal_tax_rate"] = result_df["marginal_tax_rate"].replace(
        [np.inf, -np.inf, np.nan], 0
    )

    # Drop the temporary columns
    result_df = result_df.drop(["tax_diff", "income_diff"], axis=1)

    return result_df


def process_income_marginal_tax_data(income_df):
    """
    Process the income data by calculating marginal tax rates for each income level

    Parameters:
    -----------
    income_df : pandas DataFrame
        DataFrame containing income and tax data

    Returns:
    --------
    pandas DataFrame
        DataFrame with added marginal_tax_rate column
    """
    # Sort the dataframe
    processed_df = income_df.sort_values(by=["policy", "employment_income"])

    # Calculate the marginal tax rate for each policy
    processed_df = (
        processed_df.groupby("policy")
        .apply(calculate_marginal_tax_rate_by_income)
        .reset_index(drop=True)
    )

    return processed_df


def calculate_salt_income_tax_reduction(
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
    reform_params=None,
    baseline_scenario="Current Law",
    threshold=0.1,
):
    """
    Calculate the income tax reduction from SALT by comparing income tax at 0 SALT
    with income tax at the effective SALT cap.

    Returns:
    --------
    dict
        Dictionary containing:
        - income_tax_reduction: The reduction in income tax from SALT
        - effective_salt_cap: The effective SALT cap
        - indefinite_reduction: Whether SALT reduces income tax indefinitely
    """
    # Calculate property tax data
    property_tax_df = calculate_property_tax_df(
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
        reform_params=reform_params,
        baseline_scenario=baseline_scenario,
    )

    # Process the data to calculate marginal rates
    processed_df = process_effective_cap_over_property_tax_data(property_tax_df)

    # Find the effective cap (maximum SALT where marginal rate > threshold)
    filtered_df = processed_df[processed_df["marginal_property_tax_rate"] > threshold]

    if filtered_df.empty:
        # If no effective cap found, SALT reduces income tax indefinitely
        return {
            "income_tax_reduction": 0,
            "effective_salt_cap": float("inf"),
            "indefinite_reduction": True,
        }

    # Get income tax at 0 SALT (first row)
    income_tax_at_zero_salt = property_tax_df.iloc[0]["income_tax"]

    # Get income tax at effective SALT cap
    effective_salt_cap = filtered_df["reported_salt"].max()
    income_tax_at_effective_cap = property_tax_df[
        property_tax_df["reported_salt"] <= effective_salt_cap
    ].iloc[-1]["income_tax"]

    # Calculate the reduction in income tax
    income_tax_reduction = max(0, income_tax_at_zero_salt - income_tax_at_effective_cap)

    # Check if the last increment still shows a decrease
    last_increment = (
        property_tax_df.iloc[-1]["income_tax"] - property_tax_df.iloc[-2]["income_tax"]
    )
    indefinite_reduction = last_increment < 0

    return {
        "income_tax_reduction": income_tax_reduction,
        "effective_salt_cap": effective_salt_cap,
        "indefinite_reduction": indefinite_reduction,
    }


def display_effective_salt_cap(
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

    # Calculate for single axis (fixed employment income)
    current_law_df = calculate_property_tax_df(
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
        reform_params=reform_params,
        baseline_scenario="Current Law",
    )

    current_policy_df = calculate_property_tax_df(
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
        effective_cap_law = filtered_law_df["reported_salt"].max()

    else:
        effective_cap_law = float("inf")

    if not filtered_policy_df.empty:
        effective_cap_policy = filtered_policy_df["reported_salt"].max()
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

@st.cache_data(show_spinner="Calculating...")
def calculate_df_without_axes(
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
    reform_params,
    baseline_scenario,
):
    """
    Calculate effective SALT cap for a single axis situation (fixed employment income)
    If compare_scenarios is True, returns a comparison DataFrame of Current Law vs Current Policy
    """
    # Create situation with employment income fixed
    situation = create_situation_without_axes(
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
    )

    # Create simulation based on baseline scenario
    if baseline_scenario == "Current Law":
        simulation = Simulation(situation=situation)
    elif baseline_scenario == "Current Policy":
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    elif reform_params:
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        simulation = Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid scenario configuration")

    federal_income_tax = simulation.calculate(
        "income_tax", map_to="household", period=2026
    )
    state_income_tax = simulation.calculate(
        "state_withheld_income_tax", map_to="household", period=2026
    )
    state_sales_tax = simulation.calculate(
        "state_sales_tax", map_to="household", period=2026
    )
    larger_of_state_sales_or_income_tax = max(state_sales_tax, state_income_tax)
    state_income_tax_over_sales_tax = state_income_tax > state_sales_tax

    # Create DataFrame with data
    property_tax_df = pd.DataFrame(
        {
            "employment_income": employment_income,
            "federal_income_tax": federal_income_tax,
            "state_income_tax": state_income_tax,
            "state_sales_tax": state_sales_tax,
            "larger_of_state_sales_or_income_tax": larger_of_state_sales_or_income_tax,
            "state_income_tax_over_sales_tax": state_income_tax_over_sales_tax,
        }
    )

    # Add policy information
    property_tax_df["policy"] = baseline_scenario if reform_params is None else "Reform"

    # Calculate both scenarios
    current_law_df = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        employment_income=employment_income,
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

    current_policy_df = calculate_df_without_axes(
        state_code=state_code,
        real_estate_taxes=real_estate_taxes,
        employment_income=employment_income,
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

    # Create comparison DataFrame
    comparison_data = {
        "Metric": [
            "Federal Income Tax",
            "State Income Tax",
            "State Sales Tax",
        ],
        "Current Law": [
            f"${current_law_df['federal_income_tax'].iloc[0]:,.0f}",
            f"${current_law_df['state_income_tax'].iloc[0]:,.0f}",
            f"${current_law_df['state_sales_tax'].iloc[0]:,.0f}",
        ],
        "Current Policy": [
            f"${current_policy_df['federal_income_tax'].iloc[0]:,.0f}",
            f"${current_policy_df['state_income_tax'].iloc[0]:,.0f}",
            f"${current_policy_df['state_sales_tax'].iloc[0]:,.0f}",
        ]
    }

    return pd.DataFrame(comparison_data)
