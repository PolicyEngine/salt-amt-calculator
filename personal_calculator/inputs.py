import streamlit as st
from constants import STATE_CODES


def create_personal_inputs():
    """Create inputs for personal information"""

    # Create two main columns for Personal and Income Information
    personal_col, income_col = st.columns(2)

    # Personal Information Section
    with personal_col:
        st.markdown("### Personal Information")

        # Filing status and state in same row
        state_code = st.selectbox(
            "What state do you live in?", STATE_CODES, index=STATE_CODES.index("CA")
        )

        # Marriage status and ages
        is_married = st.checkbox("Are you married?")
        if is_married:
            age_col1, age_col2 = st.columns(2)
            with age_col1:
                head_age = st.number_input(
                    "How old are you?",
                    min_value=18,
                    max_value=100,
                    value=35,
                )
            with age_col2:
                spouse_age = st.number_input(
                    "How old is your spouse?",
                    min_value=18,
                    max_value=100,
                    value=35,
                )
        else:
            head_age = st.number_input(
                "How old are you?",
                min_value=18,
                max_value=100,
                value=35,
            )
            spouse_age = None

        # Children information
        num_children = st.number_input(
            "How many children do you have?", min_value=0, max_value=10, value=0
        )

    # Income Information Section
    with income_col:
        st.markdown("### Income Information")

        # Employment income
        if is_married:
            income_col1, income_col2 = st.columns(2)
            with income_col1:
                employment_income = st.number_input(
                    "How much income do you make from employment?",
                    min_value=0,
                    max_value=10_000_000,
                    value=0,
                    step=1000,
                )
            with income_col2:
                spouse_income = st.number_input(
                    "How much income does your spouse make from employment?",
                    min_value=0,
                    max_value=10_000_000,
                    value=0,
                    step=1000,
                )
        else:
            employment_income = st.number_input(
                "How much income do you make from employment?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1000,
            )
            spouse_income = 0

        # Tax-related income in two columns
        tax_col1, tax_col2 = st.columns(2)
        with tax_col1:
            qualified_dividends = st.number_input(
                "How much income do you make from qualified dividends?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1000,
            )
            real_estate_taxes = st.number_input(
                "How much do you pay in real estate taxes?",
                min_value=0,
                max_value=10_000_000,
                value=30_000,
                step=1000,
            )

        with tax_col2:

            long_term_gains = st.number_input(
                "How much income do you make from long term capital gains?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1000,
            )
            short_term_gains = st.number_input(
                "How much income do you make from short term capital gains?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1000,
            )

    # Create a list of child ages (all 10 years old)
    child_ages = [10] * num_children if num_children > 0 else []

    return {
        "is_married": is_married,
        "state_code": state_code,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "spouse_income": spouse_income,
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "qualified_dividend_income": qualified_dividends,
        "long_term_capital_gains": long_term_gains,
        "short_term_capital_gains": short_term_gains,
        "real_estate_taxes": real_estate_taxes,
    }
