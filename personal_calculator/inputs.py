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
            "What state do you live in?",
            STATE_CODES,
            index=STATE_CODES.index("CA"),
            help="State income tax varies by state and will impact your SALT deduction.",
        )

        # Marriage status and ages
        is_married = st.checkbox(
            "Are you married?",
            help="Marital status impacts AMT related provisions such as income thresholds and tax rates.",
        )

        # Children information
        num_children = st.number_input(
            "How many children do you have?",
            min_value=0,
            max_value=10,
            value=0,
            help="Each child is assumed to be 10 years old. The AMT exemption amount increases with each child.",
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
                help="Different types of income are included in the AMT income definition, inculding qualified dividends.",
            )
            real_estate_taxes = st.number_input(
                "How much do you pay in property taxes?",
                min_value=0,
                max_value=10_000_000,
                value=30_000,
                step=1_000,
                help="Property taxes are deductible through your SALT deduction.",
            )

        with tax_col2:

            long_term_gains = st.number_input(
                "How much income do you make from long term capital gains?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1_000,
                help="The AMT is reduced by the tax on capital gains.",
            )
            short_term_gains = st.number_input(
                "How much income do you make from short term capital gains?",
                min_value=0,
                max_value=10_000_000,
                value=0,
                step=1000,
                help="The AMT is reduced by the tax on capital gains.",
            )

    # Create a list of child ages (all 10 years old)
    child_ages = [10] * num_children if num_children > 0 else []

    return {
        "is_married": is_married,
        "state_code": state_code,
        "spouse_income": spouse_income,
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "qualified_dividend_income": qualified_dividends,
        "long_term_capital_gains": long_term_gains,
        "short_term_capital_gains": short_term_gains,
        "real_estate_taxes": real_estate_taxes,
    }
