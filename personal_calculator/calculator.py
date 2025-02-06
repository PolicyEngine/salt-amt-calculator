from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from personal_calculator.reforms import PolicyReforms
from constants import CURRENT_POLICY_PARAMS


def calculate_impacts(situation, reform_params_dict, baseline_scenario):
    """Calculate the impacts of multiple reform scenarios against the selected baseline"""

    # Set up baseline simulation based on selected scenario
    if baseline_scenario == "Current Law":
        baseline_sim = Simulation(situation=situation)
    elif baseline_scenario == "Current Policy":
        # Apply current policy parameters as a reform to current law
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        baseline_sim = Simulation(situation=situation, reform=reform)
    else:
        raise ValueError(f"Invalid baseline scenario: {baseline_scenario}")

    baseline_income = baseline_sim.calculate("household_net_income", "2026")[0]
    
    results = {"baseline": baseline_income}

    # Calculate each reform against the baseline
    for reform_key, reform_params in reform_params_dict.items():
        try:
            # Create reform based on parameters
            reform_dict = PolicyReforms.policy_reforms(reform_params)
            reform = Reform.from_dict(reform_dict, country_id="us")
            # Apply reform to the baseline scenario
            reform_sim = Simulation(situation=situation, reform=reform)
            reform_income = reform_sim.calculate("household_net_income", "2026")[0]
            impact = reform_income - baseline_income
            results[f"{reform_key}_impact"] = impact
        except Exception as e:
            results[f"{reform_key}_impact"] = None

    return results
