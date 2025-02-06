from policyengine_us import Simulation
import numpy as np
from personal_calculator.calculator import calculate_impacts
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import get_reform_params_from_config


def _calculate_income(situation, reform_params_dict, baseline_scenario):
    """Calculate net income for a given policy configuration against baseline"""
    # Empty dict means baseline scenario
    if not reform_params_dict:
        results = calculate_impacts(situation, {}, baseline_scenario)
        return results["baseline"]
    
    # Calculate reform impact using the same key as elsewhere
    results = calculate_impacts(
        situation, 
        {"selected_reform": reform_params_dict},
        baseline_scenario
    )
    
    # Check for missing impact value with correct key suffix
    impact_key = "selected_reform_impact"
    impact = results.get(impact_key)
    
    if impact is None:
        raise ValueError(f"Failed to calculate impact for reform. Check reform parameters: {reform_params_dict}")
        
    return results["baseline"] + impact


def calculate_subsidy_rate(situation, period, policy_config, baseline_scenario):
    """Calculate the marginal subsidy rates for property taxes under different policies"""
    
    # Calculate baseline net income
    if baseline_scenario == "Current Law":
        current_policy_base = _calculate_income(situation, CURRENT_POLICY_PARAMS, baseline_scenario)
        baseline_base = _calculate_income(situation, {}, baseline_scenario)
    else:  # Current Policy
        baseline_base = _calculate_income(situation, CURRENT_POLICY_PARAMS, baseline_scenario)
    
    # Calculate your policy base
    reform_params = get_reform_params_from_config(policy_config)
    your_policy_base = _calculate_income(situation, {"selected_reform": reform_params}, baseline_scenario)

    # Create modified situation with increased real estate taxes
    modified_situation = situation.copy()
    delta = 500.0  # $500 increment in real estate taxes

    # Modify the real estate taxes
    head_key = "head"
    if "real_estate_taxes" in modified_situation["people"][head_key]:
        current_taxes = modified_situation["people"][head_key]["real_estate_taxes"][period]
        modified_situation["people"][head_key]["real_estate_taxes"][period] = current_taxes + delta

    # Calculate modified net incomes
    if baseline_scenario == "Current Law":
        current_policy_mod = _calculate_income(modified_situation, CURRENT_POLICY_PARAMS, baseline_scenario)
        baseline_mod = _calculate_income(modified_situation, {}, baseline_scenario)
    else:
        baseline_mod = _calculate_income(modified_situation, CURRENT_POLICY_PARAMS, baseline_scenario)
    
    your_policy_mod = _calculate_income(modified_situation, {"selected_reform": reform_params}, baseline_scenario)

    # Calculate subsidy rates
    subsidy_rates = {
        baseline_scenario: (baseline_mod - baseline_base) / delta,
        "Your Policy": (your_policy_mod - your_policy_base) / delta,
    }

    # Only show current policy rate if baseline is current law
    if baseline_scenario == "Current Law":
        subsidy_rates["Current Policy"] = (current_policy_mod - current_policy_base) / delta

    return {k: float(v) for k, v in subsidy_rates.items()}
