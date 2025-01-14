from policyengine_us import Simulation
import numpy as np
from personal_calculator.calculator import calculate_impacts
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import get_reform_params_from_config

def calculate_subsidy_rate(situation, period, policy_config):
    """Calculate the marginal subsidy rates for real estate taxes under different policies"""
    # Set up baseline situations
    baseline_sim = Simulation(situation=situation)
    
    # Calculate baseline net incomes for each policy
    results = calculate_impacts(situation, {})
    current_law_base = results["current_law"]
    
    current_policy_results = calculate_impacts(situation, CURRENT_POLICY_PARAMS)
    current_policy_base = current_law_base + current_policy_results["reform_current_policy_impact"]
    
    reform_params = get_reform_params_from_config(policy_config)
    your_policy_params = {"selected_reform": reform_params}
    your_policy_results = calculate_impacts(situation, your_policy_params)
    your_policy_base = current_law_base + your_policy_results["selected_reform_impact"]

    # Create modified situation with increased real estate taxes
    modified_situation = situation.copy()
    delta = 500.0  # $500 increment in real estate taxes

    # Modify the real estate taxes
    head_key = "head"
    if "real_estate_taxes" in modified_situation["people"][head_key]:
        current_taxes = modified_situation["people"][head_key]["real_estate_taxes"][period]
        modified_situation["people"][head_key]["real_estate_taxes"][period] = current_taxes + delta

    # Calculate modified net incomes for each policy
    mod_results = calculate_impacts(modified_situation, {})
    current_law_mod = mod_results["current_law"]
    
    mod_current_policy_results = calculate_impacts(modified_situation, CURRENT_POLICY_PARAMS)
    current_policy_mod = current_law_mod + mod_current_policy_results["reform_current_policy_impact"]
    
    mod_your_policy_results = calculate_impacts(modified_situation, your_policy_params)
    your_policy_mod = current_law_mod + mod_your_policy_results["selected_reform_impact"]

    # Calculate subsidy rates
    subsidy_rates = {
        "Current Law": float(current_law_mod - current_law_base) / delta,
        "Current Policy": float(current_policy_mod - current_policy_base) / delta,
        "Your Policy": float(your_policy_mod - your_policy_base) / delta
    }

    return subsidy_rates
