# inputs.py
import streamlit as st

def create_personal_inputs():
    """Create inputs for personal information"""
    personal_col, income_col = st.columns(2)
    
    # Personal Information Column
    with personal_col:
        st.markdown("### Personal Information")
        
        # Marriage checkbox first
        is_married = st.checkbox("Married")
        
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
        
        # Head age
        head_age = st.number_input("Age of Household Head", min_value=18, max_value=100, value=35)
        
        # Spouse age (only shown if married)
        spouse_age = None
        if is_married:
            spouse_age = st.number_input("Age of Spouse", min_value=18, max_value=100, value=35)
        
        # Number of children
        num_children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
        
        # Inputs for child ages
        child_ages = []
        if num_children > 0:
            st.write("Enter children's ages:")
            for i in range(0, num_children, 6):
                # Create up to 6 columns per row
                cols = st.columns(min(6, num_children - i))
                for j, col in enumerate(cols):
                    if i + j < num_children:  # Make sure we don't exceed num_children
                        with col:
                            age = st.number_input(
                                f"Child {i+j+1}",
                                min_value=0,
                                max_value=18,
                                value=5,
                                key=f"child_{i+j}",
                            )
                            child_ages.append(age)

    # Income Information Column
    with income_col:
        st.markdown("### Income Information")
        
        # Employment income
        employment_income = st.number_input(
            "Employment Income ($)",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000,
        )
        
        state_and_local_sales_or_income_tax = st.number_input(
            "State and Local Sales or Income Tax ($)",
            min_value=0,
            max_value=100000,
            value=20000,
            step=1000,
        )

        qualified_dividend_income = st.number_input(
            "Qualified Dividend Income ($)",
            min_value=0,
            max_value=100000,
            value=5000,
            step=1000,
        )

        long_term_capital_gains = st.number_input(
            "Long Term Capital Gains ($)",
            min_value=0,
            max_value=100000,
            value=5000,
            step=1000,
        )

        short_term_capital_gains = st.number_input(
            "Short Term Capital Gains ($)",
            min_value=0,
            max_value=100000,
            value=5000,
            step=1000,
        )
    
    return {
        "is_married": is_married,
        "state_code": state_code,
        "filing_status": filing_status,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "state_and_local_sales_or_income_tax": state_and_local_sales_or_income_tax,
        "qualified_dividend_income": qualified_dividend_income,
        "long_term_capital_gains": long_term_capital_gains,
        "short_term_capital_gains": short_term_capital_gains,
    }