from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from reforms import PolicyReforms

def calculate_impacts(situation, reform_params_1, reform_params_2):
    """Calculate the impacts of two different reform scenarios"""
    # Set up baseline simulation
    baseline = Simulation(situation=situation)
    baseline_income = baseline.calculate("household_net_income", "2025")[0]
    
    # Calculate Reform 1
    reform1_dict = PolicyReforms.policy_reforms(reform_params_1)
    reform1 = Reform.from_dict(reform1_dict, country_id="us")
    reform1_sim = Simulation(situation=situation, reform=reform1)
    reform1_income = reform1_sim.calculate("household_net_income", "2025")[0]
    
    # Calculate Reform 2
    reform2_dict = PolicyReforms.policy_reforms(reform_params_2)
    reform2 = Reform.from_dict(reform2_dict, country_id="us")
    reform2_sim = Simulation(situation=situation, reform=reform2)
    reform2_income = reform2_sim.calculate("household_net_income", "2025")[0]
    
    return (
        baseline_income,
        reform1_income - baseline_income,
        reform2_income - baseline_income
    )