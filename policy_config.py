import streamlit as st


def display_policy_config():
    """Display and collect policy configuration options"""
    st.markdown("## Reform Options")

    st.markdown("### Policy Configuration")

    # Create two columns for SALT and AMT
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Select SALT configuration**")
        st.markdown("Choose how the State and Local Tax deduction will be structured.")

        salt_repealed = st.checkbox(
            "SALT Deduction Repealed",
            help="Check to repeal the State and Local Tax deduction",
        )

        salt_cap = st.selectbox(
            "SALT Cap",
            ["Current Policy ($10k)", "Uncapped"],
            help="Select the State and Local Tax deduction cap policy",
            disabled=salt_repealed,
        )

        salt_marriage_bonus = st.checkbox(
            "Double the SALT cap for married couples",
            disabled=salt_repealed or salt_cap == "Uncapped",
        )

        salt_phaseout = st.selectbox(
            "SALT Phase-out",
            ["None", "10% for income over 200k (400k joint)"],
            help="Configure SALT deduction phase-out parameters",
            disabled=salt_repealed or salt_cap == "Uncapped",
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
    behavioral_responses = st.checkbox(
        "Include behavioral responses",
        help="Account for how taxpayers might change their behavior",
    )

    # Store configuration in session state
    st.session_state.policy_config = {
        "salt_cap": salt_cap,
        "salt_marriage_bonus": salt_marriage_bonus,
        "salt_phaseout": salt_phaseout,
        "salt_repealed": salt_repealed,
        "amt_exemption": amt_exemption,
        "amt_phaseout": amt_phaseout,
        "amt_repealed": amt_repealed,
        "behavioral_responses": behavioral_responses,
    }

    return st.session_state.policy_config
