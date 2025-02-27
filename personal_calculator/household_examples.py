def get_state_tax_description(state, income):
    """
    Get a description of the state tax situation for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        str: Description of state tax situation
    """
    state_tax_data = STATE_TAX_DATA[state][income]
    state_local_tax = state_tax_data["state_local_tax"]
    
    state_names = {
        "NY": "New York",
        "CA": "California",
        "PA": "Pennsylvania",
        "NJ": "New Jersey"
    }
    
    return f"{state_names[state]} levies state and local taxes of ${state_local_tax:,}, which can be deducted under the SALT deduction."

def get_comprehensive_tax_table(state, income):
    """
    Generate a comprehensive tax table showing all calculations for $5k and $10k property taxes
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Comprehensive tax table
    """
    # Get the data from our existing functions
    salt_table = get_salt_deduction_table(state, income)
    tax_liability_table = get_tax_liability_table(state, income)
    amt_table = get_amt_table(state, income)
    federal_tax_table = get_federal_tax_table(state, income)
    
    # Extract values
    current_law_5k_salt = salt_table["$5k property taxes"][0]
    current_policy_5k_salt = salt_table["$5k property taxes"][1]
    current_law_10k_salt = salt_table["$10k property taxes"][0]
    current_policy_10k_salt = salt_table["$10k property taxes"][1]
    
    current_law_5k_regular = tax_liability_table["$5k property taxes"][0]
    current_policy_5k_regular = tax_liability_table["$5k property taxes"][1]
    current_law_10k_regular = tax_liability_table["$10k property taxes"][0]
    current_policy_10k_regular = tax_liability_table["$10k property taxes"][1]
    
    current_law_5k_amt = amt_table["$5k property taxes"][0]
    current_policy_5k_amt = amt_table["$5k property taxes"][1]
    current_law_10k_amt = amt_table["$10k property taxes"][0]
    current_policy_10k_amt = amt_table["$10k property taxes"][1]
    
    current_law_5k_federal = federal_tax_table["$5k property taxes"][0]
    current_policy_5k_federal = federal_tax_table["$5k property taxes"][1]
    current_law_10k_federal = federal_tax_table["$10k property taxes"][0]
    current_policy_10k_federal = federal_tax_table["$10k property taxes"][1]
    
    # Get subsidy rates
    current_law_subsidy = federal_tax_table["Subsidy Rate"][0]
    current_policy_subsidy = federal_tax_table["Subsidy Rate"][1]
    
    # Create the comprehensive table
    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$5k property taxes": [
            current_law_5k_salt,
            current_policy_5k_salt,
            current_law_5k_regular,
            current_policy_5k_regular,
            current_law_5k_amt,
            current_policy_5k_amt,
            current_law_5k_federal,
            current_policy_5k_federal,
        ],
        "$10k property taxes": [
            current_law_10k_salt,
            current_policy_10k_salt,
            current_law_10k_regular,
            current_policy_10k_regular,
            current_law_10k_amt,
            current_policy_10k_amt,
            current_law_10k_federal,
            current_policy_10k_federal,
        ],
        "Difference": [
            salt_table["Difference"][0],
            salt_table["Difference"][1],
            tax_liability_table["Difference"][0],
            tax_liability_table["Difference"][1],
            amt_table["Difference"][0],
            amt_table["Difference"][1],
            federal_tax_table["Difference"][0],
            federal_tax_table["Difference"][1],
        ],
        "Property Tax Subsidy Rate": [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            current_law_subsidy,
            current_policy_subsidy,
        ],
    }
    
    return pd.DataFrame(comparison_data)

def get_higher_property_tax_comparison(state, income):
    """
    Generate a comparison table for 10k and 15k property taxes
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Comparison table for 10k and 15k property taxes
    """
    # This would ideally be calculated dynamically
    # For now, we'll use placeholder data
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    state_tax_data = STATE_TAX_DATA[state][income]
    state_local_tax = state_tax_data["state_local_tax"]
    
    # Calculate SALT deductions
    current_law_10k_salt = min(state_local_tax + 10000, float('inf'))
    current_law_15k_salt = min(state_local_tax + 15000, float('inf'))
    current_policy_10k_salt = min(state_local_tax + 10000, 10000)
    current_policy_15k_salt = min(state_local_tax + 15000, 10000)
    
    # Estimate tax impacts (in a real implementation, these would be calculated)
    # For now, we'll use simplified estimates
    current_law_10k_regular = tax_calcs["current_law"]["10k_property_taxes"]["regular_tax"]
    current_law_15k_regular = current_law_10k_regular - (current_law_15k_salt - current_law_10k_salt) * 0.35
    
    current_policy_10k_regular = tax_calcs["current_policy"]["10k_property_taxes"]["regular_tax"]
    current_policy_15k_regular = current_policy_10k_regular
    
    current_law_10k_amt = tax_calcs["current_law"]["10k_property_taxes"]["amt"]
    current_law_15k_amt = current_law_10k_amt
    
    current_policy_10k_amt = tax_calcs["current_policy"]["10k_property_taxes"]["amt"]
    current_policy_15k_amt = current_policy_10k_amt
    
    # Determine which tax applies (regular or AMT)
    current_law_10k_tax = max(current_law_10k_regular, current_law_10k_amt)
    current_law_15k_tax = max(current_law_15k_regular, current_law_15k_amt)
    
    current_policy_10k_tax = max(current_policy_10k_regular, current_policy_10k_amt)
    current_policy_15k_tax = max(current_policy_15k_regular, current_policy_15k_amt)
    
    # Calculate differences and subsidy rates
    current_law_diff = current_law_15k_tax - current_law_10k_tax
    current_policy_diff = current_policy_15k_tax - current_policy_10k_tax
    
    current_law_subsidy = abs(round(current_law_diff / 5000 * 100))
    current_policy_subsidy = abs(round(current_policy_diff / 5000 * 100))
    
    # Create the comparison data
    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$10k property taxes": [
            f"${current_law_10k_salt:,.0f}",
            f"${current_policy_10k_salt:,.0f}",
            f"${current_law_10k_regular:,.0f}",
            f"${current_policy_10k_regular:,.0f}",
            f"${current_law_10k_amt:,.0f}",
            f"${current_policy_10k_amt:,.0f}",
            f"${current_law_10k_tax:,.0f}",
            f"${current_policy_10k_tax:,.0f}",
        ],
        "$15k property taxes": [
            f"${current_law_15k_salt:,.0f}",
            f"${current_policy_15k_salt:,.0f}",
            f"${current_law_15k_regular:,.0f}",
            f"${current_policy_15k_regular:,.0f}",
            f"${current_law_15k_amt:,.0f}",
            f"${current_policy_15k_amt:,.0f}",
            f"${current_law_15k_tax:,.0f}",
            f"${current_policy_15k_tax:,.0f}",
        ],
        "Difference": [
            f"${current_law_15k_salt - current_law_10k_salt:,.0f}",
            f"${current_policy_15k_salt - current_policy_10k_salt:,.0f}",
            f"${current_law_15k_regular - current_law_10k_regular:,.0f}",
            f"${current_policy_15k_regular - current_policy_10k_regular:,.0f}",
            f"${current_law_15k_amt - current_law_10k_amt:,.0f}",
            f"${current_policy_15k_amt - current_policy_10k_amt:,.0f}",
            f"${current_law_diff:,.0f}",
            f"${current_policy_diff:,.0f}",
        ],
        "Subsidy Rate": [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            f"{current_law_subsidy}%",
            f"{current_policy_subsidy}%",
        ],
    }
    
    return pd.DataFrame(comparison_data) 