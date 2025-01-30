from policyengine_us import Simulation
import numpy as np
from personal_calculator.calculator import calculate_impacts
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import get_reform_params_from_config


def _calculate_income(situation, policy_params):
    results = calculate_impacts(situation, policy_params)
    return results["current_law"] + results.get("reform_current_policy_impact", 0)


def calculate_subsidy_rate(situation, period, policy_config):
    """Calculate the marginal subsidy rates for property taxes under different policies"""

    # Calculate baseline net incomes for each policy
    current_law_base = _calculate_income(situation, {})
    current_policy_base = _calculate_income(situation, CURRENT_POLICY_PARAMS)
    reform_params = get_reform_params_from_config(policy_config)
    your_policy_base = _calculate_income(situation, {"selected_reform": reform_params})

    # Create modified situation with increased real estate taxes
    modified_situation = situation.copy()
    delta = 500.0  # $500 increment in real estate taxes

    # Modify the real estate taxes
    head_key = "head"
    if "real_estate_taxes" in modified_situation["people"][head_key]:
        current_taxes = modified_situation["people"][head_key]["real_estate_taxes"][
            period
        ]
        modified_situation["people"][head_key]["real_estate_taxes"][period] = (
            current_taxes + delta
        )

    # Calculate modified net incomes for each policy
    current_law_mod = _calculate_income(modified_situation, {})
    current_policy_mod = _calculate_income(modified_situation, CURRENT_POLICY_PARAMS)
    your_policy_mod = _calculate_income(
        modified_situation, {"selected_reform": reform_params}
    )

    # Calculate subsidy rates
    subsidy_rates = {
        "Current Law": float(current_law_mod - current_law_base) / delta,
        "Current Policy": float(current_policy_mod - current_policy_base) / delta,
        "Your Policy": float(your_policy_mod - your_policy_base) / delta,
    }

    return subsidy_rates
