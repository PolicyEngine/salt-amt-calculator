import streamlit as st
import numpy as np
import pandas as pd
from constants import CURRENT_POLICY_PARAMS
from personal_calculator.subsidy_rate import calculate_marginal_subsidy_rate


def _format_value(reform_params, key, label, default_value="N/A"):
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
        joint = (
            "Unlimited"
            if reform_params.get(key, {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get(key, {}).get('JOINT', 0):,.0f}"
        )
        other = (
            "Unlimited"
            if reform_params.get(key, {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get(key, {}).get('SINGLE', 0):,.0f}"
        )
        return f"Joint: {joint}<br>Other: {other}"
    except:
        return default_value


def _format_salt_caps(reform_params):
    return _format_value(reform_params, "salt_caps", "SALT Cap")


def _format_salt_phaseout(reform_params):
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
        if reform_params.get("salt_phase_out_rate", 0) > 0:
            rate = f"{reform_params.get('salt_phase_out_rate', 0)*100:.0f}%"
            joint = f"${reform_params.get('salt_phase_out_threshold_joint', 0):,.0f}"
            other = f"${reform_params.get('salt_phase_out_threshold_other', 0):,.0f}"
            return f"Rate: {rate}<br>Joint: {joint}<br>Other: {other}"
        return "N/A"
    except:
        return "Error"


def _format_amt_exemptions(reform_params):
    return _format_value(reform_params, "amt_exemptions", "AMT Exemption")


def _format_amt_phaseout(reform_params):
    return _format_value(reform_params, "amt_phase_outs", "AMT Phase-out")


def _format_tcja_provisions(reform_params):
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
        return (
            "Extended"
            if reform_params.get("other_tcja_provisions", False)
            else "Repealed"
        )
    except:
        return "Error"


def create_summary_table(
    baseline_income,
    session_state, 
    reform_params_dict, 
    baseline_scenario="Current Law"
):
    """Create a summary table comparing scenarios based on selected baseline"""
    
    # Get scenario names dynamically
    baseline_name = baseline_scenario
    reform_name = "Your Policy"

    # Create DataFrame for table
    data = {
        baseline_name: [
            f"${session_state.summary_results[baseline_name]:,.0f}",
            "$0",  # Baseline comparison
            f"{session_state.subsidy_rates['baseline']:.1f}%"
        ],
        reform_name: [
            f"${session_state.summary_results[reform_name]:,.0f}",
            f"${session_state.summary_results[reform_name] - session_state.summary_results[baseline_name]:,.0f}",
            f"{session_state.subsidy_rates['reform']:.1f}%"
        ],
    }

    # Create index for the rows
    index = [
        "Household Income",
        f"Change from {baseline_name}",
        "Marginal Subsidy Rate"
    ]

    df = pd.DataFrame(data, index=index)

    # Display table
    st.markdown("### Summary Table")

    # Use the full container width
    st.write(
        df.to_html(escape=False, classes=["dataframe", "full-width"]),
        unsafe_allow_html=True,
    )

    # Add CSS to make the table full width and improve formatting with dark mode support
    st.markdown(
        """
        <style>
        .full-width {
            width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        /* Light mode styles */
        [data-theme="light"] .dataframe {
            border: 1px solid #e1e4e8;
        }
        [data-theme="light"] .dataframe td {
            white-space: pre-wrap !important;
            text-align: left !important;
            padding: 8px !important;
            border: 1px solid #e1e4e8;
        }
        [data-theme="light"] .dataframe th {
            text-align: left !important;
            padding: 8px !important;
            background-color: #f0f2f6 !important;
            border: 1px solid #e1e4e8;
            color: #1f2937;
        }
        
        /* Dark mode styles */
        [data-theme="dark"] .dataframe {
            border: 1px solid #4a5568;
        }
        [data-theme="dark"] .dataframe td {
            white-space: pre-wrap !important;
            text-align: left !important;
            padding: 8px !important;
            border: 1px solid #4a5568;
            background-color: #262730;
        }
        [data-theme="dark"] .dataframe th {
            text-align: left !important;
            padding: 8px !important;
            background-color: #1e1e1e !important;
            border: 1px solid #4a5568;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
