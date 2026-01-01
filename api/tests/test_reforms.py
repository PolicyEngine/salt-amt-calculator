"""Tests for reform parameter generation."""

import pytest
import numpy as np
from salt_amt_api.simulation.reforms import (
    PolicyReforms,
    get_reform_params_from_config,
    CURRENT_POLICY_PARAMS,
)


class TestGetReformParamsFromConfig:
    """Tests for get_reform_params_from_config function."""

    def test_current_law_uncapped_returns_infinite_salt_caps(self):
        """Current Law (Uncapped) should return infinite SALT caps."""
        config = {"salt_cap": "Current Law (Uncapped)"}
        params = get_reform_params_from_config(config)

        assert params["salt_caps"]["SINGLE"] == float("inf")
        assert params["salt_caps"]["JOINT"] == float("inf")

    def test_current_policy_10k_cap(self):
        """Current Policy ($10k) should return $10k caps."""
        config = {"salt_cap": "Current Policy ($10k)"}
        params = get_reform_params_from_config(config)

        assert params["salt_caps"]["SINGLE"] == 10_000
        assert params["salt_caps"]["JOINT"] == 10_000
        assert params["salt_caps"]["SEPARATE"] == 5_000

    def test_15k_cap(self):
        """$15k option should return $15k caps."""
        config = {"salt_cap": "$15k"}
        params = get_reform_params_from_config(config)

        assert params["salt_caps"]["SINGLE"] == 15_000
        assert params["salt_caps"]["JOINT"] == 15_000
        assert params["salt_caps"]["SEPARATE"] == 7_500

    def test_marriage_bonus_doubles_joint_cap(self):
        """Marriage bonus should double the joint cap."""
        config = {"salt_cap": "$15k", "salt_marriage_bonus": True}
        params = get_reform_params_from_config(config)

        assert params["salt_caps"]["SINGLE"] == 15_000
        assert params["salt_caps"]["JOINT"] == 30_000  # Doubled

    def test_salt_repealed_sets_zero_caps(self):
        """SALT repealed should set all caps to zero."""
        config = {"salt_cap": "$15k", "salt_repealed": True}
        params = get_reform_params_from_config(config)

        assert all(v == 0 for v in params["salt_caps"].values())

    def test_amt_repealed_sets_infinite_exemptions(self):
        """AMT repealed should set infinite exemptions."""
        config = {"salt_cap": "$10k", "amt_repealed": True}
        params = get_reform_params_from_config(config)

        assert params["amt_exemptions"]["SINGLE"] == np.inf
        assert params["amt_exemptions"]["JOINT"] == np.inf

    def test_salt_phaseout_enables_phaseout(self):
        """SALT phaseout option should enable phaseout parameters."""
        config = {
            "salt_cap": "$10k",
            "salt_phaseout": "10% for income over 200k (400k joint)",
        }
        params = get_reform_params_from_config(config)

        assert params["salt_phase_out_enabled"] is True
        assert params["salt_phase_out_rate"] == 0.1
        assert params["salt_phase_out_threshold_joint"] == 400_000
        assert params["salt_phase_out_threshold_other"] == 200_000

    def test_current_policy_amt_exemption(self):
        """Current Policy AMT exemption should use higher values."""
        config = {
            "salt_cap": "$10k",
            "amt_exemption": "Current Policy ($89,925 Single, $139,850 Joint)",
        }
        params = get_reform_params_from_config(config)

        assert params["amt_exemptions"]["SINGLE"] == 90_394
        assert params["amt_exemptions"]["JOINT"] == 140_565

    def test_eliminate_marriage_penalty_doubles_joint_amt(self):
        """Eliminating marriage penalty should double joint AMT exemption."""
        config = {
            "salt_cap": "$10k",
            "amt_exemption": "Current Law ($70,500 Single, $109,500 Joint)",
            "amt_eliminate_marriage_penalty": True,
        }
        params = get_reform_params_from_config(config)

        # Joint should be ~2x single
        assert params["amt_exemptions"]["JOINT"] == 141_200
        assert params["amt_exemptions"]["SINGLE"] == 70_600


class TestPolicyReforms:
    """Tests for PolicyReforms class."""

    def test_policy_reforms_returns_dict(self):
        """policy_reforms should return a dictionary."""
        reform_dict = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)
        assert isinstance(reform_dict, dict)

    def test_policy_reforms_sets_salt_caps(self):
        """Reform dict should contain SALT cap parameters."""
        reform_dict = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)

        # Check that SALT cap keys exist
        assert any("salt_and_real_estate.cap" in k for k in reform_dict.keys())

    def test_policy_reforms_sets_amt_exemptions(self):
        """Reform dict should contain AMT exemption parameters."""
        reform_dict = PolicyReforms.policy_reforms(CURRENT_POLICY_PARAMS)

        # Check that AMT exemption keys exist
        assert any("amt.exemption.amount" in k for k in reform_dict.keys())

    def test_other_tcja_provisions_adds_many_params(self):
        """Enabling TCJA provisions should add many parameters."""
        params_without = {**CURRENT_POLICY_PARAMS, "other_tcja_provisions": False}
        params_with = {**CURRENT_POLICY_PARAMS, "other_tcja_provisions": True}

        reform_without = PolicyReforms.policy_reforms(params_without)
        reform_with = PolicyReforms.policy_reforms(params_with)

        # TCJA adds many more parameters
        assert len(reform_with) > len(reform_without)
