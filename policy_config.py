import streamlit as st


def display_policy_config():
    """Display and collect policy configuration options"""

    st.markdown("## Configure your policy")

    # Create two columns for SALT and AMT
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**State and local tax deduction**")

        salt_repealed = st.checkbox(
            "Repeal SALT deduction",
            help="Check to repeal the State and Local Tax deduction",
        )

        salt_cap = st.selectbox(
            "SALT cap",
            ["Current Policy ($10k)", "Uncapped"],
            help="Select the State and Local Tax deduction cap policy",
            disabled=salt_repealed,
        )

        salt_marriage_bonus = st.checkbox(
            "Double the SALT cap for married couples",
            disabled=salt_repealed or salt_cap == "Uncapped",
        )

        salt_phaseout = st.selectbox(
            "SALT phase-out",
            ["None", "10% for income over 200k (400k joint)"],
            help="Configure SALT deduction phase-out parameters",
            disabled=salt_repealed or salt_cap == "Uncapped",
        )

    with col2:
        st.markdown("**Alternative minimum tax**")

        amt_repealed = st.checkbox(
            "Repeal AMT", help="Check to repeal the Alternative Minimum Tax"
        )

        # AMT options are disabled if AMT is repealed
        amt_exemption = st.selectbox(
            "AMT exemption",
            ["Current Law", "Current Policy"],
            help="Set AMT exemption levels",
            disabled=amt_repealed,
        )

        amt_phaseout = st.selectbox(
            "AMT phase-out threshold",
            ["Current Law", "Current Policy"],
            help="Set AMT phase-out threshold",
            disabled=amt_repealed,
        )

    # Behavioral responses section
    st.markdown("**General**")
    behavioral_responses = st.checkbox(
        "Include behavioral responses",
        help="Account for how taxpayers might change their behavior",
    )
    # Add other TCJA provisions selector
    other_tcja_provisions_extended = st.radio(
        "Other TCJA Provisions",
        ["Current Law", "Current Policy"],
        help="Choose whether TCJA provisions other than SALT and AMT expire (Current Law) or are extended (Current Policy), including the Income Tax Rate Changes, Standard Deduction, and others.",
    )

    # Store baseline in session state with the correct data column identifier
    st.session_state.other_tcja_provisions_extended = (
        "other_tcja_provisions_extended_no"
        if other_tcja_provisions_extended == "Current Law (TCJA Expires)"
        else "other_tcja_provisions_extended_yes"
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
        "other_tcja_provisions_extended": other_tcja_provisions_extended,
    }

    return st.session_state.policy_config
