def create_situation(
    state_code,
    filing_status,
    employment_income,
    head_age,
    is_married,
    spouse_age,
    spouse_income,  # Added spouse_income parameter
    num_children,
    child_ages,
    state_and_local_sales_or_income_tax,
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
                "filing_status": {"2026": filing_status},
                "state_and_local_sales_or_income_tax": {
                    "2026": state_and_local_sales_or_income_tax
                },
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