from personal_calculator.calculator import calculate_impacts

def calculate_marginal_subsidy_rate(situation, reform_params_dict, baseline_scenario, increment=500):
    """
    Calculate the marginal subsidy rate for a $500 increase in real estate taxes
    
    Args:
        situation (dict): The baseline tax situation
        reform_params_dict (dict): Dictionary of reform parameters
        baseline_scenario (str): The baseline scenario ("Current Law" or "Current Policy")
        increment (float): The amount to increment real estate taxes by (default $500)
    
    Returns:
        dict: Dictionary containing marginal subsidy rates for baseline and reform scenarios
    """    
    # First calculate the original situation
    original_results = calculate_impacts(situation, reform_params_dict, baseline_scenario)
    # Create a copy of the situation for the incremented scenario
    modified_situation = situation.copy()
    
    # Modify the real estate taxes
    head_key = "head"
    period = "2026"
    if "real_estate_taxes" in modified_situation["people"][head_key]:
        current_taxes = modified_situation["people"][head_key]["real_estate_taxes"][period]
        modified_situation["people"][head_key]["real_estate_taxes"][period] = current_taxes + increment


    
    # Then calculate the modified situation
    modified_results = calculate_impacts(modified_situation, reform_params_dict, baseline_scenario)

    # Calculate marginal subsidy rates
    subsidy_rates = {}
    
    # For baseline scenario
    baseline_original = original_results["baseline"]  
    baseline_modified = modified_results["baseline"]  
    baseline_delta = baseline_modified - baseline_original
    
    baseline_subsidy = (-baseline_delta / increment) * 100
    subsidy_rates["baseline"] = baseline_subsidy

    # For reform scenario
    reform_original = baseline_original + original_results["selected_reform_impact"]
    reform_modified = baseline_modified + modified_results["selected_reform_impact"]
    reform_delta = reform_modified - reform_original
    
    reform_subsidy = (reform_delta / increment) * 100
    subsidy_rates["reform"] = reform_subsidy

    return subsidy_rates
