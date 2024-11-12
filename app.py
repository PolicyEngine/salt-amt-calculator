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
                if st.button("✕", key=f"remove_{reform_idx}", help="Remove this reform"):
                    st.session_state.reform_indexes.remove(reform_idx)
                    del st.session_state.reform_names[reform_idx]
                    st.rerun()
        
        # Create reform parameters using the imported function
        reform_params_dict[f"reform_{i+1}"] = create_policy_inputs(new_name)

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
    cols = st.columns(len(st.session_state.reform_indexes) + 1)
    
    # Display baseline
    with cols[0]:
        st.markdown("#### Baseline")
        st.markdown(f"Household income: **${results['baseline']:,.2f}**")
    
    # Display each reform
    for i, reform_idx in enumerate(st.session_state.reform_indexes):
        with cols[i + 1]:
            st.markdown(f"#### {st.session_state.reform_names[reform_idx]}")
            reform_impact = results[f'reform_{i+1}_impact']
            new_income = results['baseline'] + reform_impact
            
            st.markdown(f"New household income: **${new_income:,.2f}**")
            st.markdown(f"Change from baseline: **${reform_impact:,.2f}**")
            
            if reform_impact > 0:
                st.success("This reform would increase household income")
            elif reform_impact < 0:
                st.error("This reform would decrease household income")