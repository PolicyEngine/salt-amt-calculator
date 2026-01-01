"""Calculation functions for PolicyEngine-US simulations."""

from typing import Optional
import numpy as np

from policyengine_us import Simulation
from policyengine_core.reforms import Reform

from .reforms import PolicyReforms, CURRENT_POLICY_PARAMS, get_reform_params_from_config
from .situation import (
    create_situation_without_axes,
    create_situation_with_one_property_tax_axes,
    create_situation_with_one_income_axes,
    create_situation_with_two_axes,
)


def _create_simulation(
    situation: dict,
    baseline_scenario: str,
    reform_params: Optional[dict] = None,
) -> Simulation:
    """Create a simulation based on scenario and reform params."""
    if baseline_scenario == "Current Law" and reform_params is None:
        return Simulation(situation=situation)
    elif baseline_scenario == "Current Policy" and reform_params is None:
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        return Simulation(situation=situation, reform=reform)
    elif reform_params is not None:
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        return Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid scenario configuration")


def calculate_single_point(
    state_code: str,
    real_estate_taxes: float,
    is_married: bool,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    employment_income: float,
    baseline_scenario: str = "Current Law",
    reform_params: Optional[dict] = None,
) -> dict:
    """Calculate tax values for a single household configuration."""
    situation = create_situation_without_axes(
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
    )

    simulation = _create_simulation(situation, baseline_scenario, reform_params)

    # Use .item() to convert numpy 0-d arrays to Python scalars
    household_net_income = float(
        simulation.calculate("household_net_income", map_to="household", period=2026).item()
    )
    federal_income_tax = float(
        simulation.calculate("income_tax", map_to="household", period=2026).item()
    )
    state_income_tax = float(
        simulation.calculate(
            "state_withheld_income_tax", map_to="household", period=2026
        ).item()
    )
    state_sales_tax = float(
        simulation.calculate("state_sales_tax", map_to="household", period=2026).item()
    )
    salt_deduction = float(
        simulation.calculate("salt_deduction", map_to="household", period=2026).item()
    )
    reported_salt = float(
        simulation.calculate("reported_salt", map_to="household", period=2026).item()
    )
    regular_tax = float(
        simulation.calculate(
            "regular_tax_before_credits", map_to="household", period=2026
        ).item()
    )
    amt = float(simulation.calculate("amt_base_tax", map_to="household", period=2026).item())
    taxable_income = float(
        simulation.calculate("taxable_income", map_to="household", period=2026).item()
    )
    amt_income = float(
        simulation.calculate("amt_income", map_to="household", period=2026).item()
    )

    return {
        "household_net_income": household_net_income,
        "federal_income_tax": federal_income_tax,
        "state_income_tax": state_income_tax,
        "state_sales_tax": state_sales_tax,
        "salt_deduction": salt_deduction,
        "reported_salt": reported_salt,
        "regular_tax": regular_tax,
        "amt": amt,
        "taxable_income": taxable_income,
        "amt_income": amt_income,
        "larger_of_state_sales_or_income_tax": max(state_sales_tax, state_income_tax),
        "state_income_tax_over_sales_tax": bool(state_income_tax > state_sales_tax),
    }


def calculate_salt_axis(
    is_married: bool,
    state_code: str,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    employment_income: float,
    baseline_scenario: str = "Current Law",
    reform_params: Optional[dict] = None,
    min_salt: float = 0,
    max_salt: float = 300000,
    count: int = 600,
) -> dict:
    """Calculate tax values along the SALT axis (fixed income)."""
    situation = create_situation_with_one_property_tax_axes(
        is_married=is_married,
        state_code=state_code,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        employment_income=employment_income,
        min_salt=min_salt,
        max_salt=max_salt,
        count=count,
    )

    simulation = _create_simulation(situation, baseline_scenario, reform_params)

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
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate(
        "taxable_income", map_to="household", period=2026
    )
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    return {
        "axis_values": reported_salt.tolist(),
        "reported_salt": reported_salt.tolist(),
        "salt_deduction": salt_deduction.tolist(),
        "regular_tax": regular_tax.tolist(),
        "amt": amt.tolist(),
        "income_tax": income_tax.tolist(),
        "taxable_income": taxable_income.tolist(),
        "amt_income": amt_income.tolist(),
    }


def calculate_income_axis(
    is_married: bool,
    state_code: str,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    baseline_scenario: str = "Current Law",
    reform_params: Optional[dict] = None,
    min_income: float = 0,
    max_income: float = 1000000,
    count: int = 1000,
) -> dict:
    """Calculate tax values along the income axis."""
    situation = create_situation_with_one_income_axes(
        is_married=is_married,
        state_code=state_code,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        min_income=min_income,
        max_income=max_income,
        count=count,
    )

    simulation = _create_simulation(situation, baseline_scenario, reform_params)

    employment_income = simulation.calculate(
        "employment_income", map_to="household", period=2026
    )
    regular_tax = simulation.calculate(
        "regular_tax_before_credits", map_to="household", period=2026
    )
    amt = simulation.calculate("amt_base_tax", map_to="household", period=2026)
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate(
        "taxable_income", map_to="household", period=2026
    )
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)
    salt_deduction = simulation.calculate(
        "salt_deduction", map_to="household", period=2026
    )

    gap = np.maximum(regular_tax - amt, 0)

    return {
        "axis_values": employment_income.tolist(),
        "employment_income": employment_income.tolist(),
        "salt_deduction": salt_deduction.tolist(),
        "regular_tax": regular_tax.tolist(),
        "amt": amt.tolist(),
        "income_tax": income_tax.tolist(),
        "taxable_income": taxable_income.tolist(),
        "amt_income": amt_income.tolist(),
        "gap": gap.tolist(),
    }


def calculate_two_axes(
    is_married: bool,
    state_code: str,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    baseline_scenario: str = "Current Law",
    reform_params: Optional[dict] = None,
    min_salt: float = -50000,
    max_salt: float = 250000,
    salt_count: int = 700,
    min_income: float = 0,
    max_income: float = 1000000,
    income_count: int = 1400,
) -> dict:
    """Calculate tax values on a 2D grid (SALT x income)."""
    situation = create_situation_with_two_axes(
        is_married=is_married,
        state_code=state_code,
        num_children=num_children,
        child_ages=child_ages,
        qualified_dividend_income=qualified_dividend_income,
        long_term_capital_gains=long_term_capital_gains,
        short_term_capital_gains=short_term_capital_gains,
        deductible_mortgage_interest=deductible_mortgage_interest,
        charitable_cash_donations=charitable_cash_donations,
        min_salt=min_salt,
        max_salt=max_salt,
        salt_count=salt_count,
        min_income=min_income,
        max_income=max_income,
        income_count=income_count,
    )

    simulation = _create_simulation(situation, baseline_scenario, reform_params)

    employment_income = simulation.calculate(
        "employment_income", map_to="household", period=2026
    )
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
    income_tax = simulation.calculate("income_tax", map_to="household", period=2026)
    taxable_income = simulation.calculate(
        "taxable_income", map_to="household", period=2026
    )
    amt_income = simulation.calculate("amt_income", map_to="household", period=2026)

    return {
        "employment_income": employment_income.tolist(),
        "reported_salt": reported_salt.tolist(),
        "regular_tax": regular_tax.tolist(),
        "amt": amt.tolist(),
        "salt_deduction": salt_deduction.tolist(),
        "income_tax": income_tax.tolist(),
        "taxable_income": taxable_income.tolist(),
        "amt_income": amt_income.tolist(),
        "amt_binds": (amt > regular_tax).tolist(),
    }
