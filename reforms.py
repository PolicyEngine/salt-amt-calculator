class PolicyReforms:
    @staticmethod
    def policy_reforms(reform_params):
        """Reform for SALT cap and AMT adjustments with different values by filing status"""
        salt_caps = reform_params["salt_caps"]
        amt_exemptions = reform_params["amt_exemptions"]
        amt_phase_outs = reform_params["amt_phase_outs"]

        reform_dict = {}

        # SALT caps
        for status in salt_caps:
            reform_dict[
                f"gov.irs.deductions.itemized.salt_and_real_estate.cap.{status}"
            ] = {"2026-01-01.2100-12-31": salt_caps[status]}

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
