import streamlit as st
from constants import STATE_CODES


def create_personal_inputs():
    """Create inputs for personal information"""
    if "personal_inputs" not in st.session_state:
        st.session_state.personal_inputs = {}

    # Create two main columns for Personal and Income Information
    # Personal Information Section
    st.markdown("### Personal Information")

    state_code = st.selectbox(
        "Select your state",
        STATE_CODES,
        index=STATE_CODES.index("CA"),
    )

    # Marriage status and ages
    is_married = st.checkbox(
        "Are you married?",
    )

    # Children information
    num_children = st.number_input(
        "How many children do you have?",
        min_value=0,
        max_value=10,
        value=st.session_state.personal_inputs.get("is_married", True),
    )
    real_estate_taxes = st.number_input(
        "How much do you pay in real estate taxes?",
        min_value=0,
        max_value=1_000_000,
        value=st.session_state.personal_inputs.get("real_estate_taxes", 0),
        step=500,
    )

    expense_col1, expense_col2 = st.columns(2)
    with expense_col1:
        mortgage_interest = st.number_input(
            "How much do you pay in mortgage interest?",
            min_value=0,
            max_value=1_000_000,
            value=st.session_state.personal_inputs.get("mortgage_interest", 0),
            step=500,
        )
    with expense_col2:
        charitable_cash_donations = st.number_input(
            "How much do you donate to charity?",
            min_value=0,
            max_value=1_000_000,
            value=0,
            step=500,
        )
    # Income Information Section
    st.markdown(
        """
        ### Income Information

        How much income did you receive from the following sources? 
                """
    )

    employment_income = st.number_input(
        "Wages and salaries",
        min_value=0,
        max_value=10_000_000,
        value=st.session_state.personal_inputs.get("employment_income", 0),
        step=1000,
    )

    income_col1, income_col2, income_col3 = st.columns(3)
    with income_col1:
        qualified_dividends = st.number_input(
            "Qualified dividends",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1000,
        )
    with income_col2:
        long_term_gains = st.number_input(
            "Long term capital gains",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1_000,
        )
    with income_col3:
        short_term_gains = st.number_input(
            "Short term capital gains",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1000,
        )

    # Create a list of child ages (all 10 years old)
    child_ages = [10] * num_children if num_children > 0 else []

    # Create the input dictionary
    inputs = {
        "state_code": state_code,
        "real_estate_taxes": real_estate_taxes,
        "is_married": is_married,
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "qualified_dividend_income": qualified_dividends,
        "long_term_capital_gains": long_term_gains,
        "short_term_capital_gains": short_term_gains,
        "deductible_mortgage_interest": mortgage_interest,
        "charitable_cash_donations": charitable_cash_donations,
    }

    return inputs
