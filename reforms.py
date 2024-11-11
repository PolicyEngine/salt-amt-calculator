class PolicyReforms:
    @staticmethod
    def policy_reforms(cap_amount):
        """Example of how to combine multiple policy changes"""
        return {
            "gov.irs.deductions.itemized.salt_and_real_estate.cap.HEAD_OF_HOUSEHOLD": {
                "2025-01-01.2100-12-31": cap_amount
            }
            # "other.policy.parameter": {
            #     "2025-01-01.2100-12-31": other_parameter
            # }
        }
