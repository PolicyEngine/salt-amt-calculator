import pandas as pd
from pathlib import Path


class NationwideImpacts:
    def __init__(self):
        """Initialize nationwide impacts data loader"""
        self.data_dir = Path(__file__).parent / "data" / "impacts_2026_2035"
        self.single_year_impacts = self._load_data("impacts_2026.csv")
        self.budget_window_impacts = self._load_budget_window_impacts()

        # Parse available options from reform names when data is loaded
        if not self.single_year_impacts.empty:
            self.filter_options = self._parse_reform_options()
            self.income_cols = [
                col
                for col in self.single_year_impacts.columns
                if col.startswith("income_p")
            ]

    def _load_data(self, filename):
        """Load impact data with error handling for malformed CSV files"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"Warning: File not found: {filename}")
            return pd.DataFrame()

        try:
            # Explicitly list all numeric columns from the CSV
            numeric_cols = [
                "total_income_change",
                "pct_better_off",
                "pct_worse_off",
            ] + [f"income_p{i:02d}_{i+10}" for i in range(0, 100, 10)]

            df = pd.read_csv(
                filepath,
                on_bad_lines="skip",
                dtype={col: float for col in numeric_cols},
            )

            return df
        except Exception as e:
            print(f"Warning: Error loading {filename}: {str(e)}")
            return pd.DataFrame()

    def _load_budget_window_impacts(self):
        """Load and combine yearly impact files for the budget window."""
        years = range(2026, 2036)
        dfs = []

        for year in years:
            filename = f"impacts_{year}.csv"
            filepath = self.data_dir / filename
            if filepath.exists():
                try:
                    df = pd.read_csv(filepath)
                    df["year"] = year
                    dfs.append(df)
                except Exception as e:
                    print(f"Warning: Error loading {filename}: {str(e)}")
            else:
                print(f"Warning: File not found: {filename}")

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)

            return combined_df
        else:
            return pd.DataFrame()

    def _parse_reform_options(self):
        """Parse reform names to extract filter options."""
        # Get unique reform names from the data
        reform_names = (
            self.single_year_impacts["reform"].unique()
            if "reform" in self.single_year_impacts.columns
            else []
        )

        filter_options = {
            "amt_type": set(),
            "tcja_status": set(),
            "behavioral_response": set(),
            "salt_cap": set(),  # Add this line to track SALT cap options
        }

        for reform in reform_names:
            if not isinstance(reform, str):
                continue

            parts = reform.split("_")

            # Skip if this isn't a SALT reform
            if "salt" not in parts:
                continue

            try:
                salt_idx = parts.index("salt")

                # Extract SALT cap type
                if "15_30" in reform:
                    filter_options["salt_cap"].add("15_30_k")
                elif "0_cap" in reform:
                    filter_options["salt_cap"].add("0_cap")
                elif "tcja" in reform:
                    filter_options["salt_cap"].add("tcja_base")

                # Extract AMT type
                amt_parts = []
                for part in parts[salt_idx + 1 :]:
                    if part in [
                        "amt",
                        "repealed",
                        "extended",
                        "behavioral",
                        "responses",
                    ]:
                        break
                    amt_parts.append(part)
                if amt_parts:
                    filter_options["amt_type"].add("_".join(amt_parts))

                # Extract TCJA status
                if "tcja" in parts:
                    tcja_status = None
                    if "extended" in parts:
                        tcja_status = "extended"
                    elif "repealed" in parts:
                        tcja_status = "repealed"
                    if tcja_status:
                        filter_options["tcja_status"].add(tcja_status)

                # Extract behavioral response
                if "behavioral" in parts:
                    response = (
                        "yes" if parts[parts.index("behavioral") + 2] == "yes" else "no"
                    )
                    filter_options["behavioral_response"].add(response)

            except (ValueError, IndexError):
                continue

        return filter_options

    def filter_reforms(
        self,
        tcja=None,
        salt_cap=None,
        salt_phase_out=None,
        amt_exemptions=None,
        amt_phase_out=None,
        behavioral=None,
    ):
        """Filter reforms based on selected options"""
        df = self.single_year_impacts.copy()

        if df.empty:
            return df

        mask = pd.Series(True, index=df.index)

        if tcja is not None:
            mask &= df["reform"].str.contains(
                "extended" if tcja == "extended" else "repealed"
            )

        if salt_cap is not None:
            if salt_cap == "15_30":
                mask &= df["reform"].str.contains("salt_15_30_k")
            elif salt_cap == "0_cap":
                mask &= df["reform"].str.contains("salt_0_cap")
            else:
                mask &= df["reform"].str.contains("salt_tcja")

        if salt_phase_out is not None:
            mask &= df["reform"].str.contains(salt_phase_out)

        if amt_exemptions is not None:
            mask &= df["reform"].str.contains(f"amt_{amt_exemptions}_")

        if amt_phase_out is not None:
            mask &= df["reform"].str.contains(amt_phase_out)

        if behavioral is not None:
            mask &= df["reform"].str.contains(
                "behavioral_responses_yes_"
                if behavioral
                else "behavioral_responses_no_"
            )

        return df[mask]

    def get_available_reforms(self):
        """Get list of available reforms"""
        reforms = set()
        if not self.single_year_impacts.empty:
            reforms.update(self.single_year_impacts["reform"].unique())
        if not self.budget_window_impacts.empty:
            reforms.update(self.budget_window_impacts["reform"].unique())
        return sorted(list(reforms))

    def get_reform_impact(self, reform_name, impact_type="single_year"):
        """Get impact data for specific reform"""
        data = (
            self.single_year_impacts
            if impact_type == "single_year"
            else self.budget_window_impacts
        )
        if data.empty:
            print(f"No data available for impact type: {impact_type}")
            return None

        reform_data = data[data["reform"] == reform_name]
        if reform_data.empty:
            return None

        return reform_data

    def get_income_distribution(self, reform_name):
        """Get income distribution impacts for a reform"""
        if self.single_year_impacts.empty:
            return None

        # Define the income columns in order
        self.income_cols = [
            "avg_income_change_p10_20",
            "avg_income_change_p20_30",
            "avg_income_change_p30_40",
            "avg_income_change_p40_50",
            "avg_income_change_p50_60",
            "avg_income_change_p60_70",
            "avg_income_change_p70_80",
            "avg_income_change_p80_90",
            "avg_income_change_p90_100",
            "avg_income_change_p100_110",
        ]

        reform_data = self.single_year_impacts[
            self.single_year_impacts["reform"] == reform_name
        ]
        if reform_data.empty:
            return None

        return (
            reform_data[self.income_cols]
            .iloc[0]
            .rename(lambda x: x.replace("avg_income_change_p", ""))
        )

    def get_time_series(self, reform_name):
        """Get time series data for a specific reform."""
        # Check if data is loaded
        if self.budget_window_impacts is None or self.budget_window_impacts.empty:
            return None

        # Ensure 'reform' column exists
        if "reform" not in self.budget_window_impacts.columns:
            return None

        # Get reform data
        reform_data = self.budget_window_impacts[
            self.budget_window_impacts["reform"] == reform_name
        ]

        if reform_data.empty:
            return None

        return reform_data

    def get_filter_options(self):
        """Get all available filter options"""
        if not hasattr(self, "filter_options"):
            return {}
        return self.filter_options


def get_reform_name(policy_config, baseline, year=None):
    """Construct reform name to match CSV format based on policy config and baseline.

    Parameters:
        policy_config (dict): The policy configuration.
        baseline (str): The baseline scenario ("Current Law" or "Current Policy").
        year (int, optional): The year for budget window impacts (2027-2035). If None, assumes 2026.

    Returns:
        str: The reform name.
    """
    # Determine SALT component of the reform name
    if policy_config["salt_cap"] == "Current Law (Uncapped)":
        salt_full = "salt_uncapped"
    elif policy_config["salt_cap"] == "$15k":
        if policy_config.get("salt_marriage_bonus"):
            if policy_config.get("salt_phaseout") != "None":
                salt_full = "salt_15_30_k_with_phaseout"
            else:
                salt_full = "salt_15_30_k_without_phaseout"
        else:
            if policy_config.get("salt_phaseout") != "None":
                salt_full = "salt_15_k_with_phaseout"
            else:
                salt_full = "salt_15_k_without_phaseout"
    else:  # Current Policy for SALT cap
        salt_full = "salt_tcja_base"

    # Handle AMT suffix based on configuration
    if policy_config.get("amt_repealed"):
        amt_suffix = "_amt_repealed"
    else:
        exemption = policy_config.get("amt_exemption")
        phaseout = policy_config.get("amt_phaseout")
        # Check for elimination of the marriage penalty
        if exemption == "Current Law ($70,500 Single, $109,500 Joint)":
            if policy_config.get("amt_eliminate_marriage_penalty"):
                amt_suffix = "_amt_nmp"  # New suffix for "no marriage penalty"
            else:
                if phaseout == "Current Law ($156,700 Single, $209,000 Joint)":
                    amt_suffix = "_amt_tcja_both"
                elif phaseout == "Current Policy ($639,300 Single, $1,278,575 Joint)":
                    amt_suffix = "_amt_pre_tcja_ex_tcja_po"
                else:
                    amt_suffix = ""
        elif exemption == "Current Policy ($89,925 Single, $139,850 Joint)":
            if phaseout == "Current Policy ($639,300 Single, $1,278,575 Joint)":
                amt_suffix = "_amt_pre_tcja_ex_pre_tcja_po"
            elif phaseout == "Current Law ($156,700 Single, $209,000 Joint)":
                amt_suffix = "_amt_tcja_ex_pre_tcja_po"
            else:
                amt_suffix = ""
        else:
            amt_suffix = ""

    # Append additional suffixes for behavioral responses and other TCJA provisions
    behavioral_suffix = (
        "_behavioral_responses_yes"
        if policy_config.get("behavioral_responses")
        else "_behavioral_responses_no"
    )

    other_tcja_provisions_suffix = (
        "_other_tcja_provisions_extended_no"
        if policy_config.get("other_tcja_provisions_extended") == "Current Law"
        else "_other_tcja_provisions_extended_yes"
    )

    # Append baseline suffix
    baseline_suffix = f"_vs_{baseline.lower().replace(' ', '_')}"
    # Append year suffix for budget window impacts (2027-2035)
    if year is not None and year >= 2027:
        year_suffix = f"_year_{year}"
    else:
        year_suffix = ""

    reform_name = f"{salt_full}{amt_suffix}{behavioral_suffix}{other_tcja_provisions_suffix}{year_suffix}{baseline_suffix}"
    return reform_name


def calculate_total_revenue_impact(budget_window_impacts_df, policy_config, baseline):
    """Calculate total revenue impact across all years for a given reform.

    Parameters:
        budget_window_impacts_df (pd.DataFrame): Concatenated DataFrame of budget window impacts
        policy_config (dict): The policy configuration
        baseline (str): The baseline scenario

    Returns:
        float: Total revenue impact across all years
    """
    reform_name = get_reform_name(
        policy_config,
        baseline,
        year=2026,  # Base reform name without year
    )
    reform_base = reform_name.split("_vs_")[0]  # Get the base reform name up to "_vs_"

    return budget_window_impacts_df[
        budget_window_impacts_df["reform"].str.contains(reform_base)
    ]["total_income_change"].sum()
