import streamlit as st
from personal_calculator.situation import create_situation
from personal_calculator.inputs import create_personal_inputs
from personal_calculator.chart import (
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

from policy_config import display_policy_config, initialize_policy_config_state
from constants import BLUE

from personal_calculator.charts.salt_amt_charts import (
    display_salt_deduction_comparison_chart,
    display_notes,
    display_effective_salt_cap,
    display_regular_tax_and_amt_chart,
    display_taxable_income_and_amti_chart,
    display_income_tax_chart,
    display_effective_salt_cap_graph,
    display_regular_tax_comparison_chart,
    display_amt_comparison_chart,
    display_gap_chart,
    display_marginal_rate_chart,
    display_regular_tax_and_amt_by_income_chart,
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

# Initialize chart index in session state if not already present
if "chart_index" not in st.session_state:
    st.session_state.chart_index = 0


def change_chart_without_rerun(direction):
    """Change the chart index without triggering a page rerun"""
    current_index = st.session_state.chart_index
    num_charts = len(available_charts)

    if direction == "next":
        st.session_state.chart_index = (current_index + 1) % num_charts
    elif direction == "prev":
        st.session_state.chart_index = (current_index - 1) % num_charts


# Set up sidebar for navigation
with st.sidebar:
    st.title("Inputs")
    section = st.radio("---", ["Personal Inputs", "Policy Inputs"])

    # Set policy config state to default values to prevent error
    # if user skips straight to budgetary impacts
    initialize_policy_config_state()

    if section == "Personal Inputs":

        # Get personal inputs (will use session state if available)
        personal_inputs = create_personal_inputs()

        # Store current inputs in session state
        if (
            "personal_inputs" not in st.session_state
            or personal_inputs != st.session_state.personal_inputs
        ):
            st.session_state.personal_inputs = personal_inputs

        inputs_changed = (
            "last_calculated_inputs" in st.session_state
            and st.session_state.personal_inputs
            != st.session_state.last_calculated_inputs
        )

        if inputs_changed:
            calculate_button_text = "Recalculate with New Inputs"
            button_help = (
                "Your inputs have changed. Click to update charts with new values."
            )
        else:
            calculate_button_text = "Calculate Impacts"
            button_help = "Calculate tax impacts based on your inputs."

        calculate_clicked = st.button(calculate_button_text, type="primary")

        if calculate_clicked:
            # Only set flag and recalculate if inputs changed
            inputs_changed = (
                "last_calculated_inputs" not in st.session_state
                or st.session_state.personal_inputs
                != st.session_state.last_calculated_inputs
            )

            if inputs_changed:
                st.session_state.calculate_clicked = True
                st.session_state.last_calculated_inputs = (
                    st.session_state.personal_inputs.copy()
                )

                # Reset results and recalculate
                reset_results()

                # Create situation based on inputs
                situation = create_situation(
                    employment_income=personal_inputs["employment_income"],
                    is_married=personal_inputs["is_married"],
                    num_children=personal_inputs["num_children"],
                    child_ages=personal_inputs["child_ages"],
                    qualified_dividend_income=personal_inputs[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=personal_inputs["long_term_capital_gains"],
                    short_term_capital_gains=personal_inputs[
                        "short_term_capital_gains"
                    ],
                    deductible_mortgage_interest=personal_inputs[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=personal_inputs[
                        "charitable_cash_donations"
                    ],
                )

                # Store calculation results in session state
                st.session_state.situation = situation
                st.session_state.calculation_performed = True

                # Reset chart index when recalculating
                st.session_state.chart_index = 0
    elif section == "Policy Inputs":
        display_policy_config()

    def update_nav_page(new_page):
        st.session_state.nav_page = new_page

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
if st.session_state.nav_page == "Introduction":
    # Show the introduction and basics, without the How SALT affects taxes
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
    if st.button("Go to The Effective SALT Cap", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "The Effective SALT Cap"
        st.rerun()

elif st.session_state.nav_page == "The Effective SALT Cap":
    # Only show the How SALT affects taxes part
    st.markdown(
        f"""
    <h2 style="font-family: Roboto; color:;">How SALT and AMT Affect Sample Households</h2>
        
    **Please select a state and income level to see how SALT and AMT affect a sample household.**
    """,
        unsafe_allow_html=True,
    )

    if "chart_index" not in st.session_state:
        st.session_state.chart_index = 0

    # Define the list of available charts
    available_charts = [
        "SALT Deduction Comparison",
        "Taxable Income and AMTI Comparison",
        "Regular Tax and AMT Comparison",
        "Income Tax Comparison",
        "Effective SALT Cap",
        # "Regular Tax and AMT Comparison",
        # "AMT Comparison",
        "Regular Tax and AMT Comparison by Income",
        "Gap Chart",
        "Marginal Tax Rate Chart",
        "Effective SALT Cap",
    ]

    inputs_changed = (
        "personal_inputs" in st.session_state
        and "last_calculated_inputs" in st.session_state
        and st.session_state.personal_inputs != st.session_state.last_calculated_inputs
    )

    calculation_is_valid = (
        "calculate_clicked" in st.session_state
        and st.session_state.calculate_clicked
        and not inputs_changed
    )

    # Check if the sidebar calculate button was clicked
    if calculation_is_valid:
        if "last_calculated_inputs" in st.session_state:
            inputs_to_use = st.session_state.last_calculated_inputs

            current_chart = available_charts[st.session_state.chart_index]

            # Display the current chart based on the chart_index
            if st.session_state.chart_index == 0:
                st.markdown("### Current policy creates an explicit SALT cap")
                display_salt_deduction_comparison_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    employment_income=inputs_to_use["employment_income"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
                st.markdown(
                    "### TCJA capped SALT at $10,000; prior law allowed deductions for all SALT"
                )
            elif st.session_state.chart_index == 1:
                st.markdown("### But AMT income does not vary with SALT")
                display_taxable_income_and_amti_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    employment_income=inputs_to_use["employment_income"],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
                st.markdown(
                    "### AMT income equals taxable income plus exemptions and deductions including SALT"
                )
            elif st.session_state.chart_index == 2:
                # Calculate effective SALT caps for both policies
                current_law_cap = display_effective_salt_cap(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    employment_income=inputs_to_use["employment_income"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                    policy="Current Law",
                )

                current_policy_cap = display_effective_salt_cap(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    employment_income=inputs_to_use["employment_income"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                    policy="Current Policy",
                )

                st.markdown(
                    f"### You face an effective SALT cap of <span style='color: {BLUE}'>{current_policy_cap}</span> under current policy and <span style='color: {BLUE}'>{current_law_cap}</span> under current law",
                    unsafe_allow_html=True,
                )
                display_regular_tax_and_amt_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    employment_income=inputs_to_use["employment_income"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
                st.markdown(
                    "### Additional SALT does not reduce your income tax if AMT exceeds regular tax"
                )
            elif st.session_state.chart_index == 3:
                st.markdown(
                    "### SALT could lower your taxes by up to $x under current law and $y under current policy"
                )
                display_income_tax_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    employment_income=inputs_to_use["employment_income"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
                st.markdown("### Filers pay the greater of regular tax and AMT")
            elif st.session_state.chart_index == 4:
                st.markdown("### Effective SALT Cap")
                display_effective_salt_cap_graph(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                    policy="Current Law",
                )
            # elif st.session_state.chart_index == 5:
            #     st.markdown("### Regular Tax and AMT Comparison")
            #     display_regular_tax_comparison_chart(
            #             is_married=inputs_to_use["is_married"],
            #             num_children=inputs_to_use["num_children"],
            #             child_ages=inputs_to_use["child_ages"],
            #             qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
            #             long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
            #             short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
            #             deductible_mortgage_interest=inputs_to_use["deductible_mortgage_interest"],
            #             charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            #         )
            # elif st.session_state.chart_index == 6:
            #     st.markdown("### AMT Comparison")
            #     display_amt_comparison_chart(
            #             is_married=inputs_to_use["is_married"],
            #             num_children=inputs_to_use["num_children"],
            #             child_ages=inputs_to_use["child_ages"],
            #             qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
            #             long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
            #             short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
            #             deductible_mortgage_interest=inputs_to_use["deductible_mortgage_interest"],
            #             charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            # )
            elif st.session_state.chart_index == 5:
                st.markdown("### Regular Tax and AMT Comparison by Income")
                display_regular_tax_and_amt_by_income_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
            elif st.session_state.chart_index == 6:
                st.markdown("### Gap Chart")
                display_gap_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
            elif st.session_state.chart_index == 7:
                st.markdown("### Marginal Tax Rate Chart")
                display_marginal_rate_chart(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                )
            elif st.session_state.chart_index == 8:
                st.markdown("### Effective SALT Cap")
                display_effective_salt_cap_graph(
                    is_married=inputs_to_use["is_married"],
                    num_children=inputs_to_use["num_children"],
                    child_ages=inputs_to_use["child_ages"],
                    qualified_dividend_income=inputs_to_use[
                        "qualified_dividend_income"
                    ],
                    long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                    short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                    deductible_mortgage_interest=inputs_to_use[
                        "deductible_mortgage_interest"
                    ],
                    charitable_cash_donations=inputs_to_use[
                        "charitable_cash_donations"
                    ],
                    policy="Current Law",
                )
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.button(
                    "← Previous",
                    key="prev_chart",
                    on_click=change_chart_without_rerun,
                    args=("prev",),
                )

            with col2:
                st.markdown(
                    f"**Chart {st.session_state.chart_index + 1} of {len(available_charts)}: {available_charts[st.session_state.chart_index]}**"
                )

            with col3:
                st.button(
                    "Next →",
                    key="next_chart",
                    on_click=change_chart_without_rerun,
                    args=("next",),
                )
        else:
            st.error("Calculation data is missing. Please recalculate impacts.")
    elif inputs_changed:
        # Show a message that inputs have changed and need recalculation
        st.info(
            "Your inputs have changed. Click 'Calculate Impacts' in the sidebar to generate new charts."
        )
    elif (
        "calculate_clicked" not in st.session_state
        or not st.session_state.calculate_clicked
    ):
        # No calculation has been performed yet
        st.info(
            "Please fill out your personal information in the sidebar and click 'Calculate Impacts' to see charts."
        )
    else:
        # Some other edge case
        st.warning("Please try recalculating your impacts from the sidebar.")

    # Add a button to go to the next section
    st.markdown("---")
    if st.button("Go to Budgetary and distributional impacts", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Budgetary and distributional impacts"
        st.rerun()

elif st.session_state.nav_page == "Budgetary and distributional impacts":
    # Create the Budgetary and distributional impacts section
    st.markdown(
        f"""
    <h2 style="font-family: Roboto;">Budgetary and distributional impacts</h2>
    """,
        unsafe_allow_html=True,
    )

    policy_config = st.session_state.policy_config

    # Baseline selection
    baseline = st.radio(
        "Baseline Scenario",
        ["Current Law", "Current Policy"],
        help="Choose whether to compare against Current Law or Current Policy (TCJA Extended)",
        horizontal=True,
    )
    st.session_state.baseline = baseline

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
                    <h3 style="color: #777777; font-family: Roboto;">Your policy would {impact_word} the deficit by <span style="color: {BLUE}; font-weight: bold;">${impact_amount:.2f} trillion</span> over the 10-Year Budget window</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Create an expander for the 10-year impact graph
            with st.expander("Show 10-Year Impact Graph"):
                st.markdown("**Figure 4: Budgetary Impact Over the 10-Year Window**")

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

# Add Notes section at the app level after any sections are displayed
if st.session_state.nav_page in [
    "Introduction",
    "The Effective SALT Cap",
    "Budgetary and distributional impacts",
]:
    display_notes()

# Add a button to restart the navigation cycle for the Budgetary and distributional impacts section
if st.session_state.nav_page == "Budgetary and distributional impacts":
    st.markdown("---")
    if st.button("Back to Introduction", type="primary"):
        # Set the page in session state and rerun to navigate
        st.session_state.nav_page = "Introduction"
        st.rerun()
