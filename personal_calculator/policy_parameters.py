import streamlit as st
import numpy as np


def create_policy_inputs(prefix):
    """Create inputs for all policy parameters with a streamlined interface"""
    reform_params = {
        "salt_caps": {},
        "salt_phase_out_rate": 0,
        "salt_phase_out_threshold_joint": 0,
        "salt_phase_out_threshold_other": 0,
        "salt_phase_out_enabled": False,
        "amt_exemptions": {},
        "amt_phase_outs": {},
        "salt_phase_out_in_effect": True,  # Always true, not a user input
    }

    # Initialize session state variables
    if "expander_states" not in st.session_state:
        st.session_state.expander_states = {}

    for section in ["salt", "amt"]:
        if f"{prefix}_{section}_expanded" not in st.session_state.expander_states:
            st.session_state.expander_states[f"{prefix}_{section}_expanded"] = False

    # Initialize all session state variables
    defaults = {
        f"{prefix}_salt_joint": 10_000,
        f"{prefix}_salt_other": 10_000,
        f"{prefix}_salt_joint_unlimited": True,
        f"{prefix}_salt_other_unlimited": True,
        f"{prefix}_salt_phase_out_rate": 0,
        f"{prefix}_salt_phase_out_threshold_joint": 0,
        f"{prefix}_salt_phase_out_threshold_other": 0,
        f"{prefix}_amt_ex_joint": 109_700,
        f"{prefix}_amt_ex_other": 70_500,
        f"{prefix}_amt_ex_joint_unlimited": False,
        f"{prefix}_amt_ex_other_unlimited": False,
        f"{prefix}_amt_po_joint": 209_000,
        f"{prefix}_amt_po_other": 156_700,
        f"{prefix}_amt_po_joint_unlimited": False,
        f"{prefix}_amt_po_other_unlimited": False,
    }

    # Initialize any missing session state variables with default values
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

    def set_current_policy():
        # Set SALT caps
        st.session_state[f"{prefix}_salt_joint_unlimited"] = False
        st.session_state[f"{prefix}_salt_other_unlimited"] = False
        st.session_state[f"{prefix}_salt_joint"] = 10_000
        st.session_state[f"{prefix}_salt_other"] = 10_000

        # Set SALT phase out parameters
        st.session_state[f"{prefix}_salt_phase_out_rate"] = 0
        st.session_state[f"{prefix}_salt_phase_out_threshold_joint"] = 0
        st.session_state[f"{prefix}_salt_phase_out_threshold_other"] = 0
        st.session_state[f"{prefix}_salt_phase_out_enabled"] = False

        # Set AMT exemptions
        st.session_state[f"{prefix}_amt_ex_joint_unlimited"] = False
        st.session_state[f"{prefix}_amt_ex_other_unlimited"] = False
        st.session_state[f"{prefix}_amt_ex_joint"] = 140_565
        st.session_state[f"{prefix}_amt_ex_other"] = 90_394

        # Set AMT phase-outs
        st.session_state[f"{prefix}_amt_po_joint_unlimited"] = False
        st.session_state[f"{prefix}_amt_po_other_unlimited"] = False
        st.session_state[f"{prefix}_amt_po_joint"] = 1_285_409
        st.session_state[f"{prefix}_amt_po_other"] = 642_705

        # Ensure expanders stay open
        st.session_state.expander_states[f"{prefix}_salt_expanded"] = True
        st.session_state.expander_states[f"{prefix}_amt_expanded"] = True

    def set_current_law():
        # Set SALT caps as unlimited
        st.session_state[f"{prefix}_salt_joint_unlimited"] = True
        st.session_state[f"{prefix}_salt_other_unlimited"] = True
        st.session_state[f"{prefix}_salt_joint"] = 10_000
        st.session_state[f"{prefix}_salt_other"] = 10_000

        # Set SALT phase out parameters
        st.session_state[f"{prefix}_salt_phase_out_rate"] = 0
        st.session_state[f"{prefix}_salt_phase_out_threshold_joint"] = 0
        st.session_state[f"{prefix}_salt_phase_out_threshold_other"] = 0
        st.session_state[f"{prefix}_salt_phase_out_enabled"] = False

        # Set AMT exemptions to default values
        st.session_state[f"{prefix}_amt_ex_joint_unlimited"] = False
        st.session_state[f"{prefix}_amt_ex_other_unlimited"] = False
        st.session_state[f"{prefix}_amt_ex_joint"] = 109_700
        st.session_state[f"{prefix}_amt_ex_other"] = 70_500

        # Set AMT phase-outs to default values
        st.session_state[f"{prefix}_amt_po_joint_unlimited"] = False
        st.session_state[f"{prefix}_amt_po_other_unlimited"] = False
        st.session_state[f"{prefix}_amt_po_joint"] = 209_000
        st.session_state[f"{prefix}_amt_po_other"] = 156_700

        # Ensure expanders stay open
        st.session_state.expander_states[f"{prefix}_salt_expanded"] = True
        st.session_state.expander_states[f"{prefix}_amt_expanded"] = True

    # Add Current Policy and Current Law buttons at the top in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Populate Current Policy",
            key=f"{prefix}_current_policy",
            on_click=set_current_policy,
            use_container_width=True,
        )
    with col2:
        st.button(
            "Populate Current Law",
            key=f"{prefix}_current_law",
            on_click=set_current_law,
            use_container_width=True,
        )

    # State and Local Tax Parameters (Caps and Phase-out)
    with st.expander(
        "State and Local Tax Deduction",
        expanded=st.session_state.expander_states[f"{prefix}_salt_expanded"],
    ):
        st.markdown("#### Deduction Cap")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True
            )
            joint_salt = create_parameter_input(
                "Joint Filer",
                f"{prefix}_salt_joint",
                f"{prefix}_salt_joint_unlimited",
                expander_key=f"{prefix}_salt_expanded",
            )
        with col2:
            st.markdown(
                '<div class="filer-label">Other Filers</div>', unsafe_allow_html=True
            )
            other_salt = create_parameter_input(
                "Other Filers",
                f"{prefix}_salt_other",
                f"{prefix}_salt_other_unlimited",
                expander_key=f"{prefix}_salt_expanded",
            )

        # Add header for phase-out section
        st.markdown("#### Phase-out rate and thresholds")

        # Single rate input that affects both joint and other
        salt_phase_out_rate_pct = st.number_input(
            "Phase-out Rate (%)",
            min_value=0,
            max_value=100,
            value=int(st.session_state[f"{prefix}_salt_phase_out_rate"] * 100),
            step=1,
            key=f"{prefix}_salt_phase_out_rate_pct",
        )
        # Convert to decimal for backend
        salt_phase_out_rate = salt_phase_out_rate_pct / 100.0
        # Update session state
        st.session_state[f"{prefix}_salt_phase_out_rate"] = salt_phase_out_rate

        # Determine if phase-out is enabled based on rate and thresholds
        salt_phase_out_enabled = (
            salt_phase_out_rate > 0 
            and (st.session_state[f"{prefix}_salt_phase_out_threshold_joint"] > 0 or st.session_state[f"{prefix}_salt_phase_out_threshold_other"] > 0)
        )

        # Separate threshold inputs for joint and other
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True
            )
            salt_phase_out_threshold_joint = st.number_input(
                "Phase-out Threshold - Joint ($)",
                min_value=0,
                max_value=1_000_000,
                value=int(st.session_state[f"{prefix}_salt_phase_out_threshold_joint"]),
                step=1_000,
                key=f"{prefix}_salt_phase_out_threshold_joint",
            )

        with col2:
            st.markdown(
                '<div class="filer-label">Other Filers</div>', unsafe_allow_html=True
            )
            salt_phase_out_threshold_other = st.number_input(
                "Phase-out Threshold - Other ($)",
                min_value=0,
                max_value=1_000_000,
                value=int(st.session_state[f"{prefix}_salt_phase_out_threshold_other"]),
                step=1_000,
                key=f"{prefix}_salt_phase_out_threshold_other",
            )

    # Alternative Minimum Tax Parameters
    with st.expander(
        "Alternative Minimum Tax",
        expanded=st.session_state.expander_states[f"{prefix}_amt_expanded"],
    ):
        st.markdown("#### Exemption Amounts")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True
            )
            joint_amt = create_parameter_input(
                "Joint Filer",
                f"{prefix}_amt_ex_joint",
                f"{prefix}_amt_ex_joint_unlimited",
                300_000,
                expander_key=f"{prefix}_amt_expanded",
            )
        with col2:
            st.markdown(
                '<div class="filer-label">Other Filers</div>', unsafe_allow_html=True
            )
            other_amt = create_parameter_input(
                "Other Filers",
                f"{prefix}_amt_ex_other",
                f"{prefix}_amt_ex_other_unlimited",
                200_000,
                expander_key=f"{prefix}_amt_expanded",
            )

        st.markdown("#### Phase-out thresholds")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True
            )
            joint_phase = create_parameter_input(
                "Joint Filer",
                f"{prefix}_amt_po_joint",
                f"{prefix}_amt_po_joint_unlimited",
                2_000_000,
                expander_key=f"{prefix}_amt_expanded",
            )
        with col2:
            st.markdown(
                '<div class="filer-label">Other Filers</div>', unsafe_allow_html=True
            )
            other_phase = create_parameter_input(
                "Other Filers",
                f"{prefix}_amt_po_other",
                f"{prefix}_amt_po_other_unlimited",
                1_000_000,
                expander_key=f"{prefix}_amt_expanded",
            )

    # Set reform parameters
    reform_params["salt_caps"].update(
        {
            "JOINT": joint_salt,
            "SEPARATE": joint_salt / 2 if joint_salt != np.inf else np.inf,
            "SINGLE": other_salt,
            "HEAD_OF_HOUSEHOLD": other_salt,
            "SURVIVING_SPOUSE": other_salt,
        }
    )

    reform_params["salt_phase_out_rate"] = salt_phase_out_rate
    reform_params["salt_phase_out_threshold_joint"] = salt_phase_out_threshold_joint
    reform_params["salt_phase_out_threshold_other"] = salt_phase_out_threshold_other
    reform_params["salt_phase_out_enabled"] = salt_phase_out_enabled

    reform_params["amt_exemptions"].update(
        {
            "JOINT": joint_amt,
            "SEPARATE": joint_amt / 2 if joint_amt != np.inf else np.inf,
            "SINGLE": other_amt,
            "HEAD_OF_HOUSEHOLD": other_amt,
            "SURVIVING_SPOUSE": other_amt,
        }
    )

    reform_params["amt_phase_outs"].update(
        {
            "JOINT": joint_phase,
            "SEPARATE": joint_phase / 2 if joint_phase != np.inf else np.inf,
            "SINGLE": other_phase,
            "HEAD_OF_HOUSEHOLD": other_phase,
            "SURVIVING_SPOUSE": other_phase,
        }
    )

    return reform_params


def create_parameter_input(
    label, param_key, unlimited_key, max_value=None, expander_key=None
):
    """Helper function to create a parameter input"""
    if not st.session_state[unlimited_key]:
        st.markdown('<div class="policy-input">', unsafe_allow_html=True)
        value = st.number_input(
            label,
            min_value=0,
            max_value=max_value if max_value else None,
            value=st.session_state[param_key],
            step=1_000,
            label_visibility="collapsed",
            key=param_key,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        value = np.inf
        st.write("Unlimited")

    if st.button(
        "Limited" if st.session_state[unlimited_key] else "Unlimited",
        key=f"toggle_{param_key}",
    ):
        st.session_state[unlimited_key] = not st.session_state[unlimited_key]
        if expander_key and expander_key in st.session_state.expander_states:
            st.session_state.expander_states[expander_key] = True
        st.rerun()

    return value
