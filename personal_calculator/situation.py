def create_situation(
    state_code,
    employment_income,
    head_age,
    is_married,
    spouse_age,
    spouse_income,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    real_estate_taxes,
):
    """Creates a situation dictionary based on user inputs"""
    situation = {
        "people": {
            "head": {
                "age": {"2026": head_age},
                "employment_income": {"2026": employment_income},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
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
        "marital_units": {"marital_unit": {"members": ["head"]}},
    }

    # Add spouse if married
    if is_married:
        situation["people"]["spouse"] = {
            "age": {"2026": spouse_age},
            "employment_income": {"2026": spouse_income},
        }
        # Add spouse to all units
        for unit in ["households", "tax_units", "families", "marital_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")

    # Add children
    for i in range(num_children):
        child_id = f"child_{i}"
        situation["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        # Add child to relevant units
        for unit in ["households", "tax_units", "families"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    return situation

def create_situation_with_axes(
    state_code,
    employment_income,
    head_age,
    is_married,
    spouse_age,
    spouse_income,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    real_estate_taxes,
    income_min=0,
    income_max=200000,
    income_count=200
):
    """Creates a situation dictionary with axes for income variation"""
    situation = {
        "people": {
            "head": {
                "age": {"2026": head_age},
                "employment_income": {"2026": employment_income},
                "qualified_dividend_income": {"2026": qualified_dividend_income},
                "long_term_capital_gains": {"2026": long_term_capital_gains},
                "short_term_capital_gains": {"2026": short_term_capital_gains},
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
        "marital_units": {"marital_unit": {"members": ["head"]}},
    }

    # Add spouse if married
    if is_married:
        situation["people"]["spouse"] = {
            "age": {"2026": spouse_age},
            "employment_income": {"2026": spouse_income},
        }
        # Add spouse to all units
        for unit in ["households", "tax_units", "families", "marital_units"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")

    # Add children
    for i in range(num_children):
        child_id = f"child_{i}"
        situation["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        # Add child to relevant units
        for unit in ["households", "tax_units", "families"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)

    # Add axes for income variation
    situation["axes"] = [
        [
            {
                "name": "employment_income",
                "count": income_count,
                "min": income_min,
                "max": income_max
            }
        ]
    ]

    return situation