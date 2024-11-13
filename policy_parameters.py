import streamlit as st
import numpy as np

def create_policy_inputs(prefix):
    """Create inputs for all policy parameters with a streamlined interface"""
    reform_params = {
        "salt_caps": {},
        "amt_exemptions": {},
        "amt_phase_outs": {}
    }
    
    # Initialize session state variables
    if 'expander_states' not in st.session_state:
        st.session_state.expander_states = {}
    
    for section in ['salt', 'amt', 'phase']:
        if f"{prefix}_{section}_expanded" not in st.session_state.expander_states:
            st.session_state.expander_states[f"{prefix}_{section}_expanded"] = False
    
    for param in ['joint', 'other']:
        # Set SALT caps as unlimited by default, but AMT parameters as limited
        if f"{prefix}_salt_{param}_unlimited" not in st.session_state:
            st.session_state[f"{prefix}_salt_{param}_unlimited"] = True
            
        if f"{prefix}_amt_ex_{param}_unlimited" not in st.session_state:
            st.session_state[f"{prefix}_amt_ex_{param}_unlimited"] = False
            
        if f"{prefix}_amt_po_{param}_unlimited" not in st.session_state:
            st.session_state[f"{prefix}_amt_po_{param}_unlimited"] = False
            
        # Initialize default values
        if f"{prefix}_salt_{param}" not in st.session_state:
            st.session_state[f"{prefix}_salt_{param}"] = 10_000 if param == 'joint' else 10_000
        if f"{prefix}_amt_ex_{param}" not in st.session_state:
            st.session_state[f"{prefix}_amt_ex_{param}"] = 109_700 if param == 'joint' else 70_500
        if f"{prefix}_amt_po_{param}" not in st.session_state:
            st.session_state[f"{prefix}_amt_po_{param}"] = 209_000 if param == 'joint' else 156_700
    
    def set_current_policy():
        # Set SALT caps
        st.session_state[f"{prefix}_salt_joint_unlimited"] = False
        st.session_state[f"{prefix}_salt_other_unlimited"] = False
        st.session_state[f"{prefix}_salt_joint"] = 10_000
        st.session_state[f"{prefix}_salt_other"] = 10_000
        
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
        st.session_state.expander_states[f"{prefix}_phase_expanded"] = True
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Button styling */
        .stButton>button {
            padding: 0.25rem 0.5rem;
            font-size: 0.7rem;
            line-height: 1;
            height: 1.5rem;
            width: 100%;
            min-height: 1.5rem;
        }
        
        /* Number input styling for policy parameters only */
        .policy-input [data-testid="stNumberInput"] {
            width: 100%;
        }
        
        .policy-input [data-testid="stNumberInput"] input {
            padding: 0.25rem !important;
            height: 1.5rem !important;
            min-height: 1.5rem !important;
            line-height: 1 !important;
            text-align: center !important;
        }
        
        /* Hide step buttons for policy parameters only */
        .policy-input [data-testid="stNumberInput"] button {
            display: none !important;
        }
        
        /* Remove padding for hidden buttons in policy parameters */
        .policy-input [data-testid="stNumberInput"] div.css-1n76uvr {
            width: 0 !important;
            padding: 0 !important;
        }
        
        /* Container spacing */
        div[data-testid="column"] {
            padding: 0 0.5rem !important;
        }
        
        .streamlit-expanderHeader {
            padding: 0.25rem;
        }
        
        .streamlit-expanderContent {
            padding: 0.5rem 0 !important;
        }
        
        .filer-label {
            font-weight: 500;
            padding: 0.25rem 0;
        }
        
        div.row-widget.stButton, div.row-widget.stNumberInput {
            margin-bottom: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    def create_parameter_input(label, param_key, unlimited_key, max_value=None, expander_key=None):
        """Helper function to create a parameter input"""
        if not st.session_state[unlimited_key]:
            # Wrap the number input in a div with the policy-input class
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
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            value = np.inf
            st.write("Unlimited")
            
        if st.button(
            "Limited" if st.session_state[unlimited_key] else "Unlimited",
            key=f"toggle_{param_key}"
        ):
            st.session_state[unlimited_key] = not st.session_state[unlimited_key]
            if expander_key and expander_key in st.session_state.expander_states:
                st.session_state.expander_states[expander_key] = True
            st.rerun()
        
        return value

    # Add Current Policy button at the top
    st.button("Current Policy", key=f"{prefix}_current_policy", on_click=set_current_policy)

    # SALT Cap Parameters
    with st.expander("SALT Caps", expanded=st.session_state.expander_states[f"{prefix}_salt_expanded"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True)
            joint_salt = create_parameter_input(
                "Joint Filer",
                f"{prefix}_salt_joint",
                f"{prefix}_salt_joint_unlimited",
                expander_key=f"{prefix}_salt_expanded"
            )
        with col2:
            st.markdown('<div class="filer-label">Other Filers</div>', unsafe_allow_html=True)
            other_salt = create_parameter_input(
                "Other Filers",
                f"{prefix}_salt_other",
                f"{prefix}_salt_other_unlimited",
                expander_key=f"{prefix}_salt_expanded"
            )

    # AMT Exemption Parameters
    with st.expander("AMT Exemptions", expanded=st.session_state.expander_states[f"{prefix}_amt_expanded"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True)
            joint_amt = create_parameter_input(
                "Joint Filer",
                f"{prefix}_amt_ex_joint",
                f"{prefix}_amt_ex_joint_unlimited",
                300_000,
                expander_key=f"{prefix}_amt_expanded"
            )
        with col2:
            st.markdown('<div class="filer-label">Other Filers</div>', unsafe_allow_html=True)
            other_amt = create_parameter_input(
                "Other Filers",
                f"{prefix}_amt_ex_other",
                f"{prefix}_amt_ex_other_unlimited",
                200_000,
                expander_key=f"{prefix}_amt_expanded"
            )

    # AMT Phase-out Parameters
    with st.expander("Phase-out Start", expanded=st.session_state.expander_states[f"{prefix}_phase_expanded"]):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="filer-label">Joint Filer</div>', unsafe_allow_html=True)
            joint_phase = create_parameter_input(
                "Joint Filer",
                f"{prefix}_amt_po_joint",
                f"{prefix}_amt_po_joint_unlimited",
                2_000_000,
                expander_key=f"{prefix}_phase_expanded"
            )
        with col2:
            st.markdown('<div class="filer-label">Other Filers</div>', unsafe_allow_html=True)
            other_phase = create_parameter_input(
                "Other Filers",
                f"{prefix}_amt_po_other",
                f"{prefix}_amt_po_other_unlimited",
                1_000_000,
                expander_key=f"{prefix}_phase_expanded"
            )

    # Set reform parameters
    reform_params["salt_caps"].update({
        "JOINT": joint_salt,
        "SEPARATE": joint_salt / 2 if joint_salt != np.inf else np.inf,
        "SINGLE": other_salt,
        "HEAD_OF_HOUSEHOLD": other_salt,
        "SURVIVING_SPOUSE": other_salt
    })
    
    reform_params["amt_exemptions"].update({
        "JOINT": joint_amt,
        "SEPARATE": joint_amt / 2 if joint_amt != np.inf else np.inf,
        "SINGLE": other_amt,
        "HEAD_OF_HOUSEHOLD": other_amt,
        "SURVIVING_SPOUSE": other_amt
    })
    
    reform_params["amt_phase_outs"].update({
        "JOINT": joint_phase,
        "SEPARATE": joint_phase / 2 if joint_phase != np.inf else np.inf,
        "SINGLE": other_phase,
        "HEAD_OF_HOUSEHOLD": other_phase,
        "SURVIVING_SPOUSE": other_phase
    })
    
    return reform_params