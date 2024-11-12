from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import PolicyReforms

def calculate_impacts(situation, reform_params_dict):
    """Calculate the impacts of multiple reform scenarios"""
    # Set up baseline simulation
    baseline = Simulation(situation=situation)
    baseline_income = baseline.calculate("household_net_income", "2025")[0]
    
    # Initialize results dictionary with baseline
    results = {'baseline': baseline_income}
    
    # Calculate each reform
    for reform_key, reform_params in reform_params_dict.items():
        reform_dict = PolicyReforms.policy_reforms(reform_params)
        reform = Reform.from_dict(reform_dict, country_id="us")
        reform_sim = Simulation(situation=situation, reform=reform)
        reform_income = reform_sim.calculate("household_net_income", "2025")[0]
        
        # Store the impact
        results[f'{reform_key}_impact'] = reform_income - baseline_income
    
    return results