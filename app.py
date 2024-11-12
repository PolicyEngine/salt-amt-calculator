import streamlit as st
from situation import create_situation
from calculator import calculate_impacts

# Set up the Streamlit page
st.set_page_config(page_title="SALT Cap Policy Impact Calculator", page_icon="📊", layout="wide")

# Title and description
st.title("SALT / AMT Policy Impact Calculator")
st.markdown("""
This calculator compares two different SALT cap reform scenarios against the baseline. 
Input your household characteristics and the parameters for each reform below.
""")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Household Characteristics")
    
    # State selector
    state_codes = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    state_code = st.selectbox("State", state_codes, index=state_codes.index("CA"))
    
    # Filing status selector
    filing_statuses = ["SINGLE", "HEAD_OF_HOUSEHOLD", "JOINT", "SEPARATE", "SURVIVING_SPOUSE"]
    filing_status = st.selectbox("Filing Status", filing_statuses)
    
    # Income input
    employment_income = st.number_input(
        "Employment Income ($)",
        min_value=0,
        max_value=1000000,
        value=50000,
        step=1000,
    )
    
    # Head age
    head_age = st.number_input("Age of Household Head", min_value=18, max_value=100, value=35)

with col2:
    st.markdown("### Family Structure")
    
    # Marriage checkbox
    is_married = st.checkbox("Married")
    
    # Spouse age (only shown if married)
    spouse_age = None
    if is_married:
        spouse_age = st.number_input("Age of Spouse", min_value=18, max_value=100, value=35)
    
    # Number of children
    num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
    
    # Child ages (only shown if there are children)
    child_ages = []
    if num_children > 0:
        st.markdown("#### Child Ages")
        for i in range(num_children):
            age = st.number_input(f"Age of Child {i+1}", min_value=0, max_value=18, value=5)
            child_ages.append(age)

st.markdown("### Policy Parameters")

# Create tabs for the two reforms
tab1, tab2 = st.tabs(["Reform Scenario 1", "Reform Scenario 2"])

def create_policy_inputs(prefix):
    """Create inputs for all policy parameters with collapsible sections"""
    reform_params = {
        "salt_caps": {},
        "amt_exemptions": {},
        "amt_phase_outs": {}
    }
    
    # SALT Cap Section
    with st.expander("SALT Deduction Caps", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            reform_params["salt_caps"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_single"
            )
            
            reform_params["salt_caps"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_hoh"
            )
            
            reform_params["salt_caps"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer Cap ($)",
                min_value=0,
                max_value=200_000,
                value=20_000,
                step=1_000,
                key=f"{prefix}_salt_joint"
            )

        with col2:
            reform_params["salt_caps"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately Cap ($)",
                min_value=0,
                max_value=100_000,
                value=5_000,
                step=1_000,
                key=f"{prefix}_salt_separate"
            )
            
            reform_params["salt_caps"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_survivor"
            )
    
    # AMT Exemption Amount Section
    with st.expander("AMT Exemption Amounts", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            reform_params["amt_exemptions"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer AMT Exemption ($)",
                min_value=0,
                max_value=200_000,
                value=81_300,
                step=1_000,
                key=f"{prefix}_amt_ex_single"
            )
            
            reform_params["amt_exemptions"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household AMT Exemption ($)",
                min_value=0,
                max_value=200_000,
                value=81_300,
                step=1_000,
                key=f"{prefix}_amt_ex_hoh"
            )
            
            reform_params["amt_exemptions"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer AMT Exemption ($)",
                min_value=0,
                max_value=300_000,
                value=126_500,
                step=1_000,
                key=f"{prefix}_amt_ex_joint"
            )

        with col2:
            reform_params["amt_exemptions"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately AMT Exemption ($)",
                min_value=0,
                max_value=150_000,
                value=63_250,
                step=1_000,
                key=f"{prefix}_amt_ex_separate"
            )
            
            reform_params["amt_exemptions"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse AMT Exemption ($)",
                min_value=0,
                max_value=300_000,
                value=126_500,
                step=1_000,
                key=f"{prefix}_amt_ex_survivor"
            )
    
    # AMT Phase-out Start Section
    with st.expander("AMT Exemption Phase-out Start", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            reform_params["amt_phase_outs"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_single"
            )
            
            reform_params["amt_phase_outs"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_hoh"
            )
            
            reform_params["amt_phase_outs"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer Phase-out Start ($)",
                min_value=0,
                max_value=2_000_000,
                value=1_156_300,
                step=1_000,
                key=f"{prefix}_amt_po_joint"
            )

        with col2:
            reform_params["amt_phase_outs"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_separate"
            )
            
            reform_params["amt_phase_outs"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse Phase-out Start ($)",
                min_value=0,
                max_value=2_000_000,
                value=1_156_300,
                step=1_000,
                key=f"{prefix}_amt_po_survivor"
            )
    
    return reform_params

# Create inputs for both reforms
with tab1:
    reform_params_1 = create_policy_inputs("Reform 1")

with tab2:
    reform_params_2 = create_policy_inputs("Reform 2")

if st.button("Calculate Impacts"):
    # Create situation based on inputs
    situation = create_situation(
        state_code=state_code,
        filing_status=filing_status,
        employment_income=employment_income,
        head_age=head_age,
        is_married=is_married,
        spouse_age=spouse_age if is_married else None,
        num_children=num_children,
        child_ages=child_ages,
    )
    
    # Calculate and display results
    baseline, reform1_impact, reform2_impact = calculate_impacts(situation, reform_params_1, reform_params_2)
    
    # Display results in a nice format
    st.markdown("### Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Baseline")
        st.markdown(f"Household income: **${baseline:,.2f}**")
    
    with col2:
        st.markdown("#### Reform Scenario 1")
        new_income_1 = baseline + reform1_impact
        st.markdown(f"New household income: **${new_income_1:,.2f}**")
        st.markdown(f"Change from baseline: **${reform1_impact:,.2f}**")
        
        if reform1_impact > 0:
            st.success("This reform would increase household income")
        elif reform1_impact < 0:
            st.error("This reform would decrease household income")
    
    with col3:
        st.markdown("#### Reform Scenario 2")
        new_income_2 = baseline + reform2_impact
        st.markdown(f"New household income: **${new_income_2:,.2f}**")
        st.markdown(f"Change from baseline: **${reform2_impact:,.2f}**")
        
        if reform2_impact > 0:
            st.success("This reform would increase household income")
        elif reform2_impact < 0:
            st.error("This reform would decrease household income")