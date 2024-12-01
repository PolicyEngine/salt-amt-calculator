import numpy as np

class PolicyReforms:
    @staticmethod
    def policy_reforms(reform_params):
        """Reform for SALT cap and AMT adjustments with different values by filing status"""
        salt_caps = reform_params["salt_caps"]
        amt_exemptions = reform_params["amt_exemptions"]
        amt_phase_outs = reform_params["amt_phase_outs"]
        salt_phase_out_rate = reform_params["salt_phase_out_rate"]
        salt_phase_out_threshold_joint = reform_params["salt_phase_out_threshold_joint"]
        salt_phase_out_threshold_other = reform_params["salt_phase_out_threshold_other"]

        reform_dict = {}

        # SALT caps
        for status in salt_caps:
            reform_dict[
                f"gov.irs.deductions.itemized.salt_and_real_estate.cap.{status}"
            ] = {"2026-01-01.2100-12-31": salt_caps[status]}

        # SALT phase-out parameters
        reform_dict["gov.contrib.salt_phase_out.in_effect"] = {
            "2026-01-01.2100-12-31": True
        }

        # Single rate applied to both joint and other
        reform_dict["gov.contrib.salt_phase_out.rate.joint[1].rate"] = {
            "2026-01-01.2100-12-31": salt_phase_out_rate
        }
        reform_dict["gov.contrib.salt_phase_out.rate.other[1].rate"] = {
            "2026-01-01.2100-12-31": salt_phase_out_rate
        }

        # Separate thresholds for joint and other
        reform_dict["gov.contrib.salt_phase_out.rate.joint[1].threshold"] = {
            "2026-01-01.2100-12-31": salt_phase_out_threshold_joint
        }
        reform_dict["gov.contrib.salt_phase_out.rate.other[1].threshold"] = {
            "2026-01-01.2100-12-31": salt_phase_out_threshold_other
        }

        return reform_dict

def get_reform_params_from_config(config):
    """Convert policy configuration into reform parameters"""
    reform_params = {
        "salt_caps": {},
        "salt_phase_out_rate": 0,
        "salt_phase_out_threshold_joint": 0,
        "salt_phase_out_threshold_other": 0,
        "amt_exemptions": {},
        "amt_phase_outs": {},
        "salt_phase_out_in_effect": True,
    }
    
    # Set SALT caps based on config
    if config['salt_cap'] == "Uncapped":
        reform_params["salt_caps"] = {
            "JOINT": np.inf,
            "SEPARATE": np.inf,
            "SINGLE": np.inf,
            "HEAD_OF_HOUSEHOLD": np.inf,
            "SURVIVING_SPOUSE": np.inf,
        }
    elif config['salt_cap'] == "$0 Cap":
        reform_params["salt_caps"] = {
            "JOINT": 0,
            "SEPARATE": 0,
            "SINGLE": 0,
            "HEAD_OF_HOUSEHOLD": 0,
            "SURVIVING_SPOUSE": 0,
        }
    else:  # Current Policy
        if config.get('salt_marriage_bonus'):
            reform_params["salt_caps"] = {
                "JOINT": 20_000,
                "SEPARATE": 10_000,
                "SINGLE": 10_000,
                "HEAD_OF_HOUSEHOLD": 10_000,
                "SURVIVING_SPOUSE": 10_000,
            }
        else:
            reform_params["salt_caps"] = {
                "JOINT": 10_000,
                "SEPARATE": 5_000,
                "SINGLE": 10_000,
                "HEAD_OF_HOUSEHOLD": 10_000,
                "SURVIVING_SPOUSE": 10_000,
            }

    # Set phase-out parameters
    if config['salt_phaseout'] != "None":
        reform_params["salt_phase_out_rate"] = 0.1
        reform_params["salt_phase_out_threshold_joint"] = 400_000
        reform_params["salt_phase_out_threshold_other"] = 200_000
    
    # Set AMT parameters
    if config['amt_repealed']:
        reform_params["amt_exemptions"] = {k: np.inf for k in reform_params["salt_caps"].keys()}
        reform_params["amt_phase_outs"] = {k: np.inf for k in reform_params["salt_caps"].keys()}
    else:
        # Set AMT exemptions
        if config['amt_exemption'] == "Current Policy":
            reform_params["amt_exemptions"] = {
                "JOINT": 140_565,
                "SEPARATE": 70_282,
                "SINGLE": 90_394,
                "HEAD_OF_HOUSEHOLD": 90_394,
                "SURVIVING_SPOUSE": 90_394,
            }
        else:  # Current Law
            reform_params["amt_exemptions"] = {
                "JOINT": 109_700,
                "SEPARATE": 54_850,
                "SINGLE": 70_500,
                "HEAD_OF_HOUSEHOLD": 70_500,
                "SURVIVING_SPOUSE": 70_500,
            }

        # Set AMT phase-outs
        if config['amt_phaseout'] == "Current Policy":
            reform_params["amt_phase_outs"] = {
                "JOINT": 1_285_409,
                "SEPARATE": 642_704,
                "SINGLE": 642_705,
                "HEAD_OF_HOUSEHOLD": 642_705,
                "SURVIVING_SPOUSE": 642_705,
            }
        else:  # Current Law
            reform_params["amt_phase_outs"] = {
                "JOINT": 209_000,
                "SEPARATE": 104_500,
                "SINGLE": 156_700,
                "HEAD_OF_HOUSEHOLD": 156_700,
                "SURVIVING_SPOUSE": 156_700,
            }

    return reform_params
