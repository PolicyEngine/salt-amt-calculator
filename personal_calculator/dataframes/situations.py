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
            "tax_units": {
                "your tax unit": {
                    "members": members.copy(),
                }
            },
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy(),
                    "state_code": {"2026": state_code},
                }
            },
            # Set up axes for property taxes only
            "axes": [
                [
                    {
                        "name": "reported_salt",
                        "count": 600,
                        "min": 0,
                        "max": 300000,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation_with_one_axes


def create_situation_with_one_income_axes(
    is_married,
    state_code,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
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
            "age": {"2026": 10},
        }
        members.append(child_id)

    situation_with_one_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {
                "your tax unit": {
                    "members": members.copy(),
                    "state_and_local_sales_or_income_tax": {"2026": 0},
                },
            },
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy(),
                    "state_code": {"2026": state_code},
                }
            },
            # Set up axes for property taxes only
            "axes": [
                [
                    {
                        "name": "employment_income",
                        "count": 1000,
                        "min": 0,
                        "max": 1000000,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation_with_one_axes


def create_situation_with_two_axes(
    is_married,
    state_code,
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
            "age": {"2026": 10},
        }
        members.append(child_id)

    situation_with_two_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {
                "your tax unit": {
                    "members": members.copy(),
                    "state_and_local_sales_or_income_tax": {"2026": 0},
                }
            },
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy(),
                    "state_code": {"2026": state_code},
                }
            },
            # Set up axes for property taxes and employment income
            "axes": [
                [
                    {
                        "name": "reported_salt",
                        "count": 700,
                        "min": -50000,
                        "max": 250000,
                        "period": 2026,
                    }
                ],
                [
                    {
                        "name": "employment_income",
                        "count": 1400,
                        "min": 0,
                        "max": 1000000,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation_with_two_axes


def create_situation_without_axes(
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
):
    """Creates a situation dictionary based on user inputs"""
    situation = {
        "people": {
            "head": {
                "age": {"2026": 40},
                "employment_income": {"2026": employment_income},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
                "real_estate_taxes": {"2026": real_estate_taxes},
            }
        },
        "households": {
            "household": {
                "members": ["head"],
                "state_code": {"2026": state_code},
            }
        },
        "tax_units": {
            "tax_unit": {
                "members": ["head"],
            }
        },
        "families": {"family": {"members": ["head"]}},
        "spm_units": {"spm_unit": {"members": ["head"]}},
        "marital_units": {"marital_unit": {"members": ["head"]}},
    }

    # Add spouse if married
    if is_married:
        situation["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        # Add spouse to all units
        for unit in [
            "households",
            "tax_units",
            "families",
            "marital_units",
            "spm_units",
        ]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")

    # Add children
    for i in range(num_children):
        child_id = f"child_{i}"
        situation["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        # Add child to relevant units
        for unit in [
            "households",
            "tax_units",
            "families",
            "marital_units",
            "spm_units",
        ]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    return situation
