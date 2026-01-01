"""Situation builders for PolicyEngine-US simulations."""

from typing import Optional


def create_situation_without_axes(
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
) -> dict:
    """Creates a situation dictionary for single-point calculations."""
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
        age = child_ages[i] if i < len(child_ages) else 10
        situation["people"][child_id] = {
            "age": {"2026": age},
        }
        for unit in [
            "households",
            "tax_units",
            "families",
            "marital_units",
            "spm_units",
        ]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    return situation


def create_situation_with_one_property_tax_axes(
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
    min_salt: float = 0,
    max_salt: float = 300000,
    count: int = 600,
) -> dict:
    """Create a situation with one axis (reported_salt), fixed employment income."""
    situation = {
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
        situation["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        age = child_ages[i] if i < len(child_ages) else 10
        situation["people"][child_id] = {
            "age": {"2026": age},
        }
        members.append(child_id)

    situation.update(
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
            "axes": [
                [
                    {
                        "name": "reported_salt",
                        "count": count,
                        "min": min_salt,
                        "max": max_salt,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation


def create_situation_with_one_income_axes(
    is_married: bool,
    state_code: str,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    min_income: float = 0,
    max_income: float = 1000000,
    count: int = 1000,
) -> dict:
    """Create a situation with one axis (employment_income)."""
    situation = {
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
        situation["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        age = child_ages[i] if i < len(child_ages) else 10
        situation["people"][child_id] = {
            "age": {"2026": age},
        }
        members.append(child_id)

    situation.update(
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
            "axes": [
                [
                    {
                        "name": "employment_income",
                        "count": count,
                        "min": min_income,
                        "max": max_income,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation


def create_situation_with_two_axes(
    is_married: bool,
    state_code: str,
    num_children: int,
    child_ages: list[int],
    qualified_dividend_income: float,
    long_term_capital_gains: float,
    short_term_capital_gains: float,
    deductible_mortgage_interest: float,
    charitable_cash_donations: float,
    min_salt: float = -50000,
    max_salt: float = 250000,
    salt_count: int = 700,
    min_income: float = 0,
    max_income: float = 1000000,
    income_count: int = 1400,
) -> dict:
    """Create a situation with two axes (reported_salt and employment_income)."""
    situation = {
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
        situation["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        age = child_ages[i] if i < len(child_ages) else 10
        situation["people"][child_id] = {
            "age": {"2026": age},
        }
        members.append(child_id)

    situation.update(
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
            "axes": [
                [
                    {
                        "name": "reported_salt",
                        "count": salt_count,
                        "min": min_salt,
                        "max": max_salt,
                        "period": 2026,
                    }
                ],
                [
                    {
                        "name": "employment_income",
                        "count": income_count,
                        "min": min_income,
                        "max": max_income,
                        "period": 2026,
                    }
                ],
            ],
        }
    )
    return situation
