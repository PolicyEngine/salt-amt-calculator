import streamlit as st
import pandas as pd
import numpy as np


def _format_policy_parameters(reform_params):
    """
    Formats the policy parameters for a single reform.
    """
    # Handle Current Law case
    if reform_params == "Pre-TCJA provisions":
        return reform_params

    # Handle missing or differently structured parameters
    try:
        # Format SALT caps
        salt_joint = (
            "Unlimited"
            if reform_params.get("salt_caps", {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get('salt_caps', {}).get('JOINT', 0):,.0f}"
        )
        salt_other = (
            "Unlimited"
            if reform_params.get("salt_caps", {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get('salt_caps', {}).get('SINGLE', 0):,.0f}"
        )

        # Format SALT phase-out parameters
        salt_phase_out_rate = f"{reform_params.get('salt_phase_out_rate', 0)*100:.0f}%"
        salt_phase_out_threshold_joint = (
            f"${reform_params.get('salt_phase_out_threshold_joint', 0):,.0f}"
        )
        salt_phase_out_threshold_other = (
            f"${reform_params.get('salt_phase_out_threshold_other', 0):,.0f}"
        )

        # Format AMT exemptions
        amt_ex_joint = (
            "Unlimited"
            if reform_params.get("amt_exemptions", {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get('amt_exemptions', {}).get('JOINT', 0):,.0f}"
        )
        amt_ex_other = (
            "Unlimited"
            if reform_params.get("amt_exemptions", {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get('amt_exemptions', {}).get('SINGLE', 0):,.0f}"
        )

        # Format AMT phase-outs
        amt_po_joint = (
            "Unlimited"
            if reform_params.get("amt_phase_outs", {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get('amt_phase_outs', {}).get('JOINT', 0):,.0f}"
        )
        amt_po_other = (
            "Unlimited"
            if reform_params.get("amt_phase_outs", {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get('amt_phase_outs', {}).get('SINGLE', 0):,.0f}"
        )

        return (
            f"SALT Cap:<br>"
            f"• Joint: {salt_joint}<br>"
            f"• Other: {salt_other}<br>"
            f"SALT Phase-out:<br>"
            f"• Rate: {salt_phase_out_rate}<br>"
            f"• Joint Threshold: {salt_phase_out_threshold_joint}<br>"
            f"• Other Threshold: {salt_phase_out_threshold_other}<br>"
            f"AMT Exemption:<br>"
            f"• Joint: {amt_ex_joint}<br>"
            f"• Other: {amt_ex_other}<br>"
            f"AMT Phase-out:<br>"
            f"• Joint: {amt_po_joint}<br>"
            f"• Other: {amt_po_other}"
        )
    except Exception as e:
        # If there's any error in formatting, return a simple string
        return "Error formatting parameters"


def create_summary_table(current_law_income, session_state, reform_params_dict):
    """Create a summary table comparing current law, current policy, and selected policy"""
    import pandas as pd
    import streamlit as st

    # Create DataFrame for table
    data = {
        "Situation": ["Current Law", "Current Policy", "Selected Policy"],
        "Policy Parameters": [
            "Pre-TCJA provisions",
            _format_policy_parameters(
                {
                    "salt_caps": {
                        "JOINT": 10_000,
                        "SEPARATE": 5_000,
                        "SINGLE": 10_000,
                        "HEAD_OF_HOUSEHOLD": 10_000,
                        "SURVIVING_SPOUSE": 10_000,
                    },
                    "amt_exemptions": {
                        "JOINT": 140_565,
                        "SEPARATE": 70_283,
                        "SINGLE": 90_394,
                        "HEAD_OF_HOUSEHOLD": 90_394,
                        "SURVIVING_SPOUSE": 90_394,
                    },
                    "amt_phase_outs": {
                        "JOINT": 1_285_409,
                        "SEPARATE": 642_705,
                        "SINGLE": 642_705,
                        "HEAD_OF_HOUSEHOLD": 642_705,
                        "SURVIVING_SPOUSE": 642_705,
                    },
                    "salt_phase_out_rate": 0,
                    "salt_phase_out_threshold_joint": 0,
                    "salt_phase_out_threshold_other": 0,
                }
            ),
            _format_policy_parameters(reform_params_dict["selected_reform"]),
        ],
        "Household Income": [
            current_law_income,
            session_state.summary_results["Current Policy"],
            session_state.summary_results["Selected Policy"],
        ],
        "Change from Current Law": [
            0,
            session_state.summary_results["Current Policy"] - current_law_income,
            session_state.summary_results["Selected Policy"] - current_law_income,
        ],
        "Change from Current Policy": [
            session_state.summary_results["Current Law"]
            - session_state.summary_results["Current Policy"],
            0,
            session_state.summary_results["Selected Policy"]
            - session_state.summary_results["Current Policy"],
        ],
    }

    df = pd.DataFrame(data)

    # Format numeric columns
    df["Household Income"] = df["Household Income"].apply(lambda x: f"${x:,.0f}")
    df["Change from Current Law"] = df["Change from Current Law"].apply(
        lambda x: f"${x:,.0f}" if x >= 0 else f"-${-x:,.0f}"
    )
    df["Change from Current Policy"] = df["Change from Current Policy"].apply(
        lambda x: f"${x:,.0f}" if x >= 0 else f"-${-x:,.0f}"
    )

    # Display table
    st.markdown("### Summary Table")

    # Use the full container width
    st.write(
        df.to_html(escape=False, index=False, classes=["dataframe", "full-width"]),
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
            text-align: center !important;
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
            text-align: center !important;
            padding: 8px !important;
            background-color: #1e1e1e !important;
            border: 1px solid #4a5568;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
