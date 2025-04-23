import pandas as pd
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import PolicyReforms
from constants import BLUE, DARK_GRAY
from personal_calculator.dataframes.situations import create_situation_with_one_property_tax_axes, create_situation_with_one_income_axes, create_situation_with_two_axes



def calculate_property_tax_df(
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
    reform_params,
    baseline_scenario,
):
    """
    Calculate effective SALT cap for a single axis situation (fixed employment income)
    """
    # Create situation with employment income fixed
    situation = create_situation_with_one_property_tax_axes(
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
    property_taxes_axis = simulation.calculate(
        "real_estate_taxes", map_to="household", period=2026
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
    salt_and_property_tax = property_taxes_axis + sales_or_income_tax
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate("taxable_income", map_to="household", period=2026)
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    # Create DataFrame with data
    property_tax_df = pd.DataFrame(
        {
            "employment_income": employment_income,
            "property_tax": property_taxes_axis,
            "regular_tax": regular_tax,
            "amt": amt,
            "salt_deduction": salt_deduction,
            "sales_or_income_tax": sales_or_income_tax,
            "amt_binds": amt > regular_tax,
            "salt_and_property_tax": salt_and_property_tax,
            "income_tax": income_tax,
            "taxable_income": taxable_income,
            "amt_income": amt_income,
        }
    )

    # Add policy information
    property_tax_df["policy"] = (
        baseline_scenario if reform_params is None else "Reform"
    )
    property_tax_df["state"] = state_code


    return property_tax_df



def calculate_income_df(
    state_code,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    real_estate_taxes,
    reform_params,
    baseline_scenario,
):
    """
    Calculate effective SALT cap for a single axis situation (fixed employment income)
    """
    # Create situation with employment income fixed
    situation = create_situation_with_one_income_axes(
        state_code,
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        real_estate_taxes,
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
    salt_deduction = simulation.calculate(
        "salt_deduction", map_to="household", period=2026
    )
    sales_or_income_tax = simulation.calculate(
        "state_and_local_sales_or_income_tax", map_to="household", period=2026
    )
    salt_and_property_tax = real_estate_taxes + sales_or_income_tax
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate("taxable_income", map_to="household", period=2026)
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    # Create DataFrame with data
    income_df = pd.DataFrame(
        {
            "employment_income": employment_income,
            "real_estate_taxes": real_estate_taxes,
            "regular_tax": regular_tax,
            "amt": amt,
            "salt_deduction": salt_deduction,
            "sales_or_income_tax": sales_or_income_tax,
            "amt_binds": amt > regular_tax,
            "salt_and_property_tax": salt_and_property_tax,
            "income_tax": income_tax,
            "taxable_income": taxable_income,
            "amt_income": amt_income,
        }
    )

    # Add policy information
    income_df["policy"] = (
        baseline_scenario if reform_params is None else "Reform"
    )
    income_df["state"] = state_code


    return income_df


def calculate_effective_salt_cap_over_earnings(
    state_code,
    is_married,
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
        state_code,
        is_married,
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
    property_taxes_axis = simulation.calculate(
        "real_estate_taxes", map_to="household", period=2026
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
    salt_and_property_tax = property_taxes_axis + sales_or_income_tax
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate("taxable_income", map_to="household", period=2026)
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    # Create DataFrame with data
    effective_caps_over_earnings = pd.DataFrame(
        {
            "employment_income": employment_income_axis,
            "property_tax": property_taxes_axis,
            "regular_tax": regular_tax,
            "amt": amt,
            "salt_deduction": salt_deduction,
            "sales_or_income_tax": sales_or_income_tax,
            "amt_binds": amt > regular_tax,
            "salt_and_property_tax": salt_and_property_tax,
            "income_tax": income_tax,
            "taxable_income": taxable_income,
            "amt_income": amt_income,
        }
    )

    # Add policy information
    effective_caps_over_earnings["policy"] = (
        baseline_scenario if reform_params is None else "Reform"
    )
    effective_caps_over_earnings["state"] = state_code

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
        and not group["property_tax"].is_monotonic_increasing
    ):
        needs_sorting = True
        group = group.sort_values("property_tax")

    # Calculate differences in income tax and property tax
    group["income_tax_diff"] = group["income_tax"].diff()
    group["property_tax_diff"] = group["property_tax"].diff()

    # Calculate the marginal rate (change in income tax / change in property tax)
    group["marginal_property_tax_rate"] = (
        -group["income_tax_diff"] / group["property_tax_diff"]
    )

    # Handle edge cases (divide by zero, first row in group)
    group["marginal_property_tax_rate"] = group["marginal_property_tax_rate"].replace(
        [np.inf, -np.inf, np.nan], 0
    )

    # If we sorted the group, restore the original order
    if needs_sorting and "original_index" in group.columns:
        group = group.sort_values("original_index").drop("original_index", axis=1)

    return group


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


def process_effective_cap_data(effective_cap_df):
    """
    Process the effective cap data by calculating marginal rates for each income level
    """
    # Sort the dataframe
    processed_df = effective_cap_df.sort_values(
        by=["policy", "employment_income", "property_tax"]
    )

    # Calculate the marginal property tax rate for each income level
    processed_df = (
        processed_df.groupby(["policy", "employment_income"])
        .apply(calculate_marginal_rate)
        .reset_index(drop=True)
    )

    return processed_df

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
    
    # Get the index of maximum salt_and_property_tax for each income level
    idx_max = grouped["salt_and_property_tax"].idxmax()
    
    # Use these indices to get the corresponding rows
    # Include all columns needed for all four charts
    columns_to_keep = [
        "employment_income", 
        "salt_deduction", 
        "salt_and_property_tax", 
        "regular_tax", 
        "amt", 
        "taxable_income",
        "amt_income",
        "income_tax"
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
    
    # Get the index of maximum salt_and_property_tax for each income level
    idx_max = grouped["salt_and_property_tax"].idxmax()
    
    # Use these indices to get the corresponding rows
    # Include all columns needed for all four charts
    columns_to_keep = [
        "employment_income", 
        "salt_deduction", 
        "salt_and_property_tax", 
        "regular_tax", 
        "amt", 
        "taxable_income",
        "amt_income",
        "income_tax"
    ]
    
    # Create DataFrame with only the columns we need
    max_salt_by_income = filtered_df.loc[idx_max][columns_to_keep]
    
    # Sort by income for proper plotting
    max_salt_by_income = max_salt_by_income.sort_values("employment_income")
    
    return max_salt_by_income
