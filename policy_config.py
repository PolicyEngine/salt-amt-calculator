import streamlit as st

policy_config_defaults: dict[str, any] = {
    "salt_cap": "Current Law (Uncapped)",
    "salt_marriage_bonus": False,
    "salt_phaseout": "None",
    "salt_repealed": False,
    "amt_exemption": "Current Law ($70,500 Single, $109,500 Joint)",
    "amt_phaseout": "Current Law ($156,700 Single, $209,000 Joint)",
    "amt_repealed": False,
    "amt_eliminate_marriage_penalty": False,
    "other_tcja_provisions_extended": "Current Law",
    "behavioral_responses": False,
}

def initialize_policy_config_state():
    """Initialize policy config state in session state"""
    if "policy_config" not in st.session_state:
        st.session_state.policy_config = policy_config_defaults
def display_policy_config():
    """Display and collect policy configuration options"""

    # Create two columns for SALT and AMT with more width for the first column
    col1, col2 = st.columns([1, 1])  # Adjust ratio to give more space to SALT column

    # Initialize policy config in session state if it doesn't exist
    initialize_policy_config_state()

    with col1:
        st.markdown(
            '**State and local tax deduction** [📄](https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview "Learn more about how we model SALT")'
        )
        # Make labels more concise
        salt_repealed = st.checkbox(
            "Repeal SALT",
            value=st.session_state.policy_config.get("salt_repealed", False),
            key="salt_repealed_input",
        )

        # Determine the initial index based on stored value
        salt_cap_options = [
            "Current Policy ($10k)",
            "$15k",
            "$100k",
            "Current Law (Uncapped)",
        ]
        salt_cap_default = st.session_state.policy_config.get(
            "salt_cap", "Current Law (Uncapped)"
        )
        # Only set an index if the value is in our options list
        salt_cap_index = (
            salt_cap_options.index(salt_cap_default)
            if salt_cap_default in salt_cap_options
            else 2
        )

        salt_cap = st.selectbox(
            "Cap amount",  # Shortened label
            salt_cap_options,
            index=salt_cap_index,
            disabled=salt_repealed,
            key="salt_cap_input",
        )

        # If SALT is repealed, override the salt_cap value
        if salt_repealed:
            salt_cap = "Repeal SALT"

        salt_marriage_bonus = st.checkbox(
            "Double the SALT cap for married couples",
            value=st.session_state.policy_config.get("salt_marriage_bonus", False),
            disabled=salt_repealed or salt_cap == "Current Law (Uncapped)",
            key="salt_marriage_bonus_input",
        )

        salt_phaseout_options = ["None", "10% for income over 200k (400k joint)"]
        salt_phaseout_default = st.session_state.policy_config.get(
            "salt_phaseout", "None"
        )
        salt_phaseout_index = (
            salt_phaseout_options.index(salt_phaseout_default)
            if salt_phaseout_default in salt_phaseout_options
            else 0
        )

        salt_phaseout = st.selectbox(
            "SALT deduction phase-out",
            salt_phaseout_options,
            index=salt_phaseout_index,
            help="Reduce the SALT deduction linearly by 10 cents for each dollar of additional income over \$200k (or $400k for joint filers)",
            disabled=salt_repealed or salt_cap == "Current Law (Uncapped)",
            key="salt_phaseout_input",
        )

    with col2:
        st.markdown(
            '**Alternative minimum tax** [📄](https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview "Learn more about how we model AMT")'
        )

        amt_repealed = st.checkbox(
            "Repeal AMT",
            value=st.session_state.policy_config.get("amt_repealed", False),
            key="amt_repealed_input",
        )

        # AMT exemption options
        amt_exemption_options = [
            "Current Law ($70,500 Single, $109,500 Joint)",
            "Current Policy ($89,925 Single, $139,850 Joint)",
        ]
        amt_exemption_default = st.session_state.policy_config.get(
            "amt_exemption", "Current Law ($70,500 Single, $109,500 Joint)"
        )
        amt_exemption_index = (
            amt_exemption_options.index(amt_exemption_default)
            if amt_exemption_default in amt_exemption_options
            else 0
        )

        # AMT options are disabled if AMT is repealed
        amt_exemption = st.selectbox(
            "AMT exemption",
            amt_exemption_options,
            index=amt_exemption_index,
            disabled=amt_repealed,
            key="amt_exemption_input",
        )

        # AMT phaseout options
        amt_phaseout_options = [
            "Current Law ($156,700 Single, $209,000 Joint)",
            "Current Policy ($639,300 Single, $1,278,575 Joint)",
        ]
        amt_phaseout_default = st.session_state.policy_config.get(
            "amt_phaseout", "Current Law ($156,700 Single, $209,000 Joint)"
        )
        amt_phaseout_index = (
            amt_phaseout_options.index(amt_phaseout_default)
            if amt_phaseout_default in amt_phaseout_options
            else 0
        )

        amt_phaseout = st.selectbox(
            "AMT phase-out threshold",
            amt_phaseout_options,
            index=amt_phaseout_index,
            disabled=amt_repealed,
            key="amt_phaseout_input",
        )

        # New option: allow eliminating the marriage penalty if using Current Law
        amt_eliminate_marriage_penalty = st.checkbox(
            "Double the exemption amounts and phase-out thresholds for Joint filers",
            value=st.session_state.policy_config.get(
                "amt_eliminate_marriage_penalty", False
            ),
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
            key="amt_eliminate_marriage_penalty_input",
        )

    # Behavioral responses section
    st.markdown("**General**")
    # Add other TCJA provisions selector
    other_tcja_provisions_options = ["Current Law", "Current Policy"]
    other_tcja_provisions_default = st.session_state.policy_config.get(
        "other_tcja_provisions_extended", "Current Law"
    )
    other_tcja_provisions_index = (
        other_tcja_provisions_options.index(other_tcja_provisions_default)
        if other_tcja_provisions_default in other_tcja_provisions_options
        else 0
    )

    other_tcja_provisions_extended = st.radio(
        "Other TCJA Provisions",
        other_tcja_provisions_options,
        index=other_tcja_provisions_index,
        help="Choose whether TCJA provisions other than SALT and AMT expire (Current Law) or are extended (Current Policy), including the Income Tax Rate Changes, Standard Deduction, and others. [Learn More](https://policyengine.org/us/research/tcja-extension)",
        horizontal=True,  # Make radio buttons horizontal
        key="other_tcja_provisions_input",
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
