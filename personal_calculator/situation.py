def create_situation(
    state_code,
    employment_income,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    real_estate_taxes,
    deductible_mortgage_interest,
    charitable_cash_donations,
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
                "real_estate_taxes": {"2026": real_estate_taxes},
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
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
            "age": {"2026": 40},
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
