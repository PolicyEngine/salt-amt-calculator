import streamlit as st
import numpy as np
import pandas as pd
from constants import CURRENT_POLICY_PARAMS


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
    # subsidy_rates=None,
    baseline_scenario="Current Law"
):
    """Create a summary table comparing scenarios based on selected baseline"""
    
    # Get scenario names dynamically
    baseline_name = baseline_scenario
    reform_name = "Your Policy"
    comparison_name = "Current Policy" if baseline_scenario == "Current Law" else "Current Law"

    # Determine parameters for each scenario
    baseline_params = {} if baseline_scenario == "Current Law" else CURRENT_POLICY_PARAMS
    comparison_params = CURRENT_POLICY_PARAMS if baseline_scenario == "Current Law" else {}
    reform_params = reform_params_dict["selected_reform"]

    # Create DataFrame for table
    data = {
        baseline_name: [
            _format_salt_caps(baseline_params),
            _format_salt_phaseout(baseline_params),
            _format_amt_exemptions(baseline_params),
            _format_amt_phaseout(baseline_params),
            _format_tcja_provisions(baseline_params),
            f"${session_state.summary_results[baseline_name]:,.0f}",
            "$0",  # Baseline comparison
            f"${session_state.summary_results.get(comparison_name, 0) - session_state.summary_results[baseline_name]:,.0f}",
        ],
        reform_name: [
            _format_salt_caps(reform_params),
            _format_salt_phaseout(reform_params),
            _format_amt_exemptions(reform_params),
            _format_amt_phaseout(reform_params),
            _format_tcja_provisions(reform_params),
            f"${session_state.summary_results[reform_name]:,.0f}",
            f"${session_state.summary_results[reform_name] - session_state.summary_results[baseline_name]:,.0f}",
            f"${session_state.summary_results[reform_name] - session_state.summary_results.get(comparison_name, 0):,.0f}",
        ],
        comparison_name: [
            _format_salt_caps(comparison_params),
            _format_salt_phaseout(comparison_params),
            _format_amt_exemptions(comparison_params),
            _format_amt_phaseout(comparison_params),
            _format_tcja_provisions(comparison_params),
            f"${session_state.summary_results.get(comparison_name, 0):,.0f}",
            f"${session_state.summary_results.get(comparison_name, 0) - session_state.summary_results[baseline_name]:,.0f}",
            "$0"
        ]
    }

    # Create index for the rows
    index = [
        "SALT Cap",
        "SALT Phase-out",
        "AMT Exemption",
        "AMT Phase-out",
        "Other TCJA Provisions",
        "Household Income",
        f"Change from {baseline_name}",
        f"Change from {comparison_name}"
    ]

    df = pd.DataFrame(data, index=index)

    # # Update subsidy rate display
    # if subsidy_rates:
    #     df.loc["Marginal Subsidy Rate"] = [
    #         f"{subsidy_rates.get(baseline_name, 0):.0%}",
    #         f"{subsidy_rates.get(reform_name, 0):.0%}",
    #     ]
    #     if baseline_scenario == "Current Law":
    #         df.loc["Marginal Subsidy Rate"].append(f"{subsidy_rates.get('Current Policy', 0):.0%}")

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
