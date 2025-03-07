import streamlit as st
from constants import STATE_CODES


def create_personal_inputs():
    """Create inputs for personal information"""
    
    # Apply custom styling for form inputs
    custom_css = """
    <style>
    div[data-testid="stSelectbox"] > div:first-child,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: #F7FDFC;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

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

        real_estate_taxes = st.number_input(
            "How much do you pay in property taxes?",
            min_value=0,
            max_value=1_000_000,
            value=0,
            step=500,
            help="Property taxes are deductible through your SALT deduction.",
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
    with income_col:
        st.markdown(
            """
            ### Income Information

            How much income did you receive from the following sources? 
                    """
        )

        employment_income = st.number_input(
            "Employment Income",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1000,
            help="All income is attributed to the head of the household",
        )

        qualified_dividends = st.number_input(
            "Qualified dividends",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1000,
        )

        long_term_gains = st.number_input(
            "Long term capital gains",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=1_000,
        )
        short_term_gains = st.number_input(
            "Short term capital gains",
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
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "qualified_dividend_income": qualified_dividends,
        "long_term_capital_gains": long_term_gains,
        "short_term_capital_gains": short_term_gains,
        "real_estate_taxes": real_estate_taxes,
        "deductible_mortgage_interest": mortgage_interest,
        "charitable_cash_donations": charitable_cash_donations,
    }
