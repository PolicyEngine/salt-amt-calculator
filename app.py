import streamlit as st
from situation import create_situation
from calculator import calculate_impacts
from inputs import create_personal_inputs
from policy_parameters import create_policy_inputs
from chart import create_reform_comparison_graph, initialize_results_tracking, update_results, reset_results
import numpy as np

# Set up the Streamlit page
st.set_page_config(page_title="SALT Cap Policy Impact Calculator", page_icon="📊", layout="wide")

# Title and description
st.title("SALT / AMT Policy Impact Calculator")
st.markdown("""
This calculator compares different SALT cap and AMT reform scenarios against the baseline. 
Input your household characteristics and the parameters for each reform below.
""")

# Get personal inputs
personal_inputs = create_personal_inputs()

# Policy Parameters Section
st.markdown("### Policy Parameters")

# Initialize session state for tracking reforms if it doesn't exist
if 'reform_indexes' not in st.session_state:
    st.session_state.reform_indexes = [0, 1]  # Start with 2 reforms

# Initialize reform names if they don't exist
if 'reform_names' not in st.session_state:
    st.session_state.reform_names = {idx: f"Reform {idx+1}" for idx in st.session_state.reform_indexes}

# Add reform button right under the Policy Parameters header, left-aligned
col1, col2 = st.columns([1, 8])
with col1:
    if len(st.session_state.reform_indexes) < 5:
        if st.button("Add Reform"):
            next_index = max(st.session_state.reform_indexes) + 1
            st.session_state.reform_indexes.append(next_index)
            st.session_state.reform_names[next_index] = f"Reform {next_index+1}"
            st.rerun()

# Create columns for reforms based on how many we have
reform_cols = st.columns(len(st.session_state.reform_indexes))
reform_params_dict = {}

# Create inputs for each reform in columns
for i, (col, reform_idx) in enumerate(zip(reform_cols, st.session_state.reform_indexes)):
    with col:
        # Create a single row for name and remove button
        cols = st.columns([6, 1])
        with cols[0]:
            new_name = st.text_input(
                "Reform Name",
                value=st.session_state.reform_names[reform_idx],
                key=f"name_{reform_idx}",
                label_visibility="collapsed"
            )
            st.session_state.reform_names[reform_idx] = new_name
        
        with cols[1]:
            if len(st.session_state.reform_indexes) > 1:
                # Ensure unique key for remove button
                remove_key = f"remove_reform_{reform_idx}_{i}"
                if st.button("✕", key=remove_key, help="Remove this reform"):
                    st.session_state.reform_indexes.remove(reform_idx)
                    reform_name = st.session_state.reform_names[reform_idx]
                    del st.session_state.reform_names[reform_idx]
                    st.rerun()
        
        # Create reform parameters using the imported function
        reform_params_dict[f"reform_{i+1}"] = create_policy_inputs(new_name)

# Initialize results tracking in session state if not exists
if 'results_df' not in st.session_state:
    st.session_state.results_df, st.session_state.summary_results = initialize_results_tracking()

# Create columns for calculate button alignment
calc_col1, calc_col2 = st.columns([1, 8])
with calc_col1:
    calculate_clicked = st.button("Calculate Impacts", use_container_width=True)

if calculate_clicked:
    # Reset results to start fresh
    reset_results()
    
    # Create situation based on inputs
    situation = create_situation(
        state_code=personal_inputs["state_code"],
        filing_status=personal_inputs["filing_status"],
        employment_income=personal_inputs["employment_income"],
        spouse_income=personal_inputs["spouse_income"],
        head_age=personal_inputs["head_age"],
        is_married=personal_inputs["is_married"],
        spouse_age=personal_inputs["spouse_age"],
        num_children=personal_inputs["num_children"],
        child_ages=personal_inputs["child_ages"],
        state_and_local_sales_or_income_tax=personal_inputs["state_and_local_sales_or_income_tax"],
        qualified_dividend_income=personal_inputs["qualified_dividend_income"],
        long_term_capital_gains=personal_inputs["long_term_capital_gains"],
        short_term_capital_gains=personal_inputs["short_term_capital_gains"],
        real_estate_taxes=personal_inputs["real_estate_taxes"]
    )
    
    # Display results in a nice format
    st.markdown("### Results")

    # Create placeholder for chart and status message
    chart_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Calculate baseline first
    status_placeholder.info("Calculating baseline...")
    results = calculate_impacts(situation, {})
    baseline_income = results['baseline']
    
    # Update baseline results
    st.session_state.results_df, st.session_state.summary_results = update_results(
        st.session_state.results_df,
        st.session_state.summary_results,
        "Baseline",
        baseline_income
    )
    
    # Update chart with baseline
    fig = create_reform_comparison_graph(st.session_state.summary_results)
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Create columns for detailed results
    cols = st.columns(len(st.session_state.reform_indexes) + 1)
    
    # Display baseline details
    with cols[0]:
        st.markdown("#### Baseline")
        st.markdown(f"Household income: **${baseline_income:,.2f}**")
    
    # Calculate and display each reform sequentially
    for i, reform_idx in enumerate(st.session_state.reform_indexes):
        reform_name = st.session_state.reform_names[reform_idx]
        status_placeholder.info(f"Calculating {reform_name}...")
        
        # Calculate single reform
        reform_results = calculate_impacts(situation, {f"reform_{i+1}": reform_params_dict[f"reform_{i+1}"]})
        reform_impact = reform_results[f'reform_{i+1}_impact']
        new_income = baseline_income + reform_impact
        
        # Update results tracking
        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            reform_name,
            new_income
        )
        
        # Update chart after each reform
        fig = create_reform_comparison_graph(st.session_state.summary_results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Display detailed results for this reform
        with cols[i + 1]:
            st.markdown(f"#### {reform_name}")
            st.markdown(f"New household income: **${new_income:,.2f}**")
            st.markdown(f"Change from baseline: **${reform_impact:,.2f}**")
            
            if reform_impact > 0:
                st.success("This reform would increase household income")
            elif reform_impact < 0:
                st.error("This reform would decrease household income")
    
    # Clear status message when complete
    status_placeholder.empty()

# Create summary table
    st.markdown("### Detailed Summary")
    
    import pandas as pd
    
    # Initialize lists for DataFrame
    table_data = []
    
    # Add baseline
    table_data.append({
        "Reform": "Baseline",
        "Policy Parameters": (
            "SALT Cap: $10,000 (all filers)<br>"
            "AMT Exemption:<br>"
            "• Joint: $140,565<br>"
            "• Other: $90,394<br>"
            "AMT Phase-out:<br>"
            "• Joint: $1,285,409<br>"
            "• Other: $642,705"
        ),
        "Household Income": f"${baseline_income:,.2f}",
        "Change from Baseline": "$0",
        "Percent Change": "0%"
    })
    
    # Add each reform
    for i, reform_idx in enumerate(st.session_state.reform_indexes):
        reform_name = st.session_state.reform_names[reform_idx]
        reform_params = reform_params_dict[f"reform_{i+1}"]
        
        # Format policy parameters
        salt_joint = "Unlimited" if reform_params["salt_caps"]["JOINT"] == np.inf else f"${reform_params['salt_caps']['JOINT']:,.0f}"
        salt_other = "Unlimited" if reform_params["salt_caps"]["SINGLE"] == np.inf else f"${reform_params['salt_caps']['SINGLE']:,.0f}"
        
        amt_ex_joint = "Unlimited" if reform_params["amt_exemptions"]["JOINT"] == np.inf else f"${reform_params['amt_exemptions']['JOINT']:,.0f}"
        amt_ex_other = "Unlimited" if reform_params["amt_exemptions"]["SINGLE"] == np.inf else f"${reform_params['amt_exemptions']['SINGLE']:,.0f}"
        
        amt_po_joint = "Unlimited" if reform_params["amt_phase_outs"]["JOINT"] == np.inf else f"${reform_params['amt_phase_outs']['JOINT']:,.0f}"
        amt_po_other = "Unlimited" if reform_params["amt_phase_outs"]["SINGLE"] == np.inf else f"${reform_params['amt_phase_outs']['SINGLE']:,.0f}"
        
        policy_text = (
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
        
        # Get reform outcome from summary results
        reform_income = st.session_state.summary_results[reform_name]
        reform_impact = reform_income - baseline_income
        
        table_data.append({
            "Reform": reform_name,
            "Policy Parameters": policy_text,
            "Household Income": f"${reform_income:,.2f}",
            "Change from Baseline": f"${reform_impact:,.2f}",
            "Percent Change": f"{reform_impact/baseline_income:,.1%}"
        })
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Custom CSS to control table width and text wrapping
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    # Convert DataFrame to HTML with preserved line breaks
    html_table = df.to_html(escape=False, index=False)
    
    # Display table
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)