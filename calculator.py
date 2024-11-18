from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import PolicyReforms


def calculate_impacts(situation, reform_params_dict):
    """Calculate the impacts of multiple reform scenarios"""
    # Set up baseline simulation
    current_law = Simulation(situation=situation)
    current_law_income = current_law.calculate("household_net_income", "2026")[0]

    # Initialize results dictionary with baseline
    results = {"current_law": current_law_income}

    # Calculate each reform
    for reform_key, reform_params in reform_params_dict.items():
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        reform_sim = Simulation(situation=situation, reform=reform)
        reform_income = reform_sim.calculate("household_net_income", "2026")[0]

        # Store the impact
        results[f"{reform_key}_impact"] = reform_income - current_law_income

    return results
