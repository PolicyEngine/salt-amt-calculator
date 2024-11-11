from policyengine_us import Simulation
from reforms import PolicyReforms

def calculate_impact(situation, salt_cap):
    """Calculate the impact of a SALT cap change"""
    reform = PolicyReforms.policy_reforms(salt_cap)
    
    baseline = Simulation(situation=situation)
    reform_sim = Simulation(situation=situation, reform=reform)
    
    baseline_income = baseline.calculate("household_net_income", "2025")[0]
    reform_income = reform_sim.calculate("household_net_income", "2025")[0]
    
    return reform_income - baseline_income