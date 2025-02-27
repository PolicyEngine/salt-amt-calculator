from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.reforms import PolicyReforms
import numpy as np
import pandas as pd
import streamlit as st


def create_situation_with_axes(
    state_code,
    employment_income,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
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
                "deductible_mortgage_interest": {"2026": deductible_mortgage_interest},
                "charitable_cash_donations": {"2026": charitable_cash_donations},
            }
        }
    }
    members = ["you"]

    if is_married:
        situation_with_axes["people"]["spouse"] = {
            "age": {"2026": 40},
        }
        members.append("spouse")

    for i in range(num_children):
        child_id = f"child_{i}"
        situation_with_axes["people"][child_id] = {
            "age": {"2026": child_ages[i]},
        }
        members.append(child_id)

    situation_with_axes.update(
        {
            "families": {"your family": {"members": members.copy()}},
            "marital_units": {"your marital unit": {"members": members.copy()}},
            "tax_units": {"your tax unit": {"members": members.copy()}},
            "spm_units": {"your household": {"members": members.copy()}},
            "households": {
                "your household": {
                    "members": members.copy(),
                    "state_name": {"2026": state_code},
                }
            },
            "axes": [
                [{"name": "real_estate_taxes", "count": 501, "min": 0, "max": 50000}]
            ],
        }
    )

    return situation_with_axes


def find_effective_salt_cap(situation_with_axes, reform_params_dict, baseline_scenario):
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
    if baseline_scenario == "Current Law":
        baseline_simulation = Simulation(situation=situation_with_axes)
    elif baseline_scenario == "Current Policy":
        current_policy_reform = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        reform = Reform.from_dict(current_policy_reform, country_id="us")
        baseline_simulation = Simulation(situation=situation_with_axes, reform=reform)
    else:
        raise ValueError(f"Invalid baseline scenario: {baseline_scenario}")
    baseline_amt = baseline_simulation.calculate("amt_base_tax", "2026")
    baseline_regular_tax = baseline_simulation.calculate(
        "regular_tax_before_credits", "2026"
    )
    filing_status = baseline_simulation.calculate("filing_status", "2026")[0]
    is_married = filing_status == 1
    real_estate_taxes = np.linspace(
        start=situation_with_axes["axes"][0][0]["min"],
        stop=situation_with_axes["axes"][0][0]["max"],
        num=situation_with_axes["axes"][0][0]["count"],
    )
    state_local_tax = baseline_simulation.calculate(
        "state_and_local_sales_or_income_tax", "2026"
    )
    total_salt = real_estate_taxes + state_local_tax
    results_df = pd.DataFrame(
        {
            "real_estate_taxes": real_estate_taxes,
            "state_local_tax": state_local_tax,
            "total_salt": total_salt,
            "baseline_regular_tax": baseline_regular_tax,
            "baseline_amt": baseline_amt,
        }
    )
    # Add single reform net income
    for reform_key, reform_params in reform_params_dict.items():
        try:
            reform_dict = PolicyReforms.policy_reforms(reform_params)
            reform = Reform.from_dict(reform_dict, country_id="us")
            reform_simulation = Simulation(situation=situation_with_axes, reform=reform)
            reform_regular_tax = reform_simulation.calculate(
                "regular_tax_before_credits", "2026"
            )
            reform_amt = reform_simulation.calculate("amt_base_tax", "2026")
            results_df["reform_regular_tax"] = reform_regular_tax
            results_df["reform_amt"] = reform_amt
            results_df["reform_state_local_tax"] = reform_simulation.calculate(
                "state_and_local_sales_or_income_tax", "2026"
            )
            results_df["reform_total_salt"] = (
                results_df["reform_state_local_tax"] + results_df["real_estate_taxes"]
            )
        except Exception as e:
            results_df["reform_regular_tax"] = None
            results_df["reform_amt"] = None
            results_df["reform_state_local_tax"] = None
            results_df["reform_total_salt"] = None
            # Print full DataFrame without truncation
        with pd.option_context(
            "display.max_rows", None, "display.max_columns", None, "display.width", None
        ):
            print("--------------------------------")
            print(results_df)

    baseline_crossover_mask = (
        results_df["baseline_amt"] > results_df["baseline_regular_tax"]
    )
    baseline_crossover = float("inf")
    if any(baseline_crossover_mask):
        # Get the first point where AMT exceeds regular tax
        crossover_idx = np.where(baseline_crossover_mask)[0][0]
        baseline_crossover = results_df["total_salt"].iloc[crossover_idx]

    # Find where AMT exceeds regular tax for reform
    reform_crossover_mask = results_df["reform_amt"] > results_df["reform_regular_tax"]
    reform_crossover = float("inf")
    if any(reform_crossover_mask):
        # Get the first point where AMT exceeds regular tax
        crossover_idx = np.where(reform_crossover_mask)[0][0]
        reform_crossover = results_df["reform_total_salt"].iloc[crossover_idx]
    # Get baseline SALT cap
    if baseline_scenario == "Current Law":
        baseline_salt_cap = float("inf")
    else:  # Current Policy
        baseline_salt_cap = (
            10_000
            if (is_married and st.session_state.policy_config["salt_marriage_bonus"])
            else 10_000
        )
    # Get reform SALT cap from policy config
    reform_salt_cap = float("inf")  # Default to uncapped
    if reform_params_dict:
        salt_cap_setting = st.session_state.policy_config["salt_cap"]
        if salt_cap_setting == "Current Policy ($10k)":
            reform_salt_cap = (
                20_000
                if (
                    is_married and st.session_state.policy_config["salt_marriage_bonus"]
                )
                else 10_000
            )
        elif salt_cap_setting == "$15k":
            reform_salt_cap = (
                30_000
                if (
                    is_married and st.session_state.policy_config["salt_marriage_bonus"]
                )
                else 15_000
            )
        # "Current Law (Uncapped)" will use the default float('inf')

        # Apply repeal if selected
        if st.session_state.policy_config["salt_repealed"]:
            reform_salt_cap = 0

    return {
        "baseline_salt_cap": min(baseline_salt_cap, baseline_crossover),
        "reform_salt_cap": min(reform_salt_cap, reform_crossover),
    }
