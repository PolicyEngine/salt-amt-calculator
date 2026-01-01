"""Tests for situation builders."""

import pytest
from salt_amt_api.simulation.situation import (
    create_situation_without_axes,
    create_situation_with_one_property_tax_axes,
    create_situation_with_one_income_axes,
    create_situation_with_two_axes,
)


class TestCreateSituationWithoutAxes:
    """Tests for create_situation_without_axes function."""

    def test_creates_basic_situation(self):
        """Should create a valid situation dictionary."""
        situation = create_situation_without_axes(
            state_code="CA",
            real_estate_taxes=10000,
            is_married=False,
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=100000,
        )

        assert "people" in situation
        assert "households" in situation
        assert "tax_units" in situation
        assert "head" in situation["people"]

    def test_sets_state_code(self):
        """Should set the state code correctly."""
        situation = create_situation_without_axes(
            state_code="NY",
            real_estate_taxes=0,
            is_married=False,
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=0,
        )

        assert situation["households"]["household"]["state_code"]["2026"] == "NY"

    def test_adds_spouse_when_married(self):
        """Should add spouse when is_married is True."""
        situation = create_situation_without_axes(
            state_code="CA",
            real_estate_taxes=0,
            is_married=True,
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=0,
        )

        assert "spouse" in situation["people"]
        assert "spouse" in situation["households"]["household"]["members"]

    def test_adds_children(self):
        """Should add children with correct ages."""
        situation = create_situation_without_axes(
            state_code="CA",
            real_estate_taxes=0,
            is_married=False,
            num_children=2,
            child_ages=[5, 10],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=0,
        )

        assert "child_0" in situation["people"]
        assert "child_1" in situation["people"]
        assert situation["people"]["child_0"]["age"]["2026"] == 5
        assert situation["people"]["child_1"]["age"]["2026"] == 10

    def test_sets_income_values(self):
        """Should set income values correctly."""
        situation = create_situation_without_axes(
            state_code="CA",
            real_estate_taxes=15000,
            is_married=False,
            num_children=0,
            child_ages=[],
            qualified_dividend_income=5000,
            long_term_capital_gains=10000,
            short_term_capital_gains=2000,
            deductible_mortgage_interest=8000,
            charitable_cash_donations=3000,
            employment_income=150000,
        )

        head = situation["people"]["head"]
        assert head["employment_income"]["2026"] == 150000
        assert head["qualified_dividend_income"]["2026"] == 5000
        assert head["long_term_capital_gains"]["2026"] == 10000
        assert head["real_estate_taxes"]["2026"] == 15000


class TestCreateSituationWithOnePropertyTaxAxes:
    """Tests for create_situation_with_one_property_tax_axes function."""

    def test_creates_situation_with_salt_axis(self):
        """Should create situation with reported_salt axis."""
        situation = create_situation_with_one_property_tax_axes(
            is_married=False,
            state_code="CA",
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=100000,
        )

        assert "axes" in situation
        assert len(situation["axes"]) == 1
        assert situation["axes"][0][0]["name"] == "reported_salt"

    def test_uses_custom_axis_parameters(self):
        """Should use custom min, max, and count values."""
        situation = create_situation_with_one_property_tax_axes(
            is_married=False,
            state_code="CA",
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
            employment_income=100000,
            min_salt=1000,
            max_salt=50000,
            count=100,
        )

        axis = situation["axes"][0][0]
        assert axis["min"] == 1000
        assert axis["max"] == 50000
        assert axis["count"] == 100


class TestCreateSituationWithOneIncomeAxes:
    """Tests for create_situation_with_one_income_axes function."""

    def test_creates_situation_with_income_axis(self):
        """Should create situation with employment_income axis."""
        situation = create_situation_with_one_income_axes(
            is_married=False,
            state_code="CA",
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
        )

        assert "axes" in situation
        assert len(situation["axes"]) == 1
        assert situation["axes"][0][0]["name"] == "employment_income"


class TestCreateSituationWithTwoAxes:
    """Tests for create_situation_with_two_axes function."""

    def test_creates_situation_with_two_axes(self):
        """Should create situation with both salt and income axes."""
        situation = create_situation_with_two_axes(
            is_married=False,
            state_code="CA",
            num_children=0,
            child_ages=[],
            qualified_dividend_income=0,
            long_term_capital_gains=0,
            short_term_capital_gains=0,
            deductible_mortgage_interest=0,
            charitable_cash_donations=0,
        )

        assert "axes" in situation
        assert len(situation["axes"]) == 2
        assert situation["axes"][0][0]["name"] == "reported_salt"
        assert situation["axes"][1][0]["name"] == "employment_income"
