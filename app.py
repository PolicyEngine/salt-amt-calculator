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
from constants import CURRENT_POLICY_PARAMS, TEAL_ACCENT, TEAL_LIGHT
from introduction import display_introduction
import plotly.express as px
from policyengine_core.charts import format_fig
from personal_calculator.salt_cap_calculator import find_effective_salt_cap
from personal_calculator.salt_cap_calculator import create_situation_with_axes
import os


def load_custom_css():
    """Load custom CSS to apply styling to inputs"""
    css_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".streamlit", "custom.css"
    )
    with open(css_file, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator")

# Load custom CSS for form styling
load_custom_css()

# Inject additional CSS directly to handle radio buttons and primary buttons
st.markdown(
    """
<style>
    /* Override radio button colors */
    div[role="radiogroup"] label[data-baseweb="radio"] input:checked + div {
        border-color: #39C6C0 !important;
    }
    
    div[role="radiogroup"] label[data-baseweb="radio"] input:checked + div div {
        background-color: #39C6C0 !important;
    }
    
    /* Override primary button color */
    button[kind="primary"] {
        background-color: #39C6C0 !important;
        border-color: #39C6C0 !important;
    }
    
    /* Target buttons by Streamlit's generated classes */
    button.stButton button {
        background-color: #39C6C0 !important;
        border-color: #39C6C0 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Title
st.title("What's the SALTernative?")
st.markdown(
    """
    _The state and local tax (SALT) deduction and alternative minimum tax (AMT) are scheduled to change next year. We'll walk you through these policies and allow you to model your custom reform._\n
    This tool starts by describing the SALT deduction and AMT, both under _current law_ (given the expiration of the Tax Cuts and Jobs Act (TCJA) in 2026) and under _current policy_ (if the TCJA was extended beyond 2025). Then we'll explain these policies in the context of sample households. Finally, we'll put you in the driver's seat - you can design and simulate a range of SALT and AMT reforms, and we'll calculate how it affects the US and your household. Let's dive in!
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
            impact_word = "reduce" if total_revenue_impact > 0 else "increase"
            impact_amount = abs(total_revenue_impact) / 1e12

            st.markdown(
                f"""
                <div style="text-align: center; margin: 25px 0;">
                    <h3 style="color: #777777;">Your policy would {impact_word} the deficit by <span style="color: {TEAL_ACCENT}; font-weight: bold;">${impact_amount:.2f} trillion</span> over the 10-Year Budget window</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Create an expander for the 10-year impact graph
            with st.expander("Show 10-Year Impact Graph"):
                st.markdown("**Figure 2: Budgetary Impact Over the 10-Year Window**")

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
                # Add margin to ensure logo is visible
                fig.update_layout(
                    margin=dict(l=20, r=60, t=20, b=80),  # Increase bottom margin
                )
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
                        with st.expander(
                            "Show Average Household Net Income Change Chart"
                        ):
                            st.markdown(
                                "**Figure 3: Average Household Net Income Change by Income Decile**"
                            )

                            fig = ImpactCharts.plot_distributional_analysis(dist_data)
                            fig = format_fig(fig)
                            # Add margin to ensure logo is visible
                            fig.update_layout(
                                margin=dict(l=20, r=60, t=20, b=80),
                            )
                            st.plotly_chart(fig, use_container_width=False)
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
        calculate_clicked = st.button("Calculate Impacts", type="primary")

    if calculate_clicked:
        # Reset results to start fresh
        reset_results()

        # Create situation based on inputs
        situation = create_situation(
            state_code=personal_inputs["state_code"],
            employment_income=personal_inputs["employment_income"],
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

        # Calculate and display effective SALT caps
        status_placeholder.info("Calculating your effective SALT cap...")

        # Create situation with axes using the same inputs
        situation_with_axes = create_situation_with_axes(
            state_code=personal_inputs["state_code"],
            employment_income=personal_inputs["employment_income"],
            is_married=personal_inputs["is_married"],
            num_children=personal_inputs["num_children"],
            child_ages=personal_inputs["child_ages"],
            qualified_dividend_income=personal_inputs["qualified_dividend_income"],
            long_term_capital_gains=personal_inputs["long_term_capital_gains"],
            short_term_capital_gains=personal_inputs["short_term_capital_gains"],
            deductible_mortgage_interest=personal_inputs[
                "deductible_mortgage_interest"
            ],
            charitable_cash_donations=personal_inputs["charitable_cash_donations"],
        )

        # Calculate caps using the imported function
        caps = find_effective_salt_cap(
            situation_with_axes, {"selected_reform": reform_params}, baseline_scenario
        )

        # Format the effective SALT cap text with a cleaner, centered design
        if np.isinf(caps["baseline_salt_cap"]) and np.isinf(caps["reform_salt_cap"]):
            st.markdown(
                """
                <div style="text-align: center; margin: 25px 0;">
                    <h3 style="color: #777777;">Your household faces no effective SALT cap under either scenario</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif np.isinf(caps["baseline_salt_cap"]):
            st.markdown(
                f"""
                <div style="text-align: center; margin: 25px 0;">
                    <h3 style="color: #777777;">Your household faces no effective SALT cap under {baseline_scenario} but faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${caps['reform_salt_cap']:,.0f}</span> under your policy</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif np.isinf(caps["reform_salt_cap"]):
            st.markdown(
                f"""
                <div style="text-align: center; margin: 25px 0;">
                    <h3 style="color: #777777;">Your household faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${caps['baseline_salt_cap']:,.0f}</span> under {baseline_scenario} but faces no effective SALT cap under your policy</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="text-align: center; margin: 25px 0;">
                    <h3 style="color: #777777;">Your household faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${caps['baseline_salt_cap']:,.0f}</span> under {baseline_scenario} and <span style="color: {TEAL_ACCENT}; font-weight: bold;">${caps['reform_salt_cap']:,.0f}</span> under your policy</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Clear status message when complete
        status_placeholder.empty()

    # Add Notes section at the bottom
    st.markdown("---")  # Add a horizontal line for visual separation

with st.expander("Notes"):
    st.markdown(
        """
    - The calculator uses tax year 2026 for all calculations excluding budget window estimates
    - The marginal subsidy rate is computed in $500 increments of property taxes
    - We limit the computation to the federal budgetary impact due to:
      - States with AMT parameters tied to federal AMT (e.g., California)
      - States with deductions for federal tax liability (e.g., Oregon)
      - Behavioral responses
    
    **Documentation:**
    - [How we model SALT](https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview)
    - [How we model AMT](https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview)
    """
    )
