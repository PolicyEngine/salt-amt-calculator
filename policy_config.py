import streamlit as st


def display_policy_config():
    """Display and collect policy configuration options"""

    st.markdown("## Configure Your Policy")

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

    # Create two columns for SALT and AMT with more width for the first column
    col1, col2 = st.columns([1, 1])  # Adjust ratio to give more space to SALT column

    with col1:
        st.markdown("**State and local tax deduction** [📄](https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview \"Learn more about how we model SALT\")")
        # Make labels more concise
        salt_repealed = st.checkbox(
            "Repeal SALT",
        )

        salt_cap = st.selectbox(
            "Cap amount",  # Shortened label
            ["Current Policy ($10k)", "$15k", "Current Law (Uncapped)"],
            index=2,
            disabled=salt_repealed,
        )

        # If SALT is repealed, override the salt_cap value
        if salt_repealed:
            salt_cap = "Repeal SALT"

        salt_marriage_bonus = st.checkbox(
            "Double the SALT cap for married couples",
            disabled=salt_repealed or salt_cap == "Uncapped",
        )

        salt_phaseout = st.selectbox(
            "SALT deduction phase-out",
            ["None", "10% for income over 200k (400k joint)"],
            help="Reduce the SALT deduction linearly by 10 cents for each dollar of additional income over \$200k (or $400k for joint filers)",
            disabled=salt_repealed or salt_cap == "Uncapped",
        )

    with col2:
        st.markdown("**Alternative minimum tax** [📄](https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview \"Learn more about how we model AMT\")")

        amt_repealed = st.checkbox(
            "Repeal AMT",
        )

        # AMT options are disabled if AMT is repealed
        amt_exemption = st.selectbox(
            "AMT exemption",
            [
                "Current Law ($70,500 Single, $109,500 Joint)",
                "Current Policy ($89,925 Single, $139,850 Joint)",
            ],
            disabled=amt_repealed,
        )

        amt_phaseout = st.selectbox(
            "AMT phase-out threshold",
            [
                "Current Law ($156,700 Single, $209,000 Joint)",
                "Current Policy ($639,300 Single, $1,278,575 Joint)",
            ],
            disabled=amt_repealed,
        )

        # New option: allow eliminating the marriage penalty if using Current Law
        amt_eliminate_marriage_penalty = st.checkbox(
            "Double the exemption amounts and phase-out thresholds for Joint filers",
            disabled=amt_repealed
            or (amt_exemption != "Current Law ($70,500 Single, $109,500 Joint)")
            or (amt_phaseout != "Current Law ($156,700 Single, $209,000 Joint)"),
            help=(
                "When selected, the AMT exemptions are set as follows:\n"
                "    - Single: 70,500\n"
                "    - Joint: 141,000\n\n"
                "Similarly, the phase‐out thresholds are adjusted to:\n"
                "    - Single: 156,700\n"
                "    - Joint: 313,400"
            ),
        )

    # Behavioral responses section
    st.markdown("**General**")
    # Add other TCJA provisions selector
    other_tcja_provisions_extended = st.radio(
        "Other TCJA Provisions",
        ["Current Law", "Current Policy"],
        help="Choose whether TCJA provisions other than SALT and AMT expire (Current Law) or are extended (Current Policy), including the Income Tax Rate Changes, Standard Deduction, and others. [Learn More](https://policyengine.org/us/research/tcja-extension)",
        horizontal=True,  # Make radio buttons horizontal
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
        "amt_eliminate_marriage_penalty": amt_eliminate_marriage_penalty,
        "other_tcja_provisions_extended": other_tcja_provisions_extended,
    }

    return st.session_state.policy_config
