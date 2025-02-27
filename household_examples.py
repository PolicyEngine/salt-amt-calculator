import pandas as pd
import numpy as np

# Define state codes
STATE_CODES = {
    "New York": "NY",
    "California": "CA", 
    "Pennsylvania": "PA",
    "New Jersey": "NJ"
}

# Define income levels
INCOME_LEVELS = {
    "$100,000": 100000,
    "$250,000": 250000,
    "$500,000": 500000,
    "$1,000,000": 1000000
}

# Base household parameters (common across all examples)
BASE_HOUSEHOLD = {
    "is_married": True,
    "num_children": 0,
    "child_ages": [],
    "qualified_dividend_income": 0,
    "long_term_capital_gains": 0,
    "short_term_capital_gains": 0,
    "deductible_mortgage_interest": 15000,
    "charitable_cash_donations": 10000
}

# State-specific data (approximate values for demonstration)
# Using a single value for state and local sales or income tax
STATE_TAX_DATA = {
    "NY": {
        100000: {"state_local_tax": 4952},
        250000: {"state_local_tax": 14178},
        500000: {"state_local_tax": 31302},
        1000000: {"state_local_tax": 65553}
    },
    "CA": {
        100000: {"state_local_tax": 5196},
        250000: {"state_local_tax": 19146},
        500000: {"state_local_tax": 44051},
        1000000: {"state_local_tax": 103010}
    },
    "PA": {
        100000: {"state_local_tax": 3070},
        250000: {"state_local_tax": 7675},
        500000: {"state_local_tax": 15350},
        1000000: {"state_local_tax": 30700}
    },
    "NJ": {
        100000: {"state_local_tax": 4180},
        250000: {"state_local_tax": 13735},
        500000: {"state_local_tax": 29660},
        1000000: {"state_local_tax": 74484}
    }
}

# Example tax calculations for different property tax levels
# These would ideally be calculated dynamically using PolicyEngine
# For now, we'll use placeholder data that follows realistic patterns
TAX_CALCULATIONS = {
    "NY": {
        100000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 9952,
                    "regular_tax": 6928,
                    "amt": 0,
                    "federal_tax": 6928
                },
                "10k_property_taxes": {
                    "salt_deduction": 14952,
                    "regular_tax": 6155,
                    "amt": 0,
                    "federal_tax": 6155
                },
                "15k_property_taxes": {
                    "salt_deduction": 19952,
                    "regular_tax": 5381,
                    "amt": 0,
                    "federal_tax": 5381
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 9952,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        },
        # Add similar structures for other income levels
        250000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 19178,
                    "regular_tax": 37691,
                    "amt": 30979,
                    "federal_tax": 37691
                },
                "10k_property_taxes": {
                    "salt_deduction": 24178,
                    "regular_tax": 36401,
                    "amt": 30979,
                    "federal_tax": 36401
                },
                "15k_property_taxes": {
                    "salt_deduction": 29178,
                    "regular_tax": 35112,
                    "amt": 30979,
                    "federal_tax": 35112
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                }
            },
            "effective_salt_cap": {
                "current_law": 45278,
                "current_policy": 10000
            }
        },
        500000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 36303,
                    "regular_tax": 111604,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "10k_property_taxes": {
                    "salt_deduction": 41303,
                    "regular_tax": 109901,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "15k_property_taxes": {
                    "salt_deduction": 46303,
                    "regular_tax": 108199,
                    "amt": 115982,
                    "federal_tax": 115982
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                }
            },
            "effective_salt_cap": {
                "current_law": 32782,
                "current_policy": 10000
            }
        },
        1000000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 70553,
                    "regular_tax": 286919,
                    "amt": 268120,
                    "federal_tax": 286919
                },
                "10k_property_taxes": {
                    "salt_deduction": 75553,
                    "regular_tax": 284876,
                    "amt": 268120,
                    "federal_tax": 284876
                },
                "15k_property_taxes": {
                    "salt_deduction": 80553,
                    "regular_tax": 282834,
                    "amt": 268120,
                    "federal_tax": 282834
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        }
    },
    "CA": {
        100000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 10196,
                    "regular_tax": 6892,
                    "amt": 0,
                    "federal_tax": 6892
                },
                "10k_property_taxes": {
                    "salt_deduction": 15196,
                    "regular_tax": 6118,
                    "amt": 0,
                    "federal_tax": 6118
                },
                "15k_property_taxes": {
                    "salt_deduction": 20196,
                    "regular_tax": 5344,
                    "amt": 0,
                    "federal_tax": 5344
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        },
        250000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 24146,
                    "regular_tax": 36449,
                    "amt": 30979,
                    "federal_tax": 36449
                },
                "10k_property_taxes": {
                    "salt_deduction": 29146,
                    "regular_tax": 35159,
                    "amt": 30979,
                    "federal_tax": 35159
                },
                "15k_property_taxes": {
                    "salt_deduction": 34146,
                    "regular_tax": 33869,
                    "amt": 30979,
                    "federal_tax": 33869
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                }
            },
            "effective_salt_cap": {
                "current_law": 44051,
                "current_policy": 10000
            }
        },
        500000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 49051,
                    "regular_tax": 107397,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "10k_property_taxes": {
                    "salt_deduction": 54051,
                    "regular_tax": 105694,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "15k_property_taxes": {
                    "salt_deduction": 59051,
                    "regular_tax": 103992,
                    "amt": 115982,
                    "federal_tax": 115982
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                }
            },
            "effective_salt_cap": {
                "current_law": 23951,
                "current_policy": 10000
            }
        },
        1000000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 108010,
                    "regular_tax": 272086,
                    "amt": 268120,
                    "federal_tax": 272086
                },
                "10k_property_taxes": {
                    "salt_deduction": 113010,
                    "regular_tax": 270043,
                    "amt": 268120,
                    "federal_tax": 270043
                },
                "15k_property_taxes": {
                    "salt_deduction": 118010,
                    "regular_tax": 268001,
                    "amt": 268120,
                    "federal_tax": 268120
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                }
            },
            "effective_salt_cap": {
                "current_law": 117810,
                "current_policy": 10000
            }
        }
    },
    "PA": {
        100000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 8070,
                    "regular_tax": 7211,
                    "amt": 0,
                    "federal_tax": 7211
                },
                "10k_property_taxes": {
                    "salt_deduction": 13070,
                    "regular_tax": 6437,
                    "amt": 0,
                    "federal_tax": 6437
                },
                "15k_property_taxes": {
                    "salt_deduction": 18070,
                    "regular_tax": 5663,
                    "amt": 0,
                    "federal_tax": 5663
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 8070,
                    "regular_tax": 7527,
                    "amt": 0,
                    "federal_tax": 7527
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        },
        250000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 18735,
                    "regular_tax": 37802,
                    "amt": 30979,
                    "federal_tax": 37802
                },
                "10k_property_taxes": {
                    "salt_deduction": 23735,
                    "regular_tax": 36512,
                    "amt": 30979,
                    "federal_tax": 36512
                },
                "15k_property_taxes": {
                    "salt_deduction": 28735,
                    "regular_tax": 35222,
                    "amt": 30979,
                    "federal_tax": 35222
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                }
            },
            "effective_salt_cap": {
                "current_law": 44875,
                "current_policy": 10000
            }
        },
        500000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 20350,
                    "regular_tax": 116868,
                    "amt": 115982,
                    "federal_tax": 116868
                },
                "10k_property_taxes": {
                    "salt_deduction": 25350,
                    "regular_tax": 115166,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "15k_property_taxes": {
                    "salt_deduction": 30350,
                    "regular_tax": 113463,
                    "amt": 115982,
                    "federal_tax": 115982
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                }
            },
            "effective_salt_cap": {
                "current_law": 23050,
                "current_policy": 10000
            }
        },
        1000000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 35700,
                    "regular_tax": 300721,
                    "amt": 268120,
                    "federal_tax": 300721
                },
                "10k_property_taxes": {
                    "salt_deduction": 40700,
                    "regular_tax": 298678,
                    "amt": 268120,
                    "federal_tax": 298678
                },
                "15k_property_taxes": {
                    "salt_deduction": 45700,
                    "regular_tax": 296635,
                    "amt": 268120,
                    "federal_tax": 296635
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        }
    },
    "NJ": {
        100000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 9180,
                    "regular_tax": 7044,
                    "amt": 0,
                    "federal_tax": 7044
                },
                "10k_property_taxes": {
                    "salt_deduction": 14180,
                    "regular_tax": 6270,
                    "amt": 0,
                    "federal_tax": 6270
                },
                "15k_property_taxes": {
                    "salt_deduction": 19180,
                    "regular_tax": 5497,
                    "amt": 0,
                    "federal_tax": 5497
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 9180,
                    "regular_tax": 7393,
                    "amt": 0,
                    "federal_tax": 7393
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 7314,
                    "amt": 0,
                    "federal_tax": 7314
                }
            },
            "effective_salt_cap": {
                "current_law": float('inf'),
                "current_policy": 10000
            }
        },
        250000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 18735,
                    "regular_tax": 37802,
                    "amt": 30979,
                    "federal_tax": 37802
                },
                "10k_property_taxes": {
                    "salt_deduction": 23735,
                    "regular_tax": 36512,
                    "amt": 30979,
                    "federal_tax": 36512
                },
                "15k_property_taxes": {
                    "salt_deduction": 28735,
                    "regular_tax": 35222,
                    "amt": 30979,
                    "federal_tax": 35222
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 37035,
                    "amt": 21953,
                    "federal_tax": 37035
                }
            },
            "effective_salt_cap": {
                "current_law": 45235,
                "current_policy": 10000
            }
        },
        500000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 34660,
                    "regular_tax": 112146,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "10k_property_taxes": {
                    "salt_deduction": 39660,
                    "regular_tax": 110443,
                    "amt": 115982,
                    "federal_tax": 115982
                },
                "15k_property_taxes": {
                    "salt_deduction": 44660,
                    "regular_tax": 108741,
                    "amt": 115982,
                    "federal_tax": 115982
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 102017,
                    "amt": 103252,
                    "federal_tax": 103252
                }
            },
            "effective_salt_cap": {
                "current_law": 23760,
                "current_policy": 10000
            }
        },
        1000000: {
            "current_law": {
                "5k_property_taxes": {
                    "salt_deduction": 79484,
                    "regular_tax": 283383,
                    "amt": 268120,
                    "federal_tax": 283383
                },
                "10k_property_taxes": {
                    "salt_deduction": 84484,
                    "regular_tax": 281340,
                    "amt": 268120,
                    "federal_tax": 281340
                },
                "15k_property_taxes": {
                    "salt_deduction": 89484,
                    "regular_tax": 279297,
                    "amt": 268120,
                    "federal_tax": 279297
                }
            },
            "current_policy": {
                "5k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "10k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                },
                "15k_property_taxes": {
                    "salt_deduction": 10000,
                    "regular_tax": 279583,
                    "amt": 268120,
                    "federal_tax": 279583
                }
            },
            "effective_salt_cap": {
                "current_law": 112784,
                "current_policy": 10000
            }
        }
    }
}

def get_household_params(state, income):
    """
    Get the household parameters for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        dict: Household parameters
    """
    params = BASE_HOUSEHOLD.copy()
    params["state_code"] = state
    params["employment_income"] = income
    return params

def get_salt_deduction_table(state, income):
    """
    Generate the SALT deduction comparison table for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: SALT deduction comparison table
    """
    # This would ideally use real tax calculations
    # For now, we'll use the placeholder data
    state_tax_data = STATE_TAX_DATA[state][income]
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    
    current_law_5k = tax_calcs["current_law"]["5k_property_taxes"]["salt_deduction"]
    current_law_10k = tax_calcs["current_law"]["10k_property_taxes"]["salt_deduction"]
    current_policy_5k = tax_calcs["current_policy"]["5k_property_taxes"]["salt_deduction"]
    current_policy_10k = tax_calcs["current_policy"]["10k_property_taxes"]["salt_deduction"]
    
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": [f"${current_law_5k:,}", f"${current_policy_5k:,}"],
        "$10k property taxes": [f"${current_law_10k:,}", f"${current_policy_10k:,}"],
        "Difference": [f"${current_law_10k - current_law_5k:,}", f"${current_policy_10k - current_policy_5k:,}"],
    }
    
    return pd.DataFrame(comparison_data)

def get_tax_liability_table(state, income):
    """
    Generate the tax liability comparison table for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Tax liability comparison table
    """
    # This would ideally use real tax calculations
    # For now, we'll use the placeholder data
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    
    current_law_5k = tax_calcs["current_law"]["5k_property_taxes"]["regular_tax"]
    current_law_10k = tax_calcs["current_law"]["10k_property_taxes"]["regular_tax"]
    current_policy_5k = tax_calcs["current_policy"]["5k_property_taxes"]["regular_tax"]
    current_policy_10k = tax_calcs["current_policy"]["10k_property_taxes"]["regular_tax"]
    
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": [f"${current_law_5k:,}", f"${current_policy_5k:,}"],
        "$10k property taxes": [f"${current_law_10k:,}", f"${current_policy_10k:,}"],
        "Difference": [f"${current_law_10k - current_law_5k:,}", f"${current_policy_10k - current_policy_5k:,}"],
    }
    
    return pd.DataFrame(comparison_data)

def get_amt_table(state, income):
    """
    Generate the AMT comparison table for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: AMT comparison table
    """
    # This would ideally use real tax calculations
    # For now, we'll use the placeholder data
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    
    current_law_5k = tax_calcs["current_law"]["5k_property_taxes"]["amt"]
    current_law_10k = tax_calcs["current_law"]["10k_property_taxes"]["amt"]
    current_policy_5k = tax_calcs["current_policy"]["5k_property_taxes"]["amt"]
    current_policy_10k = tax_calcs["current_policy"]["10k_property_taxes"]["amt"]
    
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": [f"${current_law_5k:,}", f"${current_policy_5k:,}"],
        "$10k property taxes": [f"${current_law_10k:,}", f"${current_policy_10k:,}"],
        "Difference": [f"${current_law_10k - current_law_5k:,}", f"${current_policy_10k - current_policy_5k:,}"],
    }
    
    return pd.DataFrame(comparison_data)

def get_federal_tax_table(state, income):
    """
    Generate the federal tax comparison table for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Federal tax comparison table
    """
    # This would ideally use real tax calculations
    # For now, we'll use the placeholder data
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    
    current_law_5k = tax_calcs["current_law"]["5k_property_taxes"]["federal_tax"]
    current_law_10k = tax_calcs["current_law"]["10k_property_taxes"]["federal_tax"]
    current_policy_5k = tax_calcs["current_policy"]["5k_property_taxes"]["federal_tax"]
    current_policy_10k = tax_calcs["current_policy"]["10k_property_taxes"]["federal_tax"]
    
    # Calculate subsidy rates
    current_law_subsidy_rate = abs(round((current_law_10k - current_law_5k) / 5000 * 100))
    current_policy_subsidy_rate = abs(round((current_policy_10k - current_policy_5k) / 5000 * 100))
    
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": [f"${current_law_5k:,}", f"${current_policy_5k:,}"],
        "$10k property taxes": [f"${current_law_10k:,}", f"${current_policy_10k:,}"],
        "Difference": [f"${current_law_10k - current_law_5k:,}", f"${current_policy_10k - current_policy_5k:,}"],
        "Subsidy Rate": [f"{current_law_subsidy_rate}%", f"{current_policy_subsidy_rate}%"],
    }
    
    return pd.DataFrame(comparison_data)

def get_higher_property_tax_comparison(state, income):
    """
    Generate a comparison table for 10k and 15k property taxes
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Comparison table for 10k and 15k property taxes
    """
    # Use the existing data from TAX_CALCULATIONS
    tax_calcs = TAX_CALCULATIONS.get(state, TAX_CALCULATIONS["NY"]).get(income, TAX_CALCULATIONS["NY"][250000])
    
    # Extract values for 10k property taxes
    current_law_10k_salt = tax_calcs["current_law"]["10k_property_taxes"]["salt_deduction"]
    current_law_10k_regular = tax_calcs["current_law"]["10k_property_taxes"]["regular_tax"]
    current_law_10k_amt = tax_calcs["current_law"]["10k_property_taxes"]["amt"]
    current_law_10k_tax = tax_calcs["current_law"]["10k_property_taxes"]["federal_tax"]
    
    current_policy_10k_salt = tax_calcs["current_policy"]["10k_property_taxes"]["salt_deduction"]
    current_policy_10k_regular = tax_calcs["current_policy"]["10k_property_taxes"]["regular_tax"]
    current_policy_10k_amt = tax_calcs["current_policy"]["10k_property_taxes"]["amt"]
    current_policy_10k_tax = tax_calcs["current_policy"]["10k_property_taxes"]["federal_tax"]
    
    # Extract values for 15k property taxes
    current_law_15k_salt = tax_calcs["current_law"]["15k_property_taxes"]["salt_deduction"]
    current_law_15k_regular = tax_calcs["current_law"]["15k_property_taxes"]["regular_tax"]
    current_law_15k_amt = tax_calcs["current_law"]["15k_property_taxes"]["amt"]
    current_law_15k_tax = tax_calcs["current_law"]["15k_property_taxes"]["federal_tax"]
    
    current_policy_15k_salt = tax_calcs["current_policy"]["15k_property_taxes"]["salt_deduction"]
    current_policy_15k_regular = tax_calcs["current_policy"]["15k_property_taxes"]["regular_tax"]
    current_policy_15k_amt = tax_calcs["current_policy"]["15k_property_taxes"]["amt"]
    current_policy_15k_tax = tax_calcs["current_policy"]["15k_property_taxes"]["federal_tax"]
    
    # Calculate differences and subsidy rates
    current_law_diff = current_law_15k_tax - current_law_10k_tax
    current_policy_diff = current_policy_15k_tax - current_policy_10k_tax
    
    current_law_subsidy = abs(round(current_law_diff / 5000 * 100))
    current_policy_subsidy = abs(round(current_policy_diff / 5000 * 100))
    
    # Create the comparison data
    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$10k property taxes": [
            f"${current_law_10k_salt:,.0f}",
            f"${current_policy_10k_salt:,.0f}",
            f"${current_law_10k_regular:,.0f}",
            f"${current_policy_10k_regular:,.0f}",
            f"${current_law_10k_amt:,.0f}",
            f"${current_policy_10k_amt:,.0f}",
            f"${current_law_10k_tax:,.0f}",
            f"${current_policy_10k_tax:,.0f}",
        ],
        "$15k property taxes": [
            f"${current_law_15k_salt:,.0f}",
            f"${current_policy_15k_salt:,.0f}",
            f"${current_law_15k_regular:,.0f}",
            f"${current_policy_15k_regular:,.0f}",
            f"${current_law_15k_amt:,.0f}",
            f"${current_policy_15k_amt:,.0f}",
            f"${current_law_15k_tax:,.0f}",
            f"${current_policy_15k_tax:,.0f}",
        ],
        "Difference": [
            f"${current_law_15k_salt - current_law_10k_salt:,.0f}",
            f"${current_policy_15k_salt - current_policy_10k_salt:,.0f}",
            f"${current_law_15k_regular - current_law_10k_regular:,.0f}",
            f"${current_policy_15k_regular - current_policy_10k_regular:,.0f}",
            f"${current_law_15k_amt - current_law_10k_amt:,.0f}",
            f"${current_policy_15k_amt - current_policy_10k_amt:,.0f}",
            f"${current_law_diff:,.0f}",
            f"${current_policy_diff:,.0f}",
        ],
        "Subsidy Rate": [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            f"{current_law_subsidy}%",
            f"{current_policy_subsidy}%",
        ],
    }
    
    return pd.DataFrame(comparison_data)

def get_state_tax_description(state, income):
    """
    Get a description of the state tax situation for a specific state and income level
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        str: Description of state tax situation
    """
    state_tax_data = STATE_TAX_DATA[state][income]
    state_local_tax = state_tax_data["state_local_tax"]
    
    state_names = {
        "NY": "New York",
        "CA": "California",
        "PA": "Pennsylvania",
        "NJ": "New Jersey"
    }
    
    return f"{state_names[state]} levies state income taxes of ${state_local_tax:,} for this household, which can be deducted under the SALT deduction, in addition to the property taxes."

def get_comprehensive_tax_table(state, income):
    """
    Generate a comprehensive tax table showing all calculations for $5k and $10k property taxes
    
    Args:
        state (str): State name (NY, CA, PA, NJ)
        income (int): Income level
        
    Returns:
        pd.DataFrame: Comprehensive tax table
    """
    # Get the data from our existing functions
    salt_table = get_salt_deduction_table(state, income)
    tax_liability_table = get_tax_liability_table(state, income)
    amt_table = get_amt_table(state, income)
    federal_tax_table = get_federal_tax_table(state, income)
    
    # Extract values
    current_law_5k_salt = salt_table["$5k property taxes"][0]
    current_policy_5k_salt = salt_table["$5k property taxes"][1]
    current_law_10k_salt = salt_table["$10k property taxes"][0]
    current_policy_10k_salt = salt_table["$10k property taxes"][1]
    
    current_law_5k_regular = tax_liability_table["$5k property taxes"][0]
    current_policy_5k_regular = tax_liability_table["$5k property taxes"][1]
    current_law_10k_regular = tax_liability_table["$10k property taxes"][0]
    current_policy_10k_regular = tax_liability_table["$10k property taxes"][1]
    
    current_law_5k_amt = amt_table["$5k property taxes"][0]
    current_policy_5k_amt = amt_table["$5k property taxes"][1]
    current_law_10k_amt = amt_table["$10k property taxes"][0]
    current_policy_10k_amt = amt_table["$10k property taxes"][1]
    
    current_law_5k_federal = federal_tax_table["$5k property taxes"][0]
    current_policy_5k_federal = federal_tax_table["$5k property taxes"][1]
    current_law_10k_federal = federal_tax_table["$10k property taxes"][0]
    current_policy_10k_federal = federal_tax_table["$10k property taxes"][1]
    
    # Get subsidy rates
    current_law_subsidy = federal_tax_table["Subsidy Rate"][0]
    current_policy_subsidy = federal_tax_table["Subsidy Rate"][1]
    
    # Create the comprehensive table
    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$5k property taxes": [
            current_law_5k_salt,
            current_policy_5k_salt,
            current_law_5k_regular,
            current_policy_5k_regular,
            current_law_5k_amt,
            current_policy_5k_amt,
            current_law_5k_federal,
            current_policy_5k_federal,
        ],
        "$10k property taxes": [
            current_law_10k_salt,
            current_policy_10k_salt,
            current_law_10k_regular,
            current_policy_10k_regular,
            current_law_10k_amt,
            current_policy_10k_amt,
            current_law_10k_federal,
            current_policy_10k_federal,
        ],
        "Difference": [
            salt_table["Difference"][0],
            salt_table["Difference"][1],
            tax_liability_table["Difference"][0],
            tax_liability_table["Difference"][1],
            amt_table["Difference"][0],
            amt_table["Difference"][1],
            federal_tax_table["Difference"][0],
            federal_tax_table["Difference"][1],
        ],
        "Property Tax Subsidy Rate": [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            current_law_subsidy,
            current_policy_subsidy,
        ],
    }
    
    return pd.DataFrame(comparison_data)
