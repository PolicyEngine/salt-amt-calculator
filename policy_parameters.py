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
        col1, col2 = st.columns(2)
        with col1:
            reform_params["salt_caps"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_single"
            )
            
            reform_params["salt_caps"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_hoh"
            )
            
            reform_params["salt_caps"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer Cap ($)",
                min_value=0,
                max_value=200_000,
                value=20_000,
                step=1_000,
                key=f"{prefix}_salt_joint"
            )

        with col2:
            reform_params["salt_caps"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately Cap ($)",
                min_value=0,
                max_value=100_000,
                value=5_000,
                step=1_000,
                key=f"{prefix}_salt_separate"
            )
            
            reform_params["salt_caps"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse Cap ($)",
                min_value=0,
                max_value=100_000,
                value=10_000,
                step=1_000,
                key=f"{prefix}_salt_survivor"
            )
    
    # AMT Exemption Amount Section
    with st.expander("AMT Exemption Amounts", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            reform_params["amt_exemptions"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer AMT Exemption ($)",
                min_value=0,
                max_value=200_000,
                value=81_300,
                step=1_000,
                key=f"{prefix}_amt_ex_single"
            )
            
            reform_params["amt_exemptions"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household AMT Exemption ($)",
                min_value=0,
                max_value=200_000,
                value=81_300,
                step=1_000,
                key=f"{prefix}_amt_ex_hoh"
            )
            
            reform_params["amt_exemptions"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer AMT Exemption ($)",
                min_value=0,
                max_value=300_000,
                value=126_500,
                step=1_000,
                key=f"{prefix}_amt_ex_joint"
            )

        with col2:
            reform_params["amt_exemptions"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately AMT Exemption ($)",
                min_value=0,
                max_value=150_000,
                value=63_250,
                step=1_000,
                key=f"{prefix}_amt_ex_separate"
            )
            
            reform_params["amt_exemptions"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse AMT Exemption ($)",
                min_value=0,
                max_value=300_000,
                value=126_500,
                step=1_000,
                key=f"{prefix}_amt_ex_survivor"
            )
    
    # AMT Phase-out Start Section
    with st.expander("AMT Exemption Phase-out Start", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            reform_params["amt_phase_outs"]["SINGLE"] = st.number_input(
                f"{prefix} Single Filer Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_single"
            )
            
            reform_params["amt_phase_outs"]["HEAD_OF_HOUSEHOLD"] = st.number_input(
                f"{prefix} Head of Household Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_hoh"
            )
            
            reform_params["amt_phase_outs"]["JOINT"] = st.number_input(
                f"{prefix} Joint Filer Phase-out Start ($)",
                min_value=0,
                max_value=2_000_000,
                value=1_156_300,
                step=1_000,
                key=f"{prefix}_amt_po_joint"
            )

        with col2:
            reform_params["amt_phase_outs"]["SEPARATE"] = st.number_input(
                f"{prefix} Married Filing Separately Phase-out Start ($)",
                min_value=0,
                max_value=1_000_000,
                value=578_150,
                step=1_000,
                key=f"{prefix}_amt_po_separate"
            )
            
            reform_params["amt_phase_outs"]["SURVIVING_SPOUSE"] = st.number_input(
                f"{prefix} Surviving Spouse Phase-out Start ($)",
                min_value=0,
                max_value=2_000_000,
                value=1_156_300,
                step=1_000,
                key=f"{prefix}_amt_po_survivor"
            )
    
    return reform_params