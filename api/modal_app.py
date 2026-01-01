"""Modal app for SALT-AMT calculator API."""

import modal

# Create the Modal app
app = modal.App("salt-amt-api")

# Define the image with dependencies and local package code
image = (
    modal.Image.debian_slim(python_version="3.13")
    .pip_install(
        "policyengine-us>=1.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
    )
    .add_local_dir("salt_amt_api", remote_path="/root/salt_amt_api")
)


@app.function(image=image, timeout=300)
@modal.fastapi_endpoint(method="GET")
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "salt-amt-api"}


@app.function(image=image, timeout=300)
@modal.fastapi_endpoint(method="POST")
def calculate_single(request: dict) -> dict:
    """Calculate tax values for a single household configuration."""
    import sys
    sys.path.insert(0, "/root")

    from salt_amt_api.models import SinglePointRequest, SinglePointResponse
    from salt_amt_api.simulation.calculation import calculate_single_point
    from salt_amt_api.simulation.reforms import get_reform_params_from_config

    # Parse request
    req = SinglePointRequest(**request)

    # Convert policy config to reform params if provided
    reform_params = None
    if req.policy_config:
        reform_params = get_reform_params_from_config(req.policy_config.model_dump())

    result = calculate_single_point(
        state_code=req.household.state_code,
        real_estate_taxes=req.household.real_estate_taxes,
        is_married=req.household.is_married,
        num_children=req.household.num_children,
        child_ages=req.household.child_ages,
        qualified_dividend_income=req.household.qualified_dividend_income,
        long_term_capital_gains=req.household.long_term_capital_gains,
        short_term_capital_gains=req.household.short_term_capital_gains,
        deductible_mortgage_interest=req.household.deductible_mortgage_interest,
        charitable_cash_donations=req.household.charitable_cash_donations,
        employment_income=req.household.employment_income,
        baseline_scenario=req.baseline_scenario,
        reform_params=reform_params,
    )

    return SinglePointResponse(**result).model_dump()


@app.function(image=image, timeout=600)
@modal.fastapi_endpoint(method="POST")
def calculate_salt_axis(request: dict) -> dict:
    """Calculate tax values along the SALT axis (varying SALT, fixed income)."""
    import sys
    sys.path.insert(0, "/root")

    from salt_amt_api.models import SaltAxisRequest, AxisResponse
    from salt_amt_api.simulation.calculation import calculate_salt_axis as calc_salt_axis
    from salt_amt_api.simulation.reforms import get_reform_params_from_config

    req = SaltAxisRequest(**request)

    reform_params = None
    if req.policy_config:
        reform_params = get_reform_params_from_config(req.policy_config.model_dump())

    result = calc_salt_axis(
        is_married=req.household.is_married,
        state_code=req.household.state_code,
        num_children=req.household.num_children,
        child_ages=req.household.child_ages,
        qualified_dividend_income=req.household.qualified_dividend_income,
        long_term_capital_gains=req.household.long_term_capital_gains,
        short_term_capital_gains=req.household.short_term_capital_gains,
        deductible_mortgage_interest=req.household.deductible_mortgage_interest,
        charitable_cash_donations=req.household.charitable_cash_donations,
        employment_income=req.household.employment_income,
        baseline_scenario=req.baseline_scenario,
        reform_params=reform_params,
        min_salt=req.min_salt,
        max_salt=req.max_salt,
        count=req.count,
    )

    return AxisResponse(**result).model_dump()


@app.function(image=image, timeout=600)
@modal.fastapi_endpoint(method="POST")
def calculate_income_axis(request: dict) -> dict:
    """Calculate tax values along the income axis (varying income)."""
    import sys
    sys.path.insert(0, "/root")

    from salt_amt_api.models import IncomeAxisRequest, AxisResponse
    from salt_amt_api.simulation.calculation import calculate_income_axis as calc_income_axis
    from salt_amt_api.simulation.reforms import get_reform_params_from_config

    req = IncomeAxisRequest(**request)

    reform_params = None
    if req.policy_config:
        reform_params = get_reform_params_from_config(req.policy_config.model_dump())

    result = calc_income_axis(
        is_married=req.household.is_married,
        state_code=req.household.state_code,
        num_children=req.household.num_children,
        child_ages=req.household.child_ages,
        qualified_dividend_income=req.household.qualified_dividend_income,
        long_term_capital_gains=req.household.long_term_capital_gains,
        short_term_capital_gains=req.household.short_term_capital_gains,
        deductible_mortgage_interest=req.household.deductible_mortgage_interest,
        charitable_cash_donations=req.household.charitable_cash_donations,
        baseline_scenario=req.baseline_scenario,
        reform_params=reform_params,
        min_income=req.min_income,
        max_income=req.max_income,
        count=req.count,
    )

    return AxisResponse(**result).model_dump()


@app.function(image=image, timeout=900, memory=4096)
@modal.fastapi_endpoint(method="POST")
def calculate_two_axes(request: dict) -> dict:
    """Calculate tax values on a 2D grid (SALT x income)."""
    import sys
    sys.path.insert(0, "/root")

    from salt_amt_api.models import TwoAxesRequest, TwoAxesResponse
    from salt_amt_api.simulation.calculation import calculate_two_axes as calc_two_axes
    from salt_amt_api.simulation.reforms import get_reform_params_from_config

    req = TwoAxesRequest(**request)

    reform_params = None
    if req.policy_config:
        reform_params = get_reform_params_from_config(req.policy_config.model_dump())

    result = calc_two_axes(
        is_married=req.household.is_married,
        state_code=req.household.state_code,
        num_children=req.household.num_children,
        child_ages=req.household.child_ages,
        qualified_dividend_income=req.household.qualified_dividend_income,
        long_term_capital_gains=req.household.long_term_capital_gains,
        short_term_capital_gains=req.household.short_term_capital_gains,
        deductible_mortgage_interest=req.household.deductible_mortgage_interest,
        charitable_cash_donations=req.household.charitable_cash_donations,
        baseline_scenario=req.baseline_scenario,
        reform_params=reform_params,
        min_salt=req.min_salt,
        max_salt=req.max_salt,
        salt_count=req.salt_count,
        min_income=req.min_income,
        max_income=req.max_income,
        income_count=req.income_count,
    )

    return TwoAxesResponse(**result).model_dump()


if __name__ == "__main__":
    # For local testing
    app.serve()
