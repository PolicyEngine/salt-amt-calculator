"""Pydantic models for API requests and responses."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class HouseholdInput(BaseModel):
    """Household configuration for tax calculations."""

    state_code: str = Field(..., description="Two-letter US state code")
    is_married: bool = Field(default=False, description="Whether filing as married")
    num_children: int = Field(default=0, ge=0, le=10, description="Number of children")
    child_ages: list[int] = Field(default_factory=list, description="Ages of children")
    employment_income: float = Field(default=0, ge=0, description="Employment income")
    real_estate_taxes: float = Field(default=0, ge=0, description="Real estate taxes paid")
    qualified_dividend_income: float = Field(default=0, ge=0)
    long_term_capital_gains: float = Field(default=0, ge=0)
    short_term_capital_gains: float = Field(default=0, ge=0)
    deductible_mortgage_interest: float = Field(default=0, ge=0)
    charitable_cash_donations: float = Field(default=0, ge=0)


class PolicyConfig(BaseModel):
    """Policy configuration for SALT/AMT reforms."""

    salt_cap: str = Field(
        default="Current Law (Uncapped)",
        description="SALT cap option",
    )
    salt_marriage_bonus: bool = Field(
        default=False, description="Double SALT cap for married"
    )
    salt_phaseout: str = Field(default="None", description="SALT phase-out option")
    salt_repealed: bool = Field(default=False, description="Whether SALT is repealed")
    amt_exemption: str = Field(
        default="Current Law ($70,500 Single, $109,500 Joint)",
        description="AMT exemption option",
    )
    amt_phaseout: str = Field(
        default="Current Law ($156,700 Single, $209,000 Joint)",
        description="AMT phase-out option",
    )
    amt_repealed: bool = Field(default=False, description="Whether AMT is repealed")
    amt_eliminate_marriage_penalty: bool = Field(
        default=False, description="Double AMT exemption for joint filers"
    )
    other_tcja_provisions_extended: str = Field(
        default="Current Law", description="Other TCJA provisions"
    )


class SinglePointRequest(BaseModel):
    """Request for single-point household calculation."""

    household: HouseholdInput
    policy_config: Optional[PolicyConfig] = None
    baseline_scenario: Literal["Current Law", "Current Policy"] = "Current Law"


class SaltAxisRequest(BaseModel):
    """Request for SALT axis calculation (varying SALT, fixed income)."""

    household: HouseholdInput
    policy_config: Optional[PolicyConfig] = None
    baseline_scenario: Literal["Current Law", "Current Policy"] = "Current Law"
    min_salt: float = Field(default=0, description="Minimum SALT value")
    max_salt: float = Field(default=300000, description="Maximum SALT value")
    count: int = Field(default=600, description="Number of points")


class IncomeAxisRequest(BaseModel):
    """Request for income axis calculation (varying income, fixed SALT)."""

    household: HouseholdInput
    policy_config: Optional[PolicyConfig] = None
    baseline_scenario: Literal["Current Law", "Current Policy"] = "Current Law"
    min_income: float = Field(default=0, description="Minimum income value")
    max_income: float = Field(default=1000000, description="Maximum income value")
    count: int = Field(default=1000, description="Number of points")


class TwoAxesRequest(BaseModel):
    """Request for two-axes calculation (varying both SALT and income)."""

    household: HouseholdInput
    policy_config: Optional[PolicyConfig] = None
    baseline_scenario: Literal["Current Law", "Current Policy"] = "Current Law"
    min_salt: float = Field(default=-50000)
    max_salt: float = Field(default=250000)
    salt_count: int = Field(default=700)
    min_income: float = Field(default=0)
    max_income: float = Field(default=1000000)
    income_count: int = Field(default=1400)


class SinglePointResponse(BaseModel):
    """Response for single-point calculation."""

    household_net_income: float
    federal_income_tax: float
    state_income_tax: float
    state_sales_tax: float
    salt_deduction: float
    reported_salt: float
    regular_tax: float
    amt: float
    taxable_income: float
    amt_income: float
    larger_of_state_sales_or_income_tax: float
    state_income_tax_over_sales_tax: bool


class AxisResponse(BaseModel):
    """Response for axis calculations."""

    axis_values: list[float]
    salt_deduction: list[float]
    regular_tax: list[float]
    amt: list[float]
    income_tax: list[float]
    taxable_income: list[float]
    amt_income: list[float]
    reported_salt: Optional[list[float]] = None
    employment_income: Optional[list[float]] = None
    gap: Optional[list[float]] = None


class TwoAxesResponse(BaseModel):
    """Response for two-axes calculation."""

    employment_income: list[float]
    reported_salt: list[float]
    regular_tax: list[float]
    amt: list[float]
    salt_deduction: list[float]
    income_tax: list[float]
    taxable_income: list[float]
    amt_income: list[float]
    amt_binds: list[bool]
