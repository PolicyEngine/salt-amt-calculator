import streamlit as st
import pandas as pd
import numpy as np


def _format_policy_parameters(reform_params):
    """
    Formats the policy parameters for a single reform.
    """
    # Format SALT caps
    salt_joint = (
        "Unlimited"
        if reform_params["salt_caps"]["JOINT"] == np.inf
        else f"${reform_params['salt_caps']['JOINT']:,.0f}"
    )
    salt_other = (
        "Unlimited"
        if reform_params["salt_caps"]["SINGLE"] == np.inf
        else f"${reform_params['salt_caps']['SINGLE']:,.0f}"
    )

    # Format SALT phase-out parameters
    salt_phase_out_rate = f"{reform_params['salt_phase_out_rate']*100:.0f}%"
    salt_phase_out_threshold_joint = (
        f"${reform_params['salt_phase_out_threshold_joint']:,.0f}"
    )
    salt_phase_out_threshold_other = (
        f"${reform_params['salt_phase_out_threshold_other']:,.0f}"
    )

    # Format AMT exemptions
    amt_ex_joint = (
        "Unlimited"
        if reform_params["amt_exemptions"]["JOINT"] == np.inf
        else f"${reform_params['amt_exemptions']['JOINT']:,.0f}"
    )
    amt_ex_other = (
        "Unlimited"
        if reform_params["amt_exemptions"]["SINGLE"] == np.inf
        else f"${reform_params['amt_exemptions']['SINGLE']:,.0f}"
    )

    # Format AMT phase-outs
    amt_po_joint = (
        "Unlimited"
        if reform_params["amt_phase_outs"]["JOINT"] == np.inf
        else f"${reform_params['amt_phase_outs']['JOINT']:,.0f}"
    )
    amt_po_other = (
        "Unlimited"
        if reform_params["amt_phase_outs"]["SINGLE"] == np.inf
        else f"${reform_params['amt_phase_outs']['SINGLE']:,.0f}"
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


def create_summary_table(current_law_income, st_session_state, reform_params_dict):
    """Creates and displays a summary table of all reforms and their impacts."""
    st.markdown("### Detailed Summary")

    # Initialize lists for DataFrame
    table_data = []

    # Add current law
    table_data.append(
        {
            "Reform": "Current Law",
            "Policy Parameters": (
                "SALT Cap: Unlimited<br>"
                "SALT Phase-out:<br>"
                "• Rate: 0%<br>"
                "• Joint Threshold: $0<br>"
                "• Other Threshold: $0<br>"
                "AMT Exemption:<br>"
                "• Joint: $109,700<br>"
                "• Other: $70,500<br>"
                "AMT Phase-out:<br>"
                "• Joint: $209,000<br>"
                "• Other: $156,700"
            ),
            "Household Income": f"${current_law_income:,.2f}",
            "Change from Current Law": "$0",
            "Percent Change": "0%",
        }
    )

    # Add current policy
    current_policy_income = st_session_state.summary_results["Current Policy"]
    current_policy_impact = current_policy_income - current_law_income

    table_data.append(
        {
            "Reform": "Current Policy",
            "Policy Parameters": (
                "SALT Cap:<br>"
                "• Joint: $10,000<br>"
                "• Other: $10,000<br>"
                "SALT Phase-out:<br>"
                "• Rate: 0%<br>"
                "• Joint Threshold: $0<br>"
                "• Other Threshold: $0<br>"
                "AMT Exemption:<br>"
                "• Joint: $140,565<br>"
                "• Other: $90,394<br>"
                "AMT Phase-out:<br>"
                "• Joint: $1,285,409<br>"
                "• Other: $642,705"
            ),
            "Household Income": f"${current_policy_income:,.2f}",
            "Change from Current Law": f"${current_policy_impact:,.2f}",
            "Percent Change": f"{current_policy_impact/current_law_income:,.1%}",
        }
    )

    # Add each reform
    for i, reform_idx in enumerate(st_session_state.reform_indexes):
        reform_name = st_session_state.reform_names[reform_idx]
        reform_params = reform_params_dict[f"reform_{i+1}"]

        policy_text = _format_policy_parameters(reform_params)

        # Get reform outcome from summary results
        reform_income = st_session_state.summary_results[reform_name]
        reform_impact = reform_income - current_law_income

        table_data.append(
            {
                "Reform": reform_name,
                "Policy Parameters": policy_text,
                "Household Income": f"${reform_income:,.2f}",
                "Change from Current Law": f"${reform_impact:,.2f}",
                "Percent Change": f"{reform_impact/current_law_income:,.1%}",
            }
        )

    # Create and display the table
    _display_formatted_table(table_data)


def _display_formatted_table(table_data):
    """
    Creates and displays a formatted HTML table from the provided data.
    """
    # Create DataFrame
    df = pd.DataFrame(table_data)

    # Custom CSS for table formatting
    st.markdown(
        """
        <style>
        .table-container {
            margin: 1rem 0;
        }
        .dataframe {
            width: 100% !important;
        }
        .dataframe td, .dataframe th {
            text-align: left !important;
            padding: 12px !important;
            vertical-align: top !important;
            line-height: 1.4 !important;
        }
        .dataframe th {
            background-color: #f8f9fa !important;
            font-weight: 600 !important;
        }
        .dataframe tr:nth-child(even) {
            background-color: #f8f9fa !important;
        }
        .dataframe tr:hover {
            background-color: #f0f0f0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Convert DataFrame to HTML with preserved line breaks
    html_table = df.to_html(escape=False, index=False)

    # Display table
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
