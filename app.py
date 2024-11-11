# app.py
import streamlit as st
from situation import create_situation
from calculator import calculate_impact

# Set up the Streamlit page
st.set_page_config(page_title="SALT Cap Policy Impact Calculator", page_icon="📊")

# Title and description
st.title("SALT Cap Policy Impact Calculator")
st.markdown("""
This calculator shows the impact of adjusting the SALT (State and Local Tax) 
deduction cap. Input your household characteristics below.
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
    filing_statuses = ["SINGLE", "HEAD_OF_HOUSEHOLD", "JOINT"]
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

# Policy parameter
st.markdown("### Policy Parameter")
salt_cap = st.number_input(
    "SALT Deduction Cap ($)",
    min_value=0,
    max_value=100_000,
    value=10_000,
    step=1_000,
)

if st.button("Calculate Impact"):
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
    impact = calculate_impact(situation, salt_cap)
    
    st.markdown("### Results")
    st.markdown(
        f"Net impact on household income: **${impact:,.2f}**"
    )
    
    # Add interpretation
    if impact > 0:
        st.success("This policy change would increase household net income.")
    elif impact < 0:
        st.error("This policy change would decrease household net income.")
    else:
        st.info("This policy change would have no effect on household net income.")