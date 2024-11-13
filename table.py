import streamlit as st
import pandas as pd
import numpy as np

def create_summary_table(baseline_income, st_session_state, reform_params_dict):
    """
    Creates and displays a summary table of all reforms and their impacts.
    """
    st.markdown("### Detailed Summary")

    # Initialize lists for DataFrame
    table_data = []

    # Add baseline
    table_data.append(
        {
            "Reform": "Baseline",
            "Policy Parameters": (
                "SALT Cap: Unlimited <br>"
                "AMT Exemption:<br>"
                "• Joint: $109,700<br>"
                "• Other: $70,500<br>"
                "AMT Phase-out:<br>"
                "• Joint: $209,000<br>"
                "• Other: $156,700"
            ),
            "Household Income": f"${baseline_income:,.2f}",
            "Change from Baseline": "$0",
            "Percent Change": "0%",
        }
    )

    # Add each reform
    for i, reform_idx in enumerate(st_session_state.reform_indexes):
        reform_name = st_session_state.reform_names[reform_idx]
        reform_params = reform_params_dict[f"reform_{i+1}"]

        policy_text = _format_policy_parameters(reform_params)
        
        # Get reform outcome from summary results
        reform_income = st_session_state.summary_results[reform_name]
        reform_impact = reform_income - baseline_income

        table_data.append(
            {
                "Reform": reform_name,
                "Policy Parameters": policy_text,
                "Household Income": f"${reform_income:,.2f}",
                "Change from Baseline": f"${reform_impact:,.2f}",
                "Percent Change": f"{reform_impact/baseline_income:,.1%}",
            }
        )

    # Create and display the table
    _display_formatted_table(table_data)

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
        f"AMT Exemption:<br>"
        f"• Joint: {amt_ex_joint}<br>"
        f"• Other: {amt_ex_other}<br>"
        f"AMT Phase-out:<br>"
        f"• Joint: {amt_po_joint}<br>"
        f"• Other: {amt_po_other}"
    )

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