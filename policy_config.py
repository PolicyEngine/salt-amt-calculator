import streamlit as st


def display_policy_config():
    """Display and collect policy configuration options"""
    st.markdown("## Reform Options")

    # Baseline selector
    st.markdown("### Policy Configuration")
    st.markdown("Select baseline scenario which the reform will be compared against")
    st.markdown(
        "This determines the starting point for measuring the impact of reforms."
    )

    baseline = st.selectbox(
        "Baseline",
        ["Current Law", "Current Policy"],
        help="Choose whether to compare against Current Law or Current Policy (TCJA Extended)",
    )

    # Store baseline in session state
    st.session_state.baseline = baseline

    # Create two columns for SALT and AMT
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Select SALT configuration**")
        st.markdown("Choose how the State and Local Tax deduction will be structured.")

        salt_marriage_bonus = st.checkbox(
            "Marriage Bonus", help="Double the SALT cap for married couples"
        )

        salt_cap = st.selectbox(
            "SALT Cap",
            ["Current Policy", "Uncapped", "$0 Cap"],
            help="Select the SALT deduction cap policy",
        )

        salt_phaseout = st.selectbox(
            "SALT Phase-out",
            ["10% for income over 200k (400k joint)", "None"],
            help="Configure SALT deduction phase-out parameters",
        )

    with col2:
        st.markdown("**AMT Configuration**")
        st.markdown("Configure the Alternative Minimum Tax parameters.")

        amt_repealed = st.checkbox(
            "AMT Repealed", help="Check to repeal the Alternative Minimum Tax"
        )

        # AMT options are disabled if AMT is repealed
        amt_exemption = st.selectbox(
            "AMT Exemption",
            ["Current Law", "Current Policy"],
            help="Set AMT exemption levels",
            disabled=amt_repealed,
        )

        amt_phaseout = st.selectbox(
            "AMT Phase-out Threshold",
            ["Current Law", "Current Policy"],
            help="Set AMT phase-out threshold",
            disabled=amt_repealed,
        )

    # Behavioral responses section
    st.markdown("**Apply behavioral responses**")
    st.markdown("Include or exclude taxpayer behavioral responses to policy changes.")
    behavioral_responses = st.selectbox(
        "Behavioral Responses",
        ["Excluded", "Included"],
        help="Account for how taxpayers might change their behavior",
    )

    # Store configuration in session state
    st.session_state.policy_config = {
        "salt_cap": salt_cap,
        "salt_marriage_bonus": salt_marriage_bonus,
        "salt_phaseout": salt_phaseout,
        "amt_exemption": amt_exemption,
        "amt_phaseout": amt_phaseout,
        "amt_repealed": amt_repealed,
        "behavioral_responses": behavioral_responses,
    }

    return st.session_state.policy_config
