import streamlit as st
from personal_calculator.situation import create_situation
from personal_calculator.calculator import calculate_impacts
from personal_calculator.inputs import create_personal_inputs
from personal_calculator.chart import (
    create_reform_comparison_graph,
    initialize_results_tracking,
    update_results,
    reset_results,
)
import numpy as np
from nationwide_impacts.impacts import (
    NationwideImpacts,
    get_reform_name,
    calculate_total_revenue_impact,
)
from nationwide_impacts.charts import ImpactCharts
from nationwide_impacts.tables import display_summary_metrics
import pandas as pd
from baseline_impacts import display_baseline_impacts
from policy_config import display_policy_config
from personal_calculator.reforms import get_reform_params_from_config
from nationwide_impacts.charts import ImpactCharts
from personal_calculator.subsidy_rate import calculate_marginal_subsidy_rate
from constants import CURRENT_POLICY_PARAMS
from introduction import display_introduction
import plotly.express as px
from policyengine_core.charts import format_fig


# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator")

# Title
st.title("What's the SALTernative?")
st.markdown(
    """
    _The state and local tax (SALT) deduction and alternative minimum tax (AMT) will change next year. We'll walk you through these policies and model your custom reform._\n
    This tool starts by describing SALT and AMT, both under _current law_ (given the expiration of the Tax Cuts and Jobs Act in 2026) and under current policy (if the TCJA were extended). Then we'll explain these policies in the context of a sample filer. Finally, we'll put you in the driver's seat--you can design and simulate a range of SALT and AMT reforms, and we'll calculate how it affects the US and your household. Let's dive in!
    """
)

display_introduction()

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

# Move the baseline radio here
baseline = st.radio(
    "Baseline Scenario",
    ["Current Law", "Current Policy"],
    help="Choose whether to compare against Current Law or Current Policy (TCJA Extended)",
    horizontal=True,
)
st.session_state.baseline = baseline

# Create tabs after the baseline selection
nationwide_tab, calculator_tab = st.tabs(["US", "Household"])

with nationwide_tab:
    # Behavioral responses checkbox remains in tab
    behavioral_responses = st.checkbox(
        "Include behavioral responses",
        help="When selected, simulations adjust earnings based on how reforms affect net income and marginal tax rates, applying the Congressional Budget Office's assumptions. [Learn more](https://policyengine.org/us/research/us-behavioral-responses).",
    )

    # Store behavioral response in session state
    st.session_state.policy_config["behavioral_responses"] = behavioral_responses

    # Show budget window impacts with full width
    budget_window_impacts = []
    for year in range(2026, 2036):
        reform_name_with_year = get_reform_name(
            st.session_state.policy_config,
            st.session_state.baseline,
            year=year,
        )
        impact = st.session_state.nationwide_impacts.get_reform_impact(
            reform_name_with_year, impact_type="budget_window"
        )
        if impact is not None:
            budget_window_impacts.append(impact)
        else:
            st.warning(
                f"No data found for year {year} and reform: {reform_name_with_year}"
            )

    if budget_window_impacts:
        budget_window_impacts_df = pd.concat(budget_window_impacts, ignore_index=True)
        total_revenue_impact = calculate_total_revenue_impact(
            budget_window_impacts_df,
            st.session_state.policy_config,
            st.session_state.baseline,
        )
        if total_revenue_impact == 0:
            st.markdown("### Revise your policy to see an impact")
        else:
            st.markdown(
                f"### Your policy would {'reduce' if total_revenue_impact > 0 else 'increase'} the deficit by ${abs(total_revenue_impact)/1e12:.2f} trillion over the 10-Year Budget window."
            )
            # Create an expander for the 10-year impact graph
            with st.expander("Show 10-Year Impact Graph"):
                # Show the 10-year impact graph without the title
                fig = px.line(
                    budget_window_impacts_df,
                    x="year",
                    y="total_income_change",
                    labels={
                        "year": "Year",
                        "total_income_change": "Budgetary Impact (in billions)",
                    },
                )
                fig = format_fig(fig)
                st.plotly_chart(fig, use_container_width=False)
    else:
        st.warning("No budget window impacts found for the selected reform.")

    if not hasattr(st.session_state, "nationwide_impacts"):
        st.error("No impact data available. Please check data files.")
    else:
        # Construct reform name
        reform_name = get_reform_name(
            st.session_state.policy_config, st.session_state.baseline
        )

        # Get impact data for the selected reform
        impacts_data = st.session_state.nationwide_impacts.single_year_impacts
        reform_impacts = impacts_data[impacts_data["reform"] == reform_name]

        if reform_impacts.empty:
            st.warning(f"No data available for reform: {reform_name}")
        else:
            if total_revenue_impact == 0:
                st.markdown("")
            else:
                # Display summary metrics
                filtered_impacts = display_summary_metrics(
                    reform_impacts, st.session_state.baseline
                )

                # Show single-year impacts
                single_year_impact = (
                    st.session_state.nationwide_impacts.get_reform_impact(
                        reform_name, impact_type="single_year"
                    )
                )
                if single_year_impact is not None:
                    # Show the single-year impact graph
                    dist_data = (
                        st.session_state.nationwide_impacts.get_income_distribution(
                            reform_name
                        )
                    )
                    if dist_data is not None:
                        with st.expander("Show Distributional Analysis"):
                            fig = ImpactCharts.plot_distributional_analysis(dist_data)
                            st.plotly_chart(format_fig(fig), use_container_width=False)
                else:
                    st.error(
                        "No single-year impact data available for this combination."
                    )

    # Add Notes section
    st.markdown("---")

# Then display calculator tab
with calculator_tab:
    st.markdown(
        """
    This calculator shows the household-level impacts in 2026 of your policy configuration. 
    Input your household characteristics below.
    """
    )

    # Remove the outer columns and let create_personal_inputs handle its own columns
    personal_inputs = create_personal_inputs()

    # Initialize results tracking in session state if not exists
    if "results_df" not in st.session_state:
        st.session_state.results_df, st.session_state.summary_results = (
            initialize_results_tracking()
        )

    # Create columns for calculate button alignment
    calc_col1, calc_col2 = st.columns([1, 6])
    with calc_col1:
        calculate_clicked = st.button("Calculate Impacts")

    if calculate_clicked:
        # Reset results to start fresh
        reset_results()

        # Create situation based on inputs
        situation = create_situation(
            state_code=personal_inputs["state_code"],
            employment_income=personal_inputs["employment_income"],
            spouse_income=personal_inputs["spouse_income"],
            is_married=personal_inputs["is_married"],
            num_children=personal_inputs["num_children"],
            child_ages=personal_inputs["child_ages"],
            qualified_dividend_income=personal_inputs["qualified_dividend_income"],
            long_term_capital_gains=personal_inputs["long_term_capital_gains"],
            short_term_capital_gains=personal_inputs["short_term_capital_gains"],
            real_estate_taxes=personal_inputs["real_estate_taxes"],
            deductible_mortgage_interest=personal_inputs[
                "deductible_mortgage_interest"
            ],
            charitable_cash_donations=personal_inputs["charitable_cash_donations"],
        )

        # Display results in a nice format
        st.markdown("### Results")

        # Create placeholder for chart and status message
        chart_placeholder = st.empty()
        status_placeholder = st.empty()

        # Get selected baseline from session state
        baseline_scenario = st.session_state.baseline

        # Calculate baseline first
        status_placeholder.info(
            f"Calculating your 2026 net income under {baseline_scenario}..."
        )
        baseline_results = calculate_impacts(situation, {}, baseline_scenario)
        baseline_income = baseline_results["baseline"]

        # Calculate your policy configuration against baseline
        status_placeholder.info(
            "Calculating your 2026 net income under your policy configuration..."
        )
        reform_params = get_reform_params_from_config(st.session_state.policy_config)
        reform_results = calculate_impacts(
            situation, {"selected_reform": reform_params}, baseline_scenario
        )
        impact_key = "selected_reform_impact"
        reform_income = reform_results[impact_key] + baseline_income

        # Update results with baseline and reform
        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            baseline_scenario,
            baseline_income,
        )

        st.session_state.results_df, st.session_state.summary_results = update_results(
            st.session_state.results_df,
            st.session_state.summary_results,
            "Your Policy",
            reform_income,
        )

        # Display chart first
        fig = create_reform_comparison_graph(
            st.session_state.summary_results, baseline_scenario
        )
        chart_placeholder.plotly_chart(fig, use_container_width=False)

        # Then calculate and display subsidy rates
        status_placeholder.info("Calculating your 2026 property tax subsidy rates...")
        st.session_state.subsidy_rates = calculate_marginal_subsidy_rate(
            situation, {"selected_reform": reform_params}, baseline_scenario
        )

        # Display subsidy rates after chart
        st.markdown(
            f"""
            ### Under {baseline_scenario}, your property tax subsidy rate is {st.session_state.subsidy_rates['baseline']:.1f}%.
            
            ### Under your policy configuration, your property tax subsidy rate is {st.session_state.subsidy_rates['reform']:.1f}%.
            """
        )

        # Clear status message when complete
        status_placeholder.empty()

    # Add Notes section at the bottom
    st.markdown("---")  # Add a horizontal line for visual separation

with st.expander("Notes"):
    st.markdown(
        """
    - The calculator uses tax year 2026 for all calculations excluding budget window estimates
    - Baseline deficit values are based on the Congressional Budget Office's 10-Year Budget Projections
    - The marginal subsidy rate is computed in $500 increments of property taxes
    - We limit the computation to the federal budgetary impact due to:
      - States with AMT parameters tied to federal AMT (e.g., California)
      - States with deductions for federal tax liability (e.g., Oregon)
      - Behavioral responses
    """
    )
