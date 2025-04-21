import numpy as np


def get_other_tcja_provisions():
    """Returns the reform dictionary for TCJA extension"""
    return {
        "gov.irs.credits.ctc.amount.base[0].amount": {"2026-01-01.2100-12-31": 2000},
        "gov.irs.credits.ctc.phase_out.threshold.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.JOINT": {
            "2026-01-01.2100-12-31": 400000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SEPARATE": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SINGLE": {
            "2026-01-01.2100-12-31": 200000
        },
        "gov.irs.credits.ctc.phase_out.threshold.SURVIVING_SPOUSE": {
            "2026-01-01.2100-12-31": 400000
        },
        "gov.irs.credits.ctc.refundable.individual_max": {
            "2026-01-01.2026-12-31": 1800,
        },
        "gov.irs.credits.ctc.refundable.phase_in.threshold": {
            "2026-01-01.2100-12-31": 2500
        },
        "gov.irs.deductions.itemized.casualty.active": {"2026-01-01.2100-12-31": False},
        "gov.irs.deductions.itemized.charity.ceiling.all": {
            "2026-01-01.2100-12-31": 0.6
        },
        "gov.irs.deductions.itemized.limitation.agi_rate": {
            "2026-01-01.2026-12-31": 1,
        },
        "gov.irs.deductions.itemized.limitation.applicable_amount.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 1000000,
        },
        "gov.irs.deductions.itemized.limitation.applicable_amount.JOINT": {
            "2026-01-01.2026-12-31": 1000000,
        },
        "gov.irs.deductions.itemized.limitation.applicable_amount.SEPARATE": {
            "2026-01-01.2026-12-31": 1000000,
        },
        "gov.irs.deductions.itemized.limitation.applicable_amount.SINGLE": {
            "2026-01-01.2026-12-31": 1000000,
        },
        "gov.irs.deductions.itemized.limitation.applicable_amount.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 1000000,
        },
        "gov.irs.deductions.itemized.limitation.itemized_deduction_rate": {
            "2026-01-01.2026-12-31": 1,
        },
        "gov.irs.deductions.qbi.max.business_property.rate": {
            "2026-01-01.2100-12-31": 0.025
        },
        "gov.irs.deductions.qbi.max.rate": {"2026-01-01.2100-12-31": 0.2},
        "gov.irs.deductions.qbi.max.w2_wages.alt_rate": {"2026-01-01.2100-12-31": 0.25},
        "gov.irs.deductions.qbi.max.w2_wages.rate": {"2026-01-01.2100-12-31": 0.5},
        "gov.irs.deductions.qbi.phase_out.length.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2100-12-31": 50000
        },
        "gov.irs.deductions.qbi.phase_out.length.JOINT": {
            "2026-01-01.2100-12-31": 100000
        },
        "gov.irs.deductions.qbi.phase_out.length.SEPARATE": {
            "2026-01-01.2100-12-31": 50000
        },
        "gov.irs.deductions.qbi.phase_out.length.SINGLE": {
            "2026-01-01.2100-12-31": 50000
        },
        "gov.irs.deductions.qbi.phase_out.length.SURVIVING_SPOUSE": {
            "2026-01-01.2100-12-31": 100000
        },
        "gov.irs.deductions.qbi.phase_out.start.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 204900,
        },
        "gov.irs.deductions.qbi.phase_out.start.JOINT": {
            "2026-01-01.2026-12-31": 409800,
        },
        "gov.irs.deductions.qbi.phase_out.start.SEPARATE": {
            "2026-01-01.2026-12-31": 204900,
        },
        "gov.irs.deductions.qbi.phase_out.start.SINGLE": {
            "2026-01-01.2026-12-31": 204900,
        },
        "gov.irs.deductions.qbi.phase_out.start.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 409800,
        },
        "gov.irs.deductions.standard.amount.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 22950,
        },
        "gov.irs.deductions.standard.amount.JOINT": {
            "2026-01-01.2026-12-31": 30600,
        },
        "gov.irs.deductions.standard.amount.SEPARATE": {
            "2026-01-01.2026-12-31": 15300,
        },
        "gov.irs.deductions.standard.amount.SINGLE": {
            "2026-01-01.2026-12-31": 15300,
        },
        "gov.irs.deductions.standard.amount.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 30600,
        },
        "gov.irs.income.bracket.rates.2": {"2026-01-01.2100-12-31": 0.12},
        "gov.irs.income.bracket.rates.3": {"2026-01-01.2100-12-31": 0.22},
        "gov.irs.income.bracket.rates.4": {"2026-01-01.2100-12-31": 0.24},
        "gov.irs.income.bracket.rates.5": {"2026-01-01.2100-12-31": 0.32},
        "gov.irs.income.bracket.rates.7": {"2026-01-01.2100-12-31": 0.37},
        "gov.irs.income.bracket.thresholds.3.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 105475,
        },
        "gov.irs.income.bracket.thresholds.3.JOINT": {
            "2026-01-01.2026-12-31": 210950,
        },
        "gov.irs.income.bracket.thresholds.3.SEPARATE": {
            "2026-01-01.2026-12-31": 105475,
        },
        "gov.irs.income.bracket.thresholds.3.SINGLE": {
            "2026-01-01.2026-12-31": 105475,
        },
        "gov.irs.income.bracket.thresholds.3.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 210950,
        },
        "gov.irs.income.bracket.thresholds.4.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 201350,
        },
        "gov.irs.income.bracket.thresholds.4.JOINT": {
            "2026-01-01.2026-12-31": 402725,
        },
        "gov.irs.income.bracket.thresholds.4.SEPARATE": {
            "2026-01-01.2026-12-31": 201350,
        },
        "gov.irs.income.bracket.thresholds.4.SINGLE": {
            "2026-01-01.2026-12-31": 201350,
        },
        "gov.irs.income.bracket.thresholds.4.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 402725,
        },
        "gov.irs.income.bracket.thresholds.5.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 255700,
        },
        "gov.irs.income.bracket.thresholds.5.JOINT": {
            "2026-01-01.2026-12-31": 511400,
        },
        "gov.irs.income.bracket.thresholds.5.SEPARATE": {
            "2026-01-01.2026-12-31": 255700,
        },
        "gov.irs.income.bracket.thresholds.5.SINGLE": {
            "2026-01-01.2026-12-31": 255700,
        },
        "gov.irs.income.bracket.thresholds.5.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 511400,
        },
        "gov.irs.income.bracket.thresholds.6.HEAD_OF_HOUSEHOLD": {
            "2026-01-01.2026-12-31": 639300,
        },
        "gov.irs.income.bracket.thresholds.6.JOINT": {
            "2026-01-01.2026-12-31": 767125,
        },
        "gov.irs.income.bracket.thresholds.6.SEPARATE": {
            "2026-01-01.2026-12-31": 383550,
        },
        "gov.irs.income.bracket.thresholds.6.SINGLE": {
            "2026-01-01.2026-12-31": 639300,
        },
        "gov.irs.income.bracket.thresholds.6.SURVIVING_SPOUSE": {
            "2026-01-01.2026-12-31": 767125,
        },
        "gov.irs.income.exemption.amount": {"2026-01-01.2100-12-31": 0},
    }


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
        salt_phase_out_enabled = reform_params["salt_phase_out_enabled"]
        other_tcja_provisions = reform_params.get("other_tcja_provisions", False)
        reform_dict = {}

        # SALT caps
        for status in salt_caps:
            reform_dict[
                f"gov.irs.deductions.itemized.salt_and_real_estate.cap.{status}"
            ] = {"2026-01-01.2100-12-31": salt_caps[status]}

        # SALT phase-out parameters
        if salt_phase_out_enabled:
            reform_dict["gov.contrib.salt_phase_out.in_effect"] = {
                "2026-01-01.2100-12-31": True
            }
            reform_dict["gov.contrib.salt_phase_out.rate.joint[1].rate"] = {
                "2026-01-01.2100-12-31": salt_phase_out_rate
            }
            reform_dict["gov.contrib.salt_phase_out.rate.joint[1].threshold"] = {
                "2026-01-01.2100-12-31": salt_phase_out_threshold_joint
            }
            reform_dict["gov.contrib.salt_phase_out.rate.other[1].rate"] = {
                "2026-01-01.2100-12-31": salt_phase_out_rate
            }
            reform_dict["gov.contrib.salt_phase_out.rate.other[1].threshold"] = {
                "2026-01-01.2100-12-31": salt_phase_out_threshold_other
            }
        for status in amt_phase_outs:
            reform_dict[f"gov.irs.income.amt.exemption.phase_out.start.{status}"] = {
                "2026-01-01.2100-12-31": amt_phase_outs[status]
            }
        for status in amt_exemptions:
            reform_dict[f"gov.irs.income.amt.exemption.amount.{status}"] = {
                "2026-01-01.2100-12-31": amt_exemptions[status]
            }

        if other_tcja_provisions:
            reform_dict.update(get_other_tcja_provisions())

        return reform_dict


def get_reform_params_from_config(policy_config):
    """Get reform parameters based on policy configuration.

    Note:
        To eliminate the marriage penalty for AMT parameters in Current Law,
        add `"amt_eliminate_marriage_penalty": True` to your policy config.
        This sets the AMT exemptions as follows:
            - SINGLE, HEAD_OF_HOUSEHOLD, SURVIVING_SPOUSE: 70,500
            - JOINT: 141,000 (and SEPARATE: 70,500)
        and the AMT phase‐out thresholds as:
            - SINGLE, HEAD_OF_HOUSEHOLD, SURVIVING_SPOUSE: 156,700
            - JOINT: 313,400 (and SEPARATE: 156,700).

        For the Current Policy configuration, we now also supply
        phase‐out thresholds based on scaled values from current law:
            - SINGLE, HEAD_OF_HOUSEHOLD, SURVIVING_SPOUSE: 200,700
            - JOINT: 268,000 (and SEPARATE: 134,000).
        These changes are also highlighted in the accompanying notebooks.
    """
    reform_params = {
        # Initialize with default values
        "salt_phase_out_enabled": False,
        "salt_phase_out_rate": 0,
        "salt_phase_out_threshold_joint": 0,
        "salt_phase_out_threshold_other": 0,
        "amt_phase_out_rate": 0,
        "amt_phase_out_threshold_joint": 0,
        "amt_phase_out_threshold_other": 0,
        "other_tcja_provisions": policy_config.get("other_tcja_provisions_extended")
        == "Current Policy",
    }

    # Handle SALT cap
    if policy_config["salt_cap"] == "Current Law (Uncapped)":
        reform_params["salt_caps"] = {
            "JOINT": float("inf"),
            "SEPARATE": float("inf"),
            "SINGLE": float("inf"),
            "HEAD_OF_HOUSEHOLD": float("inf"),
            "SURVIVING_SPOUSE": float("inf"),
        }
        # Add phase-out parameters if enabled for uncapped case
        if (
            policy_config.get("salt_phaseout")
            == "10% for income over 200k (400k joint)"
        ):
            reform_params["salt_phase_out_enabled"] = True
            reform_params["salt_phase_out_rate"] = 0.1
            reform_params["salt_phase_out_threshold_joint"] = 400_000
            reform_params["salt_phase_out_threshold_other"] = 200_000
    elif policy_config["salt_cap"] == "$15k":
        reform_params["salt_caps"] = {
            "JOINT": 15_000,
            "SEPARATE": 7_500,  # Half of joint for separate filers
            "SINGLE": 15_000,
            "HEAD_OF_HOUSEHOLD": 15_000,
            "SURVIVING_SPOUSE": 15_000,
        }
        # Add marriage bonus if selected
        if policy_config.get("salt_marriage_bonus"):
            reform_params["salt_caps"]["JOINT"] = 30_000
        if (
            policy_config.get("salt_phaseout")
            == "10% for income over 200k (400k joint)"
        ):
            reform_params["salt_phase_out_enabled"] = True
            reform_params["salt_phase_out_rate"] = 0.1
            reform_params["salt_phase_out_threshold_joint"] = 400_000
            reform_params["salt_phase_out_threshold_other"] = 200_000
    elif policy_config["salt_cap"] == "$100k":
        reform_params["salt_caps"] = {
            "JOINT": 100_000,
            "SEPARATE": 50_000,
            "SINGLE": 100_000,
            "HEAD_OF_HOUSEHOLD": 100_000,
            "SURVIVING_SPOUSE": 100_000,
        }
        # Add marriage bonus if selected
        if policy_config.get("salt_marriage_bonus"):
            reform_params["salt_caps"]["JOINT"] = 200_000
        if (
            policy_config.get("salt_phaseout")
            == "10% for income over 200k (400k joint)"
        ):
            reform_params["salt_phase_out_enabled"] = True
            reform_params["salt_phase_out_rate"] = 0.1
            reform_params["salt_phase_out_threshold_joint"] = 400_000
            reform_params["salt_phase_out_threshold_other"] = 200_000
    elif policy_config["salt_cap"] == "$0 Cap":
        reform_params["salt_caps"] = {
            "JOINT": 0,
            "SEPARATE": 0,
            "SINGLE": 0,
            "HEAD_OF_HOUSEHOLD": 0,
            "SURVIVING_SPOUSE": 0,
        }
    else:  # Current Policy ($10k)
        reform_params["salt_caps"] = {
            "JOINT": 10_000,
            "SEPARATE": 5_000,
            "SINGLE": 10_000,
            "HEAD_OF_HOUSEHOLD": 10_000,
            "SURVIVING_SPOUSE": 10_000,
        }

        # Add marriage bonus if selected
        if policy_config.get("salt_marriage_bonus"):
            reform_params["salt_caps"]["JOINT"] = 20_000

        # Add phase-out if selected
        if (
            policy_config.get("salt_phaseout")
            == "10% for income over 200k (400k joint)"
        ):
            reform_params["salt_phase_out_enabled"] = True
            reform_params["salt_phase_out_rate"] = 0.1
            reform_params["salt_phase_out_threshold_joint"] = 400_000
            reform_params["salt_phase_out_threshold_other"] = 200_000
    if policy_config.get("salt_repealed"):
        reform_params["salt_caps"] = {k: 0 for k in reform_params["salt_caps"].keys()}
    # Set AMT parameters
    if policy_config["amt_repealed"]:
        reform_params["amt_exemptions"] = {
            k: np.inf for k in reform_params["salt_caps"].keys()
        }
        reform_params["amt_phase_outs"] = {
            k: np.inf for k in reform_params["salt_caps"].keys()
        }
    else:
        if (
            policy_config["amt_exemption"]
            == "Current Policy ($89,925 Single, $139,850 Joint)"
        ):
            # Current Policy configuration for AMT: exemptions and phase-out thresholds.
            reform_params["amt_exemptions"] = {
                "JOINT": 140_565,
                "SEPARATE": 70_282,
                "SINGLE": 90_394,
                "HEAD_OF_HOUSEHOLD": 90_394,
                "SURVIVING_SPOUSE": 90_394,
            }
            reform_params["amt_phase_outs"] = {
                "JOINT": 268_000,
                "SEPARATE": 134_000,
                "SINGLE": 200_700,
                "HEAD_OF_HOUSEHOLD": 200_700,
                "SURVIVING_SPOUSE": 200_700,
            }
        else:  # Current Law
            if policy_config.get("amt_eliminate_marriage_penalty"):
                reform_params["amt_exemptions"] = {
                    "JOINT": 141_200,
                    "SEPARATE": 70_600,
                    "SINGLE": 70_600,
                    "HEAD_OF_HOUSEHOLD": 70_600,
                    "SURVIVING_SPOUSE": 70_600,
                }
                reform_params["amt_phase_outs"] = {
                    "JOINT": 313_800,
                    "SEPARATE": 156_900,
                    "SINGLE": 156_900,
                    "HEAD_OF_HOUSEHOLD": 156_900,
                    "SURVIVING_SPOUSE": 156_900,
                }
            else:
                reform_params["amt_exemptions"] = {
                    "JOINT": 109_800,
                    "SEPARATE": 54_900,
                    "SINGLE": 70_600,
                    "HEAD_OF_HOUSEHOLD": 70_600,
                    "SURVIVING_SPOUSE": 70_600,
                }
                reform_params["amt_phase_outs"] = {
                    "JOINT": 209_200,
                    "SEPARATE": 104_600,
                    "SINGLE": 156_900,
                    "HEAD_OF_HOUSEHOLD": 156_900,
                    "SURVIVING_SPOUSE": 156_900,
                }

    return reform_params
