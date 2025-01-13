import streamlit as st
from personal_calculator.situation import create_situation
from personal_calculator.calculator import calculate_impacts
from personal_calculator.inputs import create_personal_inputs
from personal_calculator.policy_parameters import create_policy_inputs
from personal_calculator.chart import (
    create_reform_comparison_graph,
    initialize_results_tracking,
    update_results,
    reset_results,
)
import numpy as np
from personal_calculator.table import create_summary_table
from nationwide_impacts.impacts import NationwideImpacts
from nationwide_impacts.charts import ImpactCharts
from nationwide_impacts.tables import display_summary_metrics
import pandas as pd
from baseline_impacts import display_baseline_impacts
from policy_config import display_policy_config
from personal_calculator.reforms import get_reform_params_from_config
from nationwide_impacts.charts import ImpactCharts

# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator", layout="wide")

# Title
st.title("What's the SALTernative?")
st.markdown(
    "Design and compare changes to the state and local tax (SALT) deduction and alternative minimum tax (AMT)"
)

# Initialize nationwide impacts if not already done
if "nationwide_impacts" not in st.session_state:
    try:
        st.session_state.nationwide_impacts = NationwideImpacts()
    except Exception as e:
        st.error(f"Error loading nationwide impacts data: {str(e)}")

# Display baseline impacts section first
display_baseline_impacts()

# Display policy configuration section after baseline impacts
st.markdown("---")
policy_config = display_policy_config()

# Create tabs and store active tab in session state
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0  # Default to first tab

st.markdown("---")

st.subheader("Impacts")

nationwide_tab, calculator_tab = st.tabs(["US", "Household"])

# Display nationwide impacts first
with nationwide_tab:
    st.markdown(
        """
    This section shows the nationwide impacts of the your policy configuration.
    """
    )

    # Add baseline selector radio button here
    baseline = st.radio(
        "Baseline Scenario",
        ["Current Law", "Current Policy"],
        help="Choose whether to compare against Current Law or Current Policy (TCJA Extended)",
    )

    # Store baseline in session state
    st.session_state.baseline = baseline

    if not hasattr(st.session_state, "nationwide_impacts"):
        st.error("No impact data available. Please check data files.")
    else:
        # Construct reform name to match CSV format based on policy config and baseline
        def get_reform_name(policy_config, baseline):
            """Construct reform name to match CSV format based on policy config and baseline"""
            # Handle SALT cap base option
            if policy_config["salt_cap"] == "Uncapped":
                # Check if phase-out is enabled for uncapped case
                salt_full = "salt_uncapped"
            elif policy_config["salt_repealed"]:
                salt_full = "salt_0_cap"
            else:  # Current Policy selected
                salt_base = "salt_tcja_base"
                marriage_bonus = policy_config.get("salt_marriage_bonus", False)
                phase_out = policy_config.get("salt_phaseout") != "None"

                if marriage_bonus and phase_out:
                    salt_full = "salt_tcja_married_bonus_and_phase_out"
                elif marriage_bonus:
                    salt_full = f"{salt_base}_with_married_bonus"
                elif phase_out:
                    salt_full = f"{salt_base}_with_phaseout"
                else:
                    salt_full = salt_base

            # Handle AMT suffix based on configuration
            if policy_config.get("amt_repealed"):
                amt_suffix = "_amt_repealed"
            else:
                exemption = policy_config.get("amt_exemption")
                phaseout = policy_config.get("amt_phaseout")

                # Map the combinations to their correct suffixes
                if exemption == "Current Law" and phaseout == "Current Law":
                    amt_suffix = "_amt_tcja_both"
                elif exemption == "Current Law" and phaseout == "Current Policy":
                    amt_suffix = "_amt_pre_tcja_ex_tcja_po"
                elif exemption == "Current Policy" and phaseout == "Current Policy":
                    amt_suffix = "_amt_pre_tcja_ex_pre_tcja_po"
                elif exemption == "Current Policy" and phaseout == "Current Law":
                    amt_suffix = "_amt_tcja_ex_pre_tcja_po"

            # Add behavioral response suffix
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

            # Add baseline suffix
            baseline_suffix = f"_vs_{baseline.lower().replace(' ', '_')}"

            # Add other TCJA provisions suffix
            return f"{salt_full}{amt_suffix}{behavioral_suffix}{other_tcja_provisions_suffix}{baseline_suffix}"

        reform_name = get_reform_name(
            st.session_state.policy_config, st.session_state.baseline
        )
        impacts_data = (
            st.session_state.nationwide_impacts.single_year_impacts
        )  # Access single_year_impacts directly
        reform_impacts = impacts_data[impacts_data["reform"] == reform_name]
        if reform_impacts.empty:
            st.warning(f"Debug: Looking for reform '{reform_name}'")  # Debug line
        filtered_impacts = display_summary_metrics(
            reform_impacts, st.session_state.baseline
        )

        # Filter the data to get the matching row
        filtered_data = impacts_data[impacts_data["reform"] == reform_name]

        if filtered_data.empty:
            st.warning("No data available for this combination of policy options.")
        else:
            # Create radio for impact period selection
            impact_type = st.radio(
                "Select Impact Period",
                ["single_year", "budget_window"],
                format_func=lambda x: (
                    "2026 Impact" if x == "single_year" else "10-Year Impact"
                ),
                horizontal=True,
            )

            # Get impact data for the filtered combination
            impact_data = st.session_state.nationwide_impacts.get_reform_impact(
                reform_name, impact_type
            )

            if impact_data is not None:
                # Show appropriate visualization based on impact_type
                if impact_type == "single_year":
                    # Get and plot income distribution data
                    dist_data = (
                        st.session_state.nationwide_impacts.get_income_distribution(
                            filtered_data.iloc[0]["reform"]
                        )
                    )
                    if dist_data is not None:
                        fig = ImpactCharts.plot_distributional_analysis(dist_data)
                        st.plotly_chart(fig, use_container_width=True)
                else:  # budget_window
                    # Get and plot time series data
                    time_data = st.session_state.nationwide_impacts.get_time_series(
                        filtered_data.iloc[0]["reform"]
                    )
                    if time_data is not None:
                        fig = ImpactCharts.plot_time_series(time_data)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No impact data available for this combination.")

    # Add Notes section
    st.markdown("---")

# Then display calculator tab
with calculator_tab:
    st.markdown(
        """
    This calculator shows the household-level impacts of the your policy configuration.
    Input your household characteristics below.
    """
    )

    # Get personal inputs
    personal_inputs = create_personal_inputs()

    # Initialize results tracking in session state if not exists
    if "results_df" not in st.session_state:
        st.session_state.results_df, st.session_state.summary_results = (
            initialize_results_tracking()
        )

    # Create columns for calculate button alignment
    calc_col1, calc_col2 = st.columns([1, 8])
    with calc_col1:
        calculate_clicked = st.button("Calculate Impacts", use_container_width=True)

    if calculate_clicked:
        # Reset results to start fresh
        reset_results()

        # Create situation based on inputs
        situation = create_situation(
            state_code=personal_inputs["state_code"],
            employment_income=personal_inputs["employment_income"],
            spouse_income=personal_inputs["spouse_income"],
            head_age=personal_inputs["head_age"],
            is_married=personal_inputs["is_married"],
            spouse_age=personal_inputs["spouse_age"],
            num_children=personal_inputs["num_children"],
            child_ages=personal_inputs["child_ages"],
            qualified_dividend_income=personal_inputs["qualified_dividend_income"],
            long_term_capital_gains=personal_inputs["long_term_capital_gains"],
            short_term_capital_gains=personal_inputs["short_term_capital_gains"],
            real_estate_taxes=personal_inputs["real_estate_taxes"],
        )

        # Display results in a nice format
        st.markdown("### Results")

        # Create placeholder for chart and status message
        chart_placeholder = st.empty()
        status_placeholder = st.empty()

        # Calculate current law first
        status_placeholder.info("Calculating current law...")
        results = calculate_impacts(situation, {})
        current_law_income = results["current_law"]

        # Update current law results
        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            "Current Law",
            current_law_income,
        )

        # Calculate current policy
        status_placeholder.info("Calculating current policy...")
        current_policy_params = {
            "reform_current_policy": {
                "salt_caps": {
                    "JOINT": 10_000,
                    "SEPARATE": 5_000,
                    "SINGLE": 10_000,
                    "HEAD_OF_HOUSEHOLD": 10_000,
                    "SURVIVING_SPOUSE": 10_000,
                },
                "amt_exemptions": {
                    "JOINT": 140_565,
                    "SEPARATE": 70_283,
                    "SINGLE": 90_394,
                    "HEAD_OF_HOUSEHOLD": 90_394,
                    "SURVIVING_SPOUSE": 90_394,
                },
                "amt_phase_outs": {
                    "JOINT": 1_285_409,
                    "SEPARATE": 642_705,
                    "SINGLE": 642_705,
                    "HEAD_OF_HOUSEHOLD": 642_705,
                    "SURVIVING_SPOUSE": 642_705,
                },
                "salt_phase_out_enabled": False,
                "salt_phase_out_rate": 0,
                "salt_phase_out_threshold_joint": 0,
                "salt_phase_out_threshold_other": 0,
            }
        }

        current_policy_results = calculate_impacts(situation, current_policy_params)
        current_policy_income = (
            current_law_income + current_policy_results["reform_current_policy_impact"]
        )

        # Update current policy results
        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            "Current Policy",
            current_policy_income,
        )

        # Calculate your policy configuration
        status_placeholder.info("Calculating your policy...")
        reform_params = get_reform_params_from_config(st.session_state.policy_config)
        reform_results = calculate_impacts(
            situation, {"selected_reform": reform_params}
        )
        reform_income = current_law_income + reform_results["selected_reform_impact"]

        # Update reform results
        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            "Your Policy",
            reform_income,
        )

        # Update chart with all results
        fig = create_reform_comparison_graph(st.session_state.summary_results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Clear status message when complete
        status_placeholder.empty()

        # Create summary table
        create_summary_table(
            current_law_income, st.session_state, {"selected_reform": reform_params}
        )

    # Add Notes section at the bottom
    st.markdown("---")  # Add a horizontal line for visual separation

with st.expander("Notes"):
    st.markdown(
        """
    - All children are assumed to be 10 years old
    - The calculator uses tax year 2026 for all calculations excluding budget window estimates
    - Baseline deficit values are based on the Congressional Budget Office's 10-Year Budget Projections
    """
    )
