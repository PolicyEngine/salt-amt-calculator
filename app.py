import streamlit as st
from personal_calculator.situation import create_situation
from personal_calculator.calculator import calculate_impacts
from personal_calculator.inputs import create_personal_inputs
from personal_calculator.reforms import get_reform_params_from_config
from personal_calculator.chart import (
    create_reform_comparison_graph,
    initialize_results_tracking,
    update_results,
    reset_results,
)

import pandas as pd
import plotly.express as px
from policyengine_core.charts import format_fig

from nationwide_impacts.impacts import (
    NationwideImpacts,
    get_reform_name,
    calculate_total_revenue_impact,
)
from nationwide_impacts.tables import display_summary_metrics
from nationwide_impacts.charts import ImpactCharts

from baseline_impacts import display_baseline_impacts
from policy_config import display_policy_config
from constants import BLUE

from introduction import (
    display_salt_cap_comparison_chart,
    display_notes,
    display_effective_salt_cap_graph,
    display_effective_salt_cap
    
)

# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator")


# Inject custom CSS with Roboto font and styling
st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');
        
        /* ===== FONT STYLING ===== */
        /* Apply Roboto font to all elements */
        html, body, [class*="css"], .stMarkdown, .stButton, .stHeader, 
        div, p, h1, h2, h3, h4, h5, h6, span,
        .stRadio > label, .stCheckbox > label, .stExpander > label,
        .stMarkdown p, .stMarkdown span, .stMarkdown div {{
            font-family: 'Roboto', sans-serif !important;
        }}
        
        /* ===== LAYOUT STYLING ===== */
        /* Style improvements */
        .main .block-container {{
            padding-top: 2rem;
        }}
        
        /* Hide Streamlit branding */
        div[data-testid="stToolbar"] {{
            visibility: hidden;
        }}
        
        footer {{
            visibility: hidden;
        }}
        
        /* ===== BUTTON STYLING ===== */
        /* Style all buttons with teal accent - no hover effect */
        .stButton > button {{
            background-color: {BLUE} !important;
            color: white !important;
            border: none !important;
            transition: none !important;
        }}
        
        /* Disable hover effects */
        .stButton > button:hover {{
            background-color: {BLUE} !important;
            color: white !important;
            border: none !important;
        }}
        
        /* Active state for buttons */
        .stButton > button:active {{
            background-color: {BLUE} !important;
            color: white !important;
        }}
        
        /* ===== FORM ELEMENTS STYLING ===== */
        /* Default styling for form elements - no outline */
        .stSelectbox > div > div,
        .stNumberInput > div > div > div,
        .stTextInput > div > div > input {{
            border-color: #cccccc !important;
            transition: border-color 0.2s;
        }}
        
        /* Radio and checkbox default styling */
        .stRadio > div[role="radiogroup"] > label > div:first-child,
        .stCheckbox > div > label > div:first-child {{
            color: #cccccc !important;
            background-color: #f0f0f0 !important;
            border-color: #cccccc !important;
            transition: all 0.2s;
        }}
        
        /* Hover states for all form elements - show teal outline */
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div > div:hover,
        .stTextInput > div > div > input:hover,
        .stRadio > div[role="radiogroup"] > label:hover > div:first-child,
        .stCheckbox > div > label:hover > div:first-child {{
            border-color: {BLUE} !important;
        }}
        
        /* Focus states - also show teal outline and shadow */
        .stSelectbox > div > div:focus-within,
        .stNumberInput > div > div > div:focus-within,
        .stTextInput > div > div > input:focus,
        .stRadio > div[role="radiogroup"] > label > div:first-child:focus,
        .stRadio > div[role="radiogroup"] > label > div:first-child:focus-within,
        .stCheckbox > div > label > div:first-child:focus,
        .stCheckbox > div > label > div:first-child:focus-within {{
            border-color: {BLUE} !important;
            box-shadow: 0 0 0 2px rgba(73, 190, 183, 0.2) !important;
        }}
        
        /* Adjusts the color of the radio button */
        .stRadio > div[role="radiogroup"] > label > div:first-child > div,
        .stCheckbox > div > label > div:first-child > div {{
            background-color: {BLUE} !important;
        }}
        
        /* Style the outside border of selected radio buttons */
        .stRadio > div[role="radiogroup"] > label > div:second-child {{
            border-color: black !important;
        }}
        
        /* Keep text color black in selectbox and radio buttons */
        .stSelectbox, .stMultiSelect, .stRadio {{
            color: white !important;
        }}
        
        
        /* Selectbox arrow color only */
        .stSelectbox > div > div > div:last-child {{
            color: {BLUE} !important;
        }}

        
        
        /* ===== TAB STYLING ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0 0;
            padding-top: 10px;
            padding-bottom: 10px;
            color: black;
            background-color: white;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: white !important;
            color: {BLUE} !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: {BLUE} !important;
            height: 3px !important; /* You can adjust thickness if needed */
        }}
        
        /* ===== EXPANDER STYLING ===== */
        /* Expander styling */
        .streamlit-expanderHeader:hover, 
        [data-testid="stExpander"] > div:first-child:hover {{
            color: {BLUE} !important;
        }}

        /* Style for expander icon on hover */
        .streamlit-expanderHeader:hover svg, 
        [data-testid="stExpander"] > div:first-child:hover svg {{
            fill: {BLUE} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize navigation in session state if not already present
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Introduction"

# Set up sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    section = st.radio("Select Input Section", ["Personal Inputs", "Policy Inputs"])
    if section == "Personal Inputs":
        personal_inputs = create_personal_inputs()
        # Add calculate button in the sidebar
        calculate_clicked = st.button("Calculate Impacts", type="primary")
        if calculate_clicked:
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

            # Store calculation results in session state for display in the main area
            st.session_state.calculation_performed = True
    elif section == "Policy Inputs":
        display_policy_config()

    page = st.radio(
        "Go to",
        [
            "Introduction",
            "Case Studies",
            "Policy Configuration",
            "Calculator",
        ],
        key="sidebar_nav",
        index=[
            "Introduction",
            "Case Studies",
            "Policy Configuration",
            "Calculator",
        ].index(st.session_state.nav_page),
    )

    # Update nav_page when sidebar selection changes
    if page != st.session_state.nav_page:
        st.session_state.nav_page = page

    st.markdown("---")
    st.markdown(
        """
    _This tool is designed to help you understand and model SALT and AMT policy changes_
    """
    )

# Initialize nationwide impacts if not already done
if "nationwide_impacts" not in st.session_state:
    try:
        st.session_state.nationwide_impacts = NationwideImpacts()
    except Exception as e:
        st.error(f"Error loading nationwide impacts data: {str(e)}")

# Display selected section based on sidebar navigation
if page == "Introduction":
    # Show the introduction and basics, without the case studies
    # Custom styled title with teal accents
    st.markdown(
        f"""
        <h1 style="font-family: Roboto;">
            <span style="color:; font-weight: bold;">What's the SALT</span><span style="color: ; font-weight: normal;">ernative?</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.image("images/cover.png")

    st.markdown(
        """
        _The state and local tax (SALT) deduction and alternative minimum tax (AMT) are scheduled to change next year. We'll walk you through these policies and allow you to model your custom reform._\n
        This tool starts by describing the SALT deduction and AMT, both under _current law_ (given the expiration of the Tax Cuts and Jobs Act (TCJA) in 2026) and under _current policy_ (if the TCJA was extended beyond 2025). Then we'll explain these policies in the context of sample households. Finally, we'll put you in the driver's seat - you can design and simulate a range of SALT and AMT reforms, and we'll calculate how it affects the US and your household. Let's dive in!
        """
    )


    # Add a button to go to the next section
    st.markdown("---")
    if st.button("Go to Case Studies →", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Case Studies"
        st.rerun()

elif page == "Case Studies":
    # Only show the case studies part
    st.markdown(
        f"""
    <h2 style="font-family: Roboto; color:;">How SALT and AMT Affect Sample Households</h2>
        
    **Please select a state and income level to see how SALT and AMT affect a sample household.**
    """,
        unsafe_allow_html=True,
    )
    if calculate_clicked:
        display_salt_cap_comparison_chart(
        state_code=personal_inputs["state_code"],
        is_married=personal_inputs["is_married"],
        num_children=personal_inputs["num_children"],
        child_ages=personal_inputs["child_ages"],
        qualified_dividend_income=personal_inputs["qualified_dividend_income"],
        long_term_capital_gains=personal_inputs["long_term_capital_gains"],
        short_term_capital_gains=personal_inputs["short_term_capital_gains"],
        deductible_mortgage_interest=personal_inputs["deductible_mortgage_interest"],
        charitable_cash_donations=personal_inputs["charitable_cash_donations"]
    )
    else:
        st.markdown("---")
    # Add a button to go to the next section
    st.markdown("---")
    if st.button("Go to Policy Configuration →", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Policy Configuration"
        st.rerun()

elif page == "Policy Configuration":
    # Display baseline impacts section first
    display_baseline_impacts()

    # Add a button to go to the next section
    st.markdown("---")
    if st.button("Go to Calculator →", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Calculator"
        st.rerun()

elif page == "Calculator":
    # Create the Calculator section
    st.markdown(
        f"""
    <h2 style="font-family: Roboto;">Calculator</h2>
    """,
        unsafe_allow_html=True,
    )

    # First ensure policy config exists
    if "policy_config" not in st.session_state:
        # Initialize default policy config
        st.session_state.policy_config = display_policy_config()
    else:
        # Just use existing policy config
        policy_config = st.session_state.policy_config

    # Baseline selection
    baseline = st.radio(
        "Baseline Scenario",
        ["Current Law", "Current Policy"],
        help="Choose whether to compare against Current Law or Current Policy (TCJA Extended)",
        horizontal=True,
    )
    st.session_state.baseline = baseline

    # Create tabs for US and Household impacts
    nationwide_tab, calculator_tab = st.tabs(["US", "Household"])

    # US nationwide impact tab content
    with nationwide_tab:
        # Behavioral responses checkbox
        behavioral_responses = st.checkbox(
            "Include behavioral responses",
            help="When selected, simulations adjust earnings based on how reforms affect net income and marginal tax rates, applying the Congressional Budget Office's assumptions. [Learn more](https://policyengine.org/us/research/us-behavioral-responses).",
            disabled=st.session_state.policy_config.get("salt_cap") == "$100k",
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
            budget_window_impacts_df = pd.concat(
                budget_window_impacts, ignore_index=True
            )
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
                        <h3 style="color: #777777; font-family: Roboto;">Your policy would {impact_word} the deficit by <span style="color: {BLUE}; font-weight: bold;">${impact_amount:.2f} trillion</span> over the 10-Year Budget window</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                # Create an expander for the 10-year impact graph
                with st.expander("Show 10-Year Impact Graph"):
                    st.markdown(
                        "**Figure 4: Budgetary Impact Over the 10-Year Window**"
                    )

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
                                    "**Figure 5: Average Household Net Income Change by Income Decile**"
                                )

                                fig = ImpactCharts.plot_distributional_analysis(
                                    dist_data
                                )
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

    # Household calculator tab content
    with calculator_tab:
        st.markdown(
            """
        This calculator shows the household-level impacts in 2026 of your policy configuration. 
        Input your household characteristics below.
        """
        )

        # Remove the outer columns and let create_personal_inputs handle its own columns

        # Initialize results tracking in session state if not exists
        if "results_df" not in st.session_state:
            st.session_state.results_df, st.session_state.summary_results = (
                initialize_results_tracking()
            )

        # Create columns for calculate button alignment
        calc_col1, calc_col2 = st.columns([1, 6])
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
            st.markdown(
                f"""
            <h3 style="font-family: Roboto; color: {BLUE};">Results</h3>
            """,
                unsafe_allow_html=True,
            )

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
            reform_params = get_reform_params_from_config(
                st.session_state.policy_config
            )
            reform_results = calculate_impacts(
                situation, {"selected_reform": reform_params}, baseline_scenario
            )
            impact_key = "selected_reform_impact"
            reform_income = reform_results[impact_key] + baseline_income

            # Update results with baseline and reform
            st.session_state.results_df, st.session_state.summary_results = (
                update_results(
                    st.session_state.results_df,
                    st.session_state.summary_results,
                    baseline_scenario,
                    baseline_income,
                )
            )

            st.session_state.results_df, st.session_state.summary_results = (
                update_results(
                    st.session_state.results_df,
                    st.session_state.summary_results,
                    "Your Policy",
                    reform_income,
                )
            )

            # Display chart first
            fig = create_reform_comparison_graph(
                st.session_state.summary_results, baseline_scenario
            )
            chart_placeholder.plotly_chart(fig, use_container_width=False)

            # Calculate and display effective SALT caps
            status_placeholder.info("Calculating your effective SALT cap...")

            # Calculate effective SALT cap for current law/baseline
            baseline_cap = display_effective_salt_cap(
                state_code=personal_inputs["state_code"],
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
                employment_income=personal_inputs["employment_income"],
                policy=baseline_scenario,
                reform_params=reform_params,
                threshold=0.1,
            )

            # Calculate effective SALT cap for reform/current policy
            reform_cap = display_effective_salt_cap(
                state_code=personal_inputs["state_code"],
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
                employment_income=personal_inputs["employment_income"],
                policy="Reform",  # Or use the appropriate policy name for your reform
                reform_params=reform_params,  # Pass the reform parameters
                threshold=0.1,
            )

            # Display effective SALT cap graph for reform scenario
            display_effective_salt_cap_graph(
                state_code=personal_inputs["state_code"],
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
                policy="Reform",
                reform_params=reform_params,
                threshold=0.1,
            )

            # You can still display a combined message if needed
            caps = {"current_law": baseline_cap, "current_policy": reform_cap}

            # Clear status message when complete
            status_placeholder.empty()

# Add Notes section at the app level after any sections are displayed
if page in ["Case Studies", "Policy Configuration", "Calculator"]:
    display_notes()

# Add a button to restart the navigation cycle for the Calculator section
if page == "Calculator":
    st.markdown("---")
    if st.button("Back to Introduction →", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Introduction"
        st.rerun()
