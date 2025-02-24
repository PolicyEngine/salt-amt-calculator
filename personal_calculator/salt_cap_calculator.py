from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import PolicyReforms
import numpy as np
import pandas as pd



def create_situation_with_axes(
        state_code,
        employment_income,
        is_married,
        spouse_income,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        real_estate_taxes,
        deductible_mortgage_interest,
        charitable_cash_donations,
):


    situation_with_axes = {
        "people": {
            "you": {
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
        "families": {
            "your family": {
            "members": [
                "you"
            ]
            }
        },
        "marital_units": {
            "your marital unit": {
            "members": [
                "you"
            ]
            }
        },
        "tax_units": {
            "your tax unit": {
            "members": [
                "you"
            ]
            }
        },
        "spm_units": {
            "your household": {
            "members": [
                "you"
            ]
            }
        },
        "households": {
            "your household": {
            "members": [
                "you"
            ],
            "state_name": {
                "2026": state_code
            }
            }
        },
        "axes": [
            [
            {
                "name": "real_estate_taxes",
                "count": 500,
                "min": 0,
                "max": 50000
            }
            ]
        ]
        }


    # Add spouse if married
    if is_married:
        situation_with_axes["people"]["spouse"] = {
            "age": {"2026": 40},
            "employment_income": {"2026": spouse_income},
        }
        # Add spouse to all units
        for unit in ["households", "tax_units", "families", "marital_units"]:
            situation_with_axes[unit][list(situation_with_axes[unit].keys())[0]]["members"].append("spouse")

    # Add children
    for i in range(num_children):
        child_id = f"child_{i}"
        situation_with_axes["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        # Add child to relevant units
        for unit in ["households", "tax_units", "families"]:
            situation_with_axes[unit][list(situation_with_axes[unit].keys())[0]]["members"].append(child_id)


    return situation_with_axes



def find_effective_salt_cap(
    situation_with_axes,
    reform_params_dict,
    baseline_scenario,
    tolerance=1
):
    """
    Find the effective SALT cap by incrementing real estate taxes until tax liability stops changing

    Args:
        situation_with_axes (dict): The situation with axes for varying real estate taxes
        reform_params_dict (dict): Dictionary of reform parameters
        baseline_scenario (str): The baseline scenario ("Current Law" or "Current Policy")
        tolerance (float): Minimum change in tax liability to consider significant (default $1)

    Returns:
        dict: Dictionary containing:
            - 'baseline_cap': Effective SALT cap under baseline scenario
            - 'reform_cap': Effective SALT cap under reform scenario
            - 'baseline_tax_at_cap': Tax liability at baseline cap
            - 'reform_tax_at_cap': Tax liability at reform cap
    """
    
    print("Starting SALT cap calculation...")
    
    # Get the real estate tax values
    tax_amounts = np.linspace(0, 50000, 500)
    baseline_taxes = []
    reform_taxes = []
    
    print(f"Testing {len(tax_amounts)} different tax amounts...")
    
    # Calculate taxes for each real estate tax amount
    for tax_amount in tax_amounts:
        # Create a copy of the situation for this iteration
        test_situation = situation_with_axes.copy()
        test_situation["people"]["head"]["real_estate_taxes"]["2026"] = tax_amount
        
        # Calculate baseline taxes
        if baseline_scenario == "Current Law":
            baseline_sim = Simulation(situation=test_situation)
        else:  # Current Policy
            current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
            reform = Reform.from_dict(current_policy_reform, country_id="us")
            baseline_sim = Simulation(situation=test_situation, reform=reform)
        baseline_tax = baseline_sim.calculate("income_tax", 2026)
        baseline_taxes.append(float(baseline_tax))
        
        # Calculate reform taxes
        reform_dict = PolicyReforms.policy_reforms(reform_params_dict["selected_reform"])
        if baseline_scenario == "Current Policy":
            reform_dict.update(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(reform_dict, country_id="us")
        reform_sim = Simulation(situation=test_situation, reform=reform)
        reform_tax = reform_sim.calculate("income_tax", 2026)
        reform_taxes.append(float(reform_tax))
    
    # Convert lists to numpy arrays
    baseline_taxes = np.array(baseline_taxes)
    reform_taxes = np.array(reform_taxes)
    
    print("\nArrays created successfully:")
    print(f"tax_amounts length: {len(tax_amounts)}")
    print(f"baseline_taxes length: {len(baseline_taxes)}")
    print(f"reform_taxes length: {len(reform_taxes)}")
    
    # Create DataFrame with results
    results_df = pd.DataFrame({
        'real_estate_taxes': tax_amounts,
        'baseline_tax': baseline_taxes,
        'reform_tax': reform_taxes
    })
    
    print("\nFirst few rows of results DataFrame:")
    print(results_df.head())
    
    # Calculate tax differences
    results_df['baseline_diff'] = results_df['baseline_tax'].diff()
    results_df['reform_diff'] = results_df['reform_tax'].diff()
    
    # Find caps using DataFrame operations
    baseline_cap_idx = (results_df['baseline_diff'].abs() < tolerance).idxmax()
    reform_cap_idx = (results_df['reform_diff'].abs() < tolerance).idxmax()
    
    caps = {"baseline": None, "reform": None}
    tax_at_cap = {"baseline": None, "reform": None}
    
    if baseline_cap_idx > 0:  # Only set if we found a valid cap
        caps["baseline"] = results_df.loc[baseline_cap_idx - 1, 'real_estate_taxes']
        tax_at_cap["baseline"] = results_df.loc[baseline_cap_idx - 1, 'baseline_tax']
    
    if reform_cap_idx > 0:  # Only set if we found a valid cap
        caps["reform"] = results_df.loc[reform_cap_idx - 1, 'real_estate_taxes']
        tax_at_cap["reform"] = results_df.loc[reform_cap_idx - 1, 'reform_tax']
    
    print("\nFound caps:")
    print(f"Baseline cap: {caps['baseline']}")
    print(f"Reform cap: {caps['reform']}")

    return {
        "baseline_cap": caps["baseline"],
        "reform_cap": caps["reform"],
        "baseline_tax_at_cap": tax_at_cap["baseline"],
        "reform_tax_at_cap": tax_at_cap["reform"]
    }