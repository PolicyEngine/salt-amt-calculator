import streamlit as st


def create_personal_inputs():
    """Create inputs for personal information"""

    # Create two main columns for Personal and Income Information
    personal_col, income_col = st.columns(2)

    # Personal Information Section
    with personal_col:
        st.markdown("### Personal Information")

        # Marriage status
        is_married = st.checkbox("Married")

        # Ages side by side
        age_cols = st.columns(2)
        with age_cols[0]:
            head_age = st.number_input(
                "Age of Household Head", min_value=18, max_value=100, value=35
            )

        # Spouse age (only shown if married)
        spouse_age = None
        if is_married:
            with age_cols[1]:
                spouse_age = st.number_input(
                    "Age of Spouse", min_value=18, max_value=100, value=35
                )

        # State and filing status side by side
        state_col, filing_col = st.columns(2)
        with state_col:
            state_codes = [
                "AL",
                "AK",
                "AZ",
                "AR",
                "CA",
                "CO",
                "CT",
                "DE",
                "FL",
                "GA",
                "HI",
                "ID",
                "IL",
                "IN",
                "IA",
                "KS",
                "KY",
                "LA",
                "ME",
                "MD",
                "MA",
                "MI",
                "MN",
                "MS",
                "MO",
                "MT",
                "NE",
                "NV",
                "NH",
                "NJ",
                "NM",
                "NY",
                "NC",
                "ND",
                "OH",
                "OK",
                "OR",
                "PA",
                "RI",
                "SC",
                "SD",
                "TN",
                "TX",
                "UT",
                "VT",
                "VA",
                "WA",
                "WV",
                "WI",
                "WY",
            ]
            state_code = st.selectbox(
                "State", state_codes, index=state_codes.index("CA")
            )

        with filing_col:
            filing_statuses = [
                "SINGLE",
                "HEAD_OF_HOUSEHOLD",
                "JOINT",
                "SEPARATE",
                "SURVIVING_SPOUSE",
            ]
            filing_status = st.selectbox("Filing Status", filing_statuses)

        # Number of children
        num_children = st.number_input(
            "Number of Children", min_value=0, max_value=10, value=0
        )

    # Income Information Section
    with income_col:
        st.markdown("### Income Information")

        # Employment income side by side
        income_cols = st.columns(2)
        with income_cols[0]:
            employment_income = st.number_input(
                "Household Head Employment Income ($)",
                min_value=0,
                max_value=10_000_000,
                value=1_000_000,
                step=1000,
            )

        # Spouse income (only shown if married)
        spouse_income = 0
        if is_married:
            with income_cols[1]:
                spouse_income = st.number_input(
                    "Spouse Employment Income ($)",
                    min_value=0,
                    max_value=10_000_000,
                    value=0,
                    step=1000,
                )

        # Create two columns for remaining income inputs
        left_col, right_col = st.columns(2)

        with left_col:
            state_and_local_sales_or_income_tax = st.number_input(
                "State and Local Sales or Income Tax ($)",
                min_value=0,
                max_value=10_000_000,
                value=50_000,
                step=1000,
            )

            real_estate_taxes = st.number_input(
                "Real Estate Taxes ($)",
                min_value=0,
                max_value=10_000_000,
                value=30_000,
                step=1000,
            )

        with right_col:
            qualified_dividend_income = st.number_input(
                "Qualified Dividend Income ($)",
                min_value=0,
                max_value=10_000_000,
                value=5000,
                step=1000,
            )

            long_term_capital_gains = st.number_input(
                "Long Term Capital Gains ($)",
                min_value=0,
                max_value=10_000_000,
                value=5000,
                step=1000,
            )

            short_term_capital_gains = st.number_input(
                "Short Term Capital Gains ($)",
                min_value=0,
                max_value=10_000_000,
                value=5000,
                step=1000,
            )

    # Create a list of child ages (all 10 years old)
    child_ages = [10] * num_children if num_children > 0 else []

    return {
        "is_married": is_married,
        "state_code": state_code,
        "filing_status": filing_status,
        "head_age": head_age,
        "spouse_age": spouse_age,
        "spouse_income": spouse_income,
        "num_children": num_children,
        "child_ages": child_ages,
        "employment_income": employment_income,
        "state_and_local_sales_or_income_tax": state_and_local_sales_or_income_tax,
        "qualified_dividend_income": qualified_dividend_income,
        "long_term_capital_gains": long_term_capital_gains,
        "short_term_capital_gains": short_term_capital_gains,
        "real_estate_taxes": real_estate_taxes,
    }
