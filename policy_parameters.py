# policy_parameters.py
import streamlit as st

def create_policy_inputs(prefix):
    """Create inputs for all policy parameters with collapsible sections"""
    reform_params = {
        "salt_caps": {},
        "amt_exemptions": {},
        "amt_phase_outs": {}
    }
    
    # SALT Cap Section
    with st.expander("SALT Deduction Caps", expanded=False):
        # Only show inputs for Joint and Other, calculate Separate
        joint_salt = st.number_input(
            f"{prefix} Joint Filer Cap ($)",
            min_value=0,
            max_value=200_000,
            value=20_000,
            step=1_000,
            key=f"{prefix}_salt_joint"
        )
        
        other_salt = st.number_input(
            f"{prefix} Other Filers Cap ($)",
            min_value=0,
            max_value=100_000,
            value=10_000,
            step=1_000,
            key=f"{prefix}_salt_other"
        )
        
        # Set values in the reform_params dictionary
        reform_params["salt_caps"]["JOINT"] = joint_salt
        reform_params["salt_caps"]["SEPARATE"] = joint_salt // 2  # Automatically set to half of joint
        reform_params["salt_caps"]["SINGLE"] = other_salt
        reform_params["salt_caps"]["HEAD_OF_HOUSEHOLD"] = other_salt
        reform_params["salt_caps"]["SURVIVING_SPOUSE"] = other_salt
    
    # AMT Exemption Amount Section
    with st.expander("AMT Exemption Amounts", expanded=False):
        joint_amt = st.number_input(
            f"{prefix} Joint Filer AMT Exemption ($)",
            min_value=0,
            max_value=300_000,
            value=126_500,
            step=1_000,
            key=f"{prefix}_amt_ex_joint"
        )
        
        other_amt = st.number_input(
            f"{prefix} Other Filers AMT Exemption ($)",
            min_value=0,
            max_value=200_000,
            value=81_300,
            step=1_000,
            key=f"{prefix}_amt_ex_other"
        )
        
        # Set values in the reform_params dictionary
        reform_params["amt_exemptions"]["JOINT"] = joint_amt
        reform_params["amt_exemptions"]["SEPARATE"] = joint_amt // 2  # Automatically set to half of joint
        reform_params["amt_exemptions"]["SINGLE"] = other_amt
        reform_params["amt_exemptions"]["HEAD_OF_HOUSEHOLD"] = other_amt
        reform_params["amt_exemptions"]["SURVIVING_SPOUSE"] = other_amt
    
    # AMT Phase-out Start Section
    with st.expander("AMT Exemption Phase-out Start", expanded=False):
        joint_phase = st.number_input(
            f"{prefix} Joint Filer Phase-out Start ($)",
            min_value=0,
            max_value=2_000_000,
            value=1_156_300,
            step=1_000,
            key=f"{prefix}_amt_po_joint"
        )
        
        other_phase = st.number_input(
            f"{prefix} Other Filers Phase-out Start ($)",
            min_value=0,
            max_value=1_000_000,
            value=578_150,
            step=1_000,
            key=f"{prefix}_amt_po_other"
        )
        
        # Set values in the reform_params dictionary
        reform_params["amt_phase_outs"]["JOINT"] = joint_phase
        reform_params["amt_phase_outs"]["SEPARATE"] = joint_phase // 2  # Automatically set to half of joint
        reform_params["amt_phase_outs"]["SINGLE"] = other_phase
        reform_params["amt_phase_outs"]["HEAD_OF_HOUSEHOLD"] = other_phase
        reform_params["amt_phase_outs"]["SURVIVING_SPOUSE"] = other_phase
    
    return reform_params