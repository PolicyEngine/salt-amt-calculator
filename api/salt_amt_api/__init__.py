"""SALT-AMT Calculator API package."""

from .models import (
    HouseholdInput,
    PolicyConfig,
    SinglePointRequest,
    SinglePointResponse,
    SaltAxisRequest,
    IncomeAxisRequest,
    TwoAxesRequest,
    AxisResponse,
    TwoAxesResponse,
)
from .simulation import (
    PolicyReforms,
    get_reform_params_from_config,
    calculate_single_point,
    calculate_salt_axis,
    calculate_income_axis,
    calculate_two_axes,
)

__version__ = "0.1.0"

__all__ = [
    # Models
    "HouseholdInput",
    "PolicyConfig",
    "SinglePointRequest",
    "SinglePointResponse",
    "SaltAxisRequest",
    "IncomeAxisRequest",
    "TwoAxesRequest",
    "AxisResponse",
    "TwoAxesResponse",
    # Simulation
    "PolicyReforms",
    "get_reform_params_from_config",
    "calculate_single_point",
    "calculate_salt_axis",
    "calculate_income_axis",
    "calculate_two_axes",
]
