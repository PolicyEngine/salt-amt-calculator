import pandas as pd
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import PolicyReforms
from constants import BLUE, DARK_GRAY


def create_situation_with_one_property_tax_axes(
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
):
    """
    Create a situation dictionary with one axis (real_estate_taxes),
    using a fixed employment income value.
    """
    situation_with_one_axes = {
        "people": {
            "you": {
                "age": {"2026": 40},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
                "employment_income": {"2026": employment_income},
            }
        }
    }
    members = ["you"]

    if is_married:
        situation_with_one_axes["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        situation_with_one_axes["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        members.append(child_id)

    situation_with_one_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {"your tax unit": {
                "members": members.copy(),
                "state_and_local_sales_or_income_tax": {"2026": 0}}},
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy()
                }
            },
            # Set up axes for property taxes only
            "axes": [
                [{"name": "real_estate_taxes", "count": 300, "min": 0, "max": 140000}],
            ],
        }
    )
    return situation_with_one_axes


def create_situation_with_one_income_axes(
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    real_estate_taxes,
):
    """
    Create a situation dictionary with one axis (real_estate_taxes),
    using a fixed employment income value.
    """
    situation_with_one_axes = {
        "people": {
            "you": {
                "age": {"2026": 40},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
                "real_estate_taxes": {"2026": real_estate_taxes},
            }
        }
    }
    members = ["you"]

    if is_married:
        situation_with_one_axes["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        situation_with_one_axes["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        members.append(child_id)

    situation_with_one_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {"your tax unit": {
                "members": members.copy(),
                "state_and_local_sales_or_income_tax": {"2026": 0}}},
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy()
                }
            },
            # Set up axes for property taxes only
            "axes": [
                [{"name": "employment_income", "count": 300, "min": 0, "max": 1000000}],
            ],
        }
    )
    return situation_with_one_axes


def create_situation_with_two_axes(
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
):
    """
    Create a situation dictionary with two axes (real_estate_taxes and employment_income).
    """
    situation_with_two_axes = {
        "people": {
            "you": {
                "age": {"2026": 40},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
            }
        }
    }
    members = ["you"]

    if is_married:
        situation_with_two_axes["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        situation_with_two_axes["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        members.append(child_id)

    situation_with_two_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {"your tax unit": {
                "members": members.copy(),
                "state_and_local_sales_or_income_tax": {"2026": 0}}},
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy()
                }
            },
            # Set up axes for property taxes and employment income
            "axes": [
                [
                    {
                        "name": "real_estate_taxes",
                        "count": 300,
                        "min": -50000,
                        "max": 140000,
                    }
                ],
                [
                    {
                        "name": "employment_income",
                        "count": 1400,
                        "min": 0,
                        "max": 1000000,
                    }
                ],
            ],
        }
    )
    return situation_with_two_axes
