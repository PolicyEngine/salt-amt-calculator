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

        # AMT exemptions
        for status in amt_exemptions:
            reform_dict[f"gov.irs.income.amt.exemption.amount.{status}"] = {
                "2023-01-01.2100-12-31": amt_exemptions[status]
            }

        # AMT phase-outs
        for status in amt_phase_outs:
            reform_dict[f"gov.irs.income.amt.exemption.phase_out.start.{status}"] = {
                "2023-01-01.2100-12-31": amt_phase_outs[status]
            }

        return reform_dict