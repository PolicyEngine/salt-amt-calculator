import streamlit as st
import numpy as np
import pandas as pd


def _format_salt_caps(reform_params):
    """Format just the SALT cap parameters."""
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
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
        return f"Joint: {salt_joint}<br>Other: {salt_other}"
    except:
        return "Error"


def _format_salt_phaseout(reform_params):
    """Format just the SALT phase-out parameters."""
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
    """Format just the AMT exemption parameters."""
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
        joint = (
            "Unlimited"
            if reform_params.get("amt_exemptions", {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get('amt_exemptions', {}).get('JOINT', 0):,.0f}"
        )
        other = (
            "Unlimited"
            if reform_params.get("amt_exemptions", {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get('amt_exemptions', {}).get('SINGLE', 0):,.0f}"
        )
        return f"Joint: {joint}<br>Other: {other}"
    except:
        return "Error"


def _format_amt_phaseout(reform_params):
    """Format just the AMT phase-out parameters."""
    if reform_params == "Pre-TCJA provisions":
        return "Pre-TCJA"

    try:
        joint = (
            "Unlimited"
            if reform_params.get("amt_phase_outs", {}).get("JOINT", 0) == np.inf
            else f"${reform_params.get('amt_phase_outs', {}).get('JOINT', 0):,.0f}"
        )
        other = (
            "Unlimited"
            if reform_params.get("amt_phase_outs", {}).get("SINGLE", 0) == np.inf
            else f"${reform_params.get('amt_phase_outs', {}).get('SINGLE', 0):,.0f}"
        )
        return f"Joint: {joint}<br>Other: {other}"
    except:
        return "Error"


def create_summary_table(
    current_law_income, session_state, reform_params_dict, subsidy_rates=None
):
    """Create a summary table comparing current law, current policy, and your policy"""

    # Create DataFrame for table
    data = {
        "Current Law": [
            "Joint: Unlimited<br>Other: Unlimited",  # SALT Cap
            "N/A",  # SALT Phase-out
            "Joint: $109,700<br>Other: $70,500",  # AMT Exemption
            "Joint: $209,000<br>Other: $156,700",  # AMT Phase-out
            f"${current_law_income:,.0f}",  # Household Income
            "$0",  # Change from Current Law
            f"${session_state.summary_results['Current Law'] - session_state.summary_results['Current Policy']:,.0f}",  # Change from Current Policy
        ],
        "Current Policy": [
            "Joint: $10,000<br>Other: $10,000",
            "N/A",
            "Joint: $140,565<br>Other: $90,394",
            "Joint: $1,285,409<br>Other: $642,705",
            f"${session_state.summary_results['Current Policy']:,.0f}",
            f"${session_state.summary_results['Current Policy'] - current_law_income:,.0f}",
            "$0",
        ],
        "Your Policy": [
            _format_salt_caps(reform_params_dict["selected_reform"]),
            _format_salt_phaseout(reform_params_dict["selected_reform"]),
            _format_amt_exemptions(reform_params_dict["selected_reform"]),
            _format_amt_phaseout(reform_params_dict["selected_reform"]),
            f"${session_state.summary_results['Your Policy']:,.0f}",
            f"${session_state.summary_results['Your Policy'] - current_law_income:,.0f}",
            f"${session_state.summary_results['Your Policy'] - session_state.summary_results['Current Policy']:,.0f}",
        ],
    }

    # Create index for the rows
    index = [
        "SALT Cap",
        "SALT Phase-out",
        "AMT Exemption",
        "AMT Phase-out",
        "Household Income",
        "Change from Current Law",
        "Change from Current Policy",
    ]

    df = pd.DataFrame(data, index=index)

    # Add subsidy rates if provided
    if subsidy_rates:
        df.loc["Marginal Subsidy Rate"] = [
            f"{subsidy_rates.get('Current Law', 0):.2%}",
            f"{subsidy_rates.get('Current Policy', 0):.2%}",
            f"{subsidy_rates.get('Your Policy', 0):.2%}",
        ]

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
