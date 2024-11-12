# app.py
import streamlit as st
from situation import create_situation
from calculator import calculate_impacts
from inputs import create_personal_inputs
from policy_parameters import create_policy_inputs

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
if 'num_reforms' not in st.session_state:
    st.session_state.num_reforms = 2  # Start with 2 reforms

# Add/Remove reform buttons in a row
col1, col2 = st.columns([4, 1])
with col2:
    # Add reform button
    if st.button("Add Reform") and st.session_state.num_reforms < 5:
        st.session_state.num_reforms += 1
    
    # Remove reform button
    if st.button("Remove Reform") and st.session_state.num_reforms > 1:
        st.session_state.num_reforms -= 1

# Create tabs for all reforms
reform_tabs = st.tabs([f"Reform Scenario {i+1}" for i in range(st.session_state.num_reforms)])

# Dictionary to store all reform parameters
reform_params_dict = {}

# Create inputs for each reform
for i, tab in enumerate(reform_tabs):
    with tab:
        reform_params_dict[f"reform_{i+1}"] = create_policy_inputs(f"Reform {i+1}")

if st.button("Calculate Impacts"):
    # Create situation based on inputs
    situation = create_situation(
        state_code=personal_inputs["state_code"],
        filing_status=personal_inputs["filing_status"],
        employment_income=personal_inputs["employment_income"],
        head_age=personal_inputs["head_age"],
        is_married=personal_inputs["is_married"],
        spouse_age=personal_inputs["spouse_age"],
        num_children=personal_inputs["num_children"],
        child_ages=personal_inputs["child_ages"],
        state_and_local_sales_or_income_tax=personal_inputs["state_and_local_sales_or_income_tax"],
        qualified_dividend_income=personal_inputs["qualified_dividend_income"],
        long_term_capital_gains=personal_inputs["long_term_capital_gains"],
        short_term_capital_gains=personal_inputs["short_term_capital_gains"],
    )
    
    # Calculate and display results for all reforms
    results = calculate_impacts(situation, reform_params_dict)
    
    # Display results in a nice format
    st.markdown("### Results")
    
    # Create columns for results - baseline plus all reforms
    cols = st.columns(st.session_state.num_reforms + 1)
    
    # Display baseline
    with cols[0]:
        st.markdown("#### Baseline")
        st.markdown(f"Household income: **${results['baseline']:,.2f}**")
    
    # Display each reform
    for i in range(st.session_state.num_reforms):
        with cols[i + 1]:
            st.markdown(f"#### Reform Scenario {i+1}")
            reform_impact = results[f'reform_{i+1}_impact']
            new_income = results['baseline'] + reform_impact
            
            st.markdown(f"New household income: **${new_income:,.2f}**")
            st.markdown(f"Change from baseline: **${reform_impact:,.2f}**")
            
            if reform_impact > 0:
                st.success("This reform would increase household income")
            elif reform_impact < 0:
                st.error("This reform would decrease household income")
