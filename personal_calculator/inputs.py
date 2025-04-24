import streamlit as st
from constants import STATE_CODES


def create_personal_inputs():
    """Create inputs for personal information"""
    if "personal_inputs" in st.session_state:
        defaults = st.session_state.personal_inputs
    else:
        defaults = {
            "is_married": True,
            "num_children": 0,
            "child_ages": [],
            "employment_income": 250_000,
            "qualified_dividend_income": 0,
            "long_term_capital_gains": 0,
            "short_term_capital_gains": 0,
            "deductible_mortgage_interest": 15_000,
            "charitable_cash_donations": 10_000,
        }
    # Create two main columns for Personal and Income Information
    # Personal Information Section
    st.markdown("### Personal Information")

    # Marriage status and ages
    is_married = st.checkbox(
        "Are you married?",
    )

    # Children information
    num_children = st.number_input(
        "How many children do you have?",
        min_value=0,
        max_value=10,
        value=0,
    )

    expense_col1, expense_col2 = st.columns(2)
    with expense_col1:
        mortgage_interest = st.number_input(
            "How much do you pay in mortgage interest?",
            min_value=0,
            max_value=1_000_000,
            value=0,
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
        value=0,
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
