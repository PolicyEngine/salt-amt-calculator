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
from nationwide_impacts.tables import ImpactTables
import pandas as pd

# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator", layout="wide")

# Title 
st.title("SALT and AMT Reform Impact Calculator")

# Create tabs
calculator_tab, nationwide_tab = st.tabs(["Household Calculator", "Nationwide Impacts"])

with calculator_tab:
    st.markdown(
        """
    This calculator compares different SALT and AMT reform scenarios against Current Law (pre-TCJA provisions) and Current Policy (2026 provisions). 
    Input your household characteristics and the parameters for each reform below.
    """
    )

    # Get personal inputs
    personal_inputs = create_personal_inputs()

    # Policy Parameters Section
    st.markdown("### Policy Parameters")
    st.markdown(
        "Compare up to three policy reforms to current law as well as current policy"
    )

    # Initialize session state for tracking reforms if it doesn't exist
    if "reform_indexes" not in st.session_state:
        st.session_state.reform_indexes = [0]  # Start with 1 custom reform

    # Initialize reform names if they don't exist
    if "reform_names" not in st.session_state:
        st.session_state.reform_names = {
            idx: f"Reform {idx+1}" for idx in st.session_state.reform_indexes
        }

    # Create columns for reforms based on current number of reforms
    num_reforms = len(st.session_state.reform_indexes)
    num_columns = num_reforms + (
        1 if num_reforms < 3 else 0
    )  # Add extra column only if under limit
    reform_cols = st.columns(num_columns)
    reform_params_dict = {}

    # Create inputs for each reform in columns
    for i, (col, reform_idx) in enumerate(
        zip(
            reform_cols[: len(st.session_state.reform_indexes)],
            st.session_state.reform_indexes,
        )
    ):
        with col:
            # Create a single row for name and remove button
            cols = st.columns([6, 1])
            with cols[0]:
                new_name = st.text_input(
                    "Reform Name",
                    value=st.session_state.reform_names[reform_idx],
                    key=f"name_{reform_idx}",
                    label_visibility="collapsed",
                )
                st.session_state.reform_names[reform_idx] = new_name

            with cols[1]:
                # Allow removing the last reform even if it's the only one
                if len(st.session_state.reform_indexes) > 0:
                    # Ensure unique key for remove button
                    remove_key = f"remove_reform_{reform_idx}_{i}"
                    if st.button("✕", key=remove_key, help="Remove this reform"):
                        st.session_state.reform_indexes.remove(reform_idx)
                        reform_name = st.session_state.reform_names[reform_idx]
                        del st.session_state.reform_names[reform_idx]
                        st.rerun()

            # Create reform parameters using the imported function
            reform_params_dict[f"reform_{i+1}"] = create_policy_inputs(new_name)

    # Add Reform button only if under the limit and either there are no reforms or we have an extra column
    if num_reforms < 3:  # Limit to 3 reforms
        # If there are no reforms, create a single column for the Add Reform button
        if num_reforms == 0:
            if st.button("Add Reform", key="add_reform", use_container_width=True):
                next_index = (
                    max(st.session_state.reform_indexes) + 1
                    if st.session_state.reform_indexes
                    else 0
                )
                st.session_state.reform_indexes.append(next_index)
                st.session_state.reform_names[next_index] = f"Reform {next_index+1}"
                st.rerun()
        else:
            # Use the last column if we have reforms
            with reform_cols[-1]:
                # Create empty space equivalent to the header space in other columns
                st.write("")  # Space where reform name would be

                # Create three columns within the column to center the button
                left_spacer, button_col, right_spacer = st.columns([1.5, 1, 1.5])

                with button_col:
                    if st.button("Add Reform", key="add_reform"):
                        next_index = (
                            max(st.session_state.reform_indexes) + 1
                            if st.session_state.reform_indexes
                            else 0
                        )
                        st.session_state.reform_indexes.append(next_index)
                        st.session_state.reform_names[next_index] = f"Reform {next_index+1}"
                        st.rerun()

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
            filing_status=personal_inputs["filing_status"],
            employment_income=personal_inputs["employment_income"],
            spouse_income=personal_inputs["spouse_income"],
            head_age=personal_inputs["head_age"],
            is_married=personal_inputs["is_married"],
            spouse_age=personal_inputs["spouse_age"],
            num_children=personal_inputs["num_children"],
            child_ages=personal_inputs["child_ages"],
            state_and_local_sales_or_income_tax=personal_inputs[
                "state_and_local_sales_or_income_tax"
            ],
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
                # Add the new SALT phase-out parameters
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

        # Update chart with both current law and policy
        fig = create_reform_comparison_graph(st.session_state.summary_results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Calculate the number of columns needed (Current Law, Current Policy, and reforms)
        num_cols = len(st.session_state.reform_indexes) + 2  # +2 for Current Law and Policy
        cols = st.columns(num_cols)

        # Display current law details
        with cols[0]:
            st.markdown("#### Current Law")
            st.markdown(f"Household income: **${round(current_law_income):,}**")

        # Display current policy details
        with cols[1]:
            st.markdown("#### Current Policy")
            st.markdown(f"Household income: **${round(current_policy_income):,}**")
            current_policy_impact = current_policy_income - current_law_income
            st.markdown(f"Change from Current Law: **${round(current_policy_impact):,}**")

        # Calculate and display each reform sequentially (if any exist)
        if st.session_state.reform_indexes:
            for i, reform_idx in enumerate(st.session_state.reform_indexes):
                reform_name = st.session_state.reform_names[reform_idx]
                status_placeholder.info(f"Calculating {reform_name}...")

                # Calculate single reform
                reform_results = calculate_impacts(
                    situation, {f"reform_{i+1}": reform_params_dict[f"reform_{i+1}"]}
                )
                reform_impact = reform_results[f"reform_{i+1}_impact"]
                new_income = current_law_income + reform_impact

                # Update results tracking
                st.session_state.results_df, st.session_state.summary_results = (
                    update_results(
                        st.session_state.results_df,
                        st.session_state.summary_results,
                        reform_name,
                        new_income,
                    )
                )

                # Update chart after each reform
                fig = create_reform_comparison_graph(st.session_state.summary_results)
                chart_placeholder.plotly_chart(fig, use_container_width=True)

                # Display detailed results for this reform
                with cols[
                    i + 2
                ]:  # +2 because indexes 0 and 1 are used for Current Law and Policy
                    st.markdown(f"#### {reform_name}")
                    st.markdown(f"New household income: **${round(new_income):,}**")
                    st.markdown(f"Change from Current Law: **${round(reform_impact):,}**")

        # Clear status message when complete
        status_placeholder.empty()

        # Create summary table
        create_summary_table(current_law_income, st.session_state, reform_params_dict)

    # Add Notes section at the bottom
    st.markdown("---")  # Add a horizontal line for visual separation
    with st.expander("Notes"):
        st.markdown(
            """
        - For calculation purposes, all children are assumed to be 10 years old
        - The calculator uses tax year 2026 for all calculations
        - Current Policy represents the tax provisions that will be in effect for 2026 under current law
        - Current Law represents the tax provisions that were in effect before the Tax Cuts and Jobs Act
        """
        )

with nationwide_tab:
    st.markdown("### Nationwide Policy Impacts")
    
    # Initialize nationwide impacts
    if 'nationwide_impacts' not in st.session_state:
        with st.spinner("Loading impact data..."):
            st.session_state.nationwide_impacts = NationwideImpacts()
    
    # Reform selection
    reform_options = st.session_state.nationwide_impacts.get_available_reforms()
    if not reform_options:
        st.error("No impact data available. Please check data files.")
    else:
        # Create two columns for selections
        col1, col2 = st.columns(2)
        with col1:
            selected_reform = st.selectbox(
                "Select Reform", 
                reform_options,
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with col2:
            impact_type = st.radio(
                "Select Impact Period",
                ["single_year", "budget_window"],
                format_func=lambda x: "2026 Impact" if x == "single_year" else "10-Year Impact",
                horizontal=True
            )
        
        # Get impact data
        impact_data = st.session_state.nationwide_impacts.get_reform_impact(
            selected_reform, 
            impact_type
        )
        
        if impact_data is not None:
            # Display summary metrics
            ImpactTables.display_summary_metrics(impact_data, impact_type)
            
            # Create tabs for different views
            dist_tab, time_tab = st.tabs([
                "Distributional Analysis", 
                "Time Series"
            ])
            
            with dist_tab:
                if impact_type == "single_year":
                    # Get and plot income distribution data
                    dist_data = st.session_state.nationwide_impacts.get_income_distribution(selected_reform)
                    if dist_data is not None:
                        fig = ImpactCharts.plot_distributional_analysis(dist_data)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Distributional analysis only available for single year impacts")
                
            with time_tab:
                if impact_type == "budget_window":
                    # Get and plot time series data
                    time_data = st.session_state.nationwide_impacts.get_time_series(selected_reform)
                    if time_data is not None:
                        fig = ImpactCharts.plot_time_series(time_data)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Time series only available for budget window analysis")
        else:
            st.error("No impact data available for selected reform.")
            
    # Add Notes section
    st.markdown("---")
    with st.expander("Notes and Methodology"):
        st.markdown(
            """
            - All monetary values are in 2026 dollars
            - Income groups are defined by total household income
            - Budget window estimates account for behavioral responses
            """
        )