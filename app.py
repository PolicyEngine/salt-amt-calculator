import streamlit as st
from personal_calculator.inputs import create_personal_inputs
from personal_calculator.chart import (
    reset_results,
)
import pandas as pd
import plotly.express as px
from policyengine_core.charts import format_fig as format_fig_


def format_fig(fig):
    return format_fig_(fig).update_layout(
        margin_r=100,
    )


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
    display_regular_tax_and_amt_chart,
    display_taxable_income_and_amti_chart,
    display_income_tax_chart,
    display_effective_salt_cap_graph,
    display_gap_chart,
    display_marginal_rate_chart,
    display_regular_tax_and_amt_by_income_chart,
    display_tax_savings_chart,
    display_sales_or_income_tax_table,
)
from personal_calculator.dataframes.dataframes import (
    calculate_salt_income_tax_reduction,
    display_effective_salt_cap,
    calculate_df_without_axes,
)
from personal_calculator.dataframes.situations import create_situation_without_axes

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

        .stRadio > div[role="radiogroup"] > label > div:first-child, .stCheckbox > div > label > div:first-child {{
            background-color: #3378b2 !important;
        }}

        .stRadio > div[role="radiogroup"] > label > div:first-child > div, .stCheckbox > div > label > div:first-child > div {{
            border: 1px solid #3378b2 !important;
            background-color: white !important;
        }}
        
    </style>
    """,
    unsafe_allow_html=True,
)

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
    st.title("Inputs (2026):")
    section = st.radio(
        "Section Selection",
        ["Household", "Policy"],
        label_visibility="collapsed",
    )

    # Set policy config state to default values to prevent error
    # if user skips straight to budgetary impacts
    initialize_policy_config_state()

    if section == "Household":

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
            calculate_button_text = "Calculate"
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
                situation = create_situation_without_axes(
                    state_code=personal_inputs["state_code"],
                    real_estate_taxes=personal_inputs["real_estate_taxes"],
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
    elif section == "Policy":
        display_policy_config()

# Initialize nationwide impacts if not already done
if "nationwide_impacts" not in st.session_state:
    try:
        st.session_state.nationwide_impacts = NationwideImpacts()
    except Exception as e:
        st.error(f"Error loading nationwide impacts data: {str(e)}")


if "chart_index" not in st.session_state:
    st.session_state.chart_index = 0

# Define the list of available charts
available_charts = [
    "Introduction",
    "SALT and Federal Income Tax Comparison",
    "SALT Deduction Comparison",
    "Taxable Income and AMTI Comparison",
    "Regular Tax and AMT Comparison",
    "Income Tax Comparison",
    "How does this vary with wages",
    "Effective SALT Cap",
    "Regular Tax and AMT Comparison by Income",
    "Gap Chart",
    "Marginal Tax Rate Chart",
    "Effective SALT Cap",
    "Tax Savings Chart",
    "How would you reform SALT/AMT?",
    "Budgetary impacts",
    "Distributional impacts",
    "Key takeaways",
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
current_chart = available_charts[st.session_state.chart_index]
if st.session_state.chart_index == 0:
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

# Check if the sidebar calculate button was clicked
if calculation_is_valid:
    if "last_calculated_inputs" in st.session_state:
        inputs_to_use = st.session_state.last_calculated_inputs
        if st.session_state.chart_index == 1:
            # Get the tax values before creating the table to use in the message
            current_law_results = calculate_df_without_axes(
                state_code=inputs_to_use["state_code"],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                scenario="Current Law",
            )

            current_policy_results = calculate_df_without_axes(
                state_code=inputs_to_use["state_code"],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                scenario="Current Policy",
            )

            # Format the tax values
            law_tax_formatted = f"${current_law_results['federal_income_tax']:,.0f}"
            policy_tax_formatted = (
                f"${current_policy_results['federal_income_tax']:,.0f}"
            )

            # Get the numeric values first
            real_estate_tax = inputs_to_use["real_estate_taxes"]
            larger_of_state_sales_or_income_tax = current_law_results[
                "larger_of_state_sales_or_income_tax"
            ]
            total_salt = real_estate_tax + larger_of_state_sales_or_income_tax

            # Now format them as strings
            real_estate_tax_formatted = f"${real_estate_tax:,.0f}"
            larger_of_state_sales_or_income_tax_formatted = (
                f"${larger_of_state_sales_or_income_tax:,.0f}"
            )
            total_salt_formatted = f"${total_salt:,.0f}"

            state_tax_type = (
                "State Income Tax"
                if current_law_results["state_income_tax_over_sales_tax"]
                else "State Sales Tax"
            )

            # Create the sentence with the tax values
            st.markdown(
                f"### In 2026, you will pay an estimated <span style='color: {BLUE}'>\{larger_of_state_sales_or_income_tax_formatted}</span> in {state_tax_type}. Combined with your <span style='color: {BLUE}'>\{real_estate_tax_formatted}</span> in property taxes, this totals <span style='color: {BLUE}'>\{total_salt_formatted}</span> in total SALT.",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"Federal law allows deducting property taxes and either state and local income taxes, or (actual or estimated) state and local sales taxes."
            )

            # Create the sentence with the tax values
            st.markdown(
                f"### You will owe <span style='color: {BLUE}'>\{law_tax_formatted}</span> in federal income taxes under current law and <span style='color: {BLUE}'>\{policy_tax_formatted}</span> under current policy.",
                unsafe_allow_html=True,
            )

        elif st.session_state.chart_index == 2:
            st.markdown("### Current policy creates an explicit SALT cap")
            display_salt_deduction_comparison_chart(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                employment_income=inputs_to_use["employment_income"],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                show_current_policy=True,
            )
            st.markdown(
                "TCJA capped SALT at $10,000; prior law allowed deductions for all SALT."
            )
        elif st.session_state.chart_index == 3:
            st.markdown("### But AMT income does not vary with SALT")
            display_taxable_income_and_amti_chart(
                state_code=inputs_to_use["state_code"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                employment_income=inputs_to_use["employment_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
            )
            st.markdown(
                "AMT income equals taxable income plus exemptions and deductions including SALT."
            )
        elif st.session_state.chart_index == 4:
            # Calculate effective SALT caps for both policies
            cap_display_law, cap_display_policy = display_effective_salt_cap(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )

            st.markdown(
                f"### With <span style='color: {BLUE}'>{cap_display_law}</span> in SALT, under current law AMT equals regular tax",
                unsafe_allow_html=True,
            )
            display_regular_tax_and_amt_chart(
                state_code=inputs_to_use["state_code"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )
            st.markdown(
                "Additional SALT does not reduce your income tax if AMT exceeds regular tax."
            )
        elif st.session_state.chart_index == 5:
            # Calculate income tax reduction for current law
            current_law_reduction = calculate_salt_income_tax_reduction(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                employment_income=inputs_to_use["employment_income"],
                baseline_scenario="Current Law",
            )

            cap_display_law, cap_display_policy = display_effective_salt_cap(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )

            # Calculate income tax reduction for current policy
            current_policy_reduction = calculate_salt_income_tax_reduction(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                employment_income=inputs_to_use["employment_income"],
                baseline_scenario="Current Policy",
            )

            # Format the values for display
            current_law_value = (
                f"\${current_law_reduction['income_tax_reduction']:,.0f}"
            )
            current_policy_value = (
                f"\${current_policy_reduction['income_tax_reduction']:,.0f}"
            )

            st.markdown(
                f"### You face an effective SALT cap of <span style='color: {BLUE}'>{cap_display_policy}</span> under current policy and <span style='color: {BLUE}'>{cap_display_law}</span> under current law.",
                unsafe_allow_html=True,
            )
            display_income_tax_chart(
                state_code=inputs_to_use["state_code"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                employment_income=inputs_to_use["employment_income"],
                real_estate_taxes=inputs_to_use["real_estate_taxes"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )
            st.markdown(
                f"SALT could lower your taxes by up to <span style='color: {BLUE}'>{current_law_value}</span> under current law and <span style='color: {BLUE}'>{current_policy_value}</span> under current policy. Filers pay the greater of regular tax and AMT.",
                unsafe_allow_html=True,
            )
        elif st.session_state.chart_index == 6:
            st.markdown("### How does this vary with wages?")
        elif st.session_state.chart_index == 7:
            st.markdown("""### AMT effectively caps SALT""")
            display_effective_salt_cap_graph(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                employment_income=inputs_to_use["employment_income"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                policy="Current Law",
            )
            st.markdown(
                "AMT functions as an implicit cap on SALT by disallowing them under AMTI, limiting the tax benefit when AMT exceeds regular tax."
            )
        elif st.session_state.chart_index == 8:
            st.markdown(
                "### The gap from AMT to regular tax influences the effective SALT cap"
            )
            display_regular_tax_and_amt_by_income_chart(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )
            st.markdown(
                "AMT taxes income at a 26% rate for AMTI under $244,000 and 28% above. Your AMT phases in at higher income levels than regular tax due to the AMT exemption. In these earnings variation charts, all points assume no SALT."
            )
        elif st.session_state.chart_index == 9:
            st.markdown(
                "### The gap from AMT to regular tax—absent SALT—influences the effective SALT cap"
            )
            display_gap_chart(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                employment_income=inputs_to_use["employment_income"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )
        elif st.session_state.chart_index == 10:
            st.markdown(
                "### SALT reduces income tax at roughly the regular marginal tax rate"
            )
            display_marginal_rate_chart(
                state_code=inputs_to_use["state_code"],
                is_married=inputs_to_use["is_married"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
            )
            st.markdown(
                "Your marginal tax rate is the additional regular federal income tax (not including credits) owed per additional dollar of taxable income."
            )
        elif st.session_state.chart_index == 11:
            st.markdown("### The effective SALT cap ~= Gap / Marginal tax rate")
            display_effective_salt_cap_graph(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                employment_income=inputs_to_use["employment_income"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                policy="Current Law",
            )
        elif st.session_state.chart_index == 12:
            st.markdown(
                "### Lastly, this is how much you could potentially save due to SALT"
            )
            display_tax_savings_chart(
                is_married=inputs_to_use["is_married"],
                state_code=inputs_to_use["state_code"],
                num_children=inputs_to_use["num_children"],
                child_ages=inputs_to_use["child_ages"],
                employment_income=inputs_to_use["employment_income"],
                qualified_dividend_income=inputs_to_use["qualified_dividend_income"],
                long_term_capital_gains=inputs_to_use["long_term_capital_gains"],
                short_term_capital_gains=inputs_to_use["short_term_capital_gains"],
                deductible_mortgage_interest=inputs_to_use[
                    "deductible_mortgage_interest"
                ],
                charitable_cash_donations=inputs_to_use["charitable_cash_donations"],
                policy="Current Law",
            )
        elif st.session_state.chart_index == 13:
            st.markdown("### How would you reform the SALT deduction and AMT?")
        elif st.session_state.chart_index in (14, 15):
            # Create the Budgetary and distributional impacts section

            policy_config = st.session_state.policy_config

            if not hasattr(st.session_state, "baseline"):
                st.session_state.baseline = "Current Law"
            if not hasattr(st.session_state, "behavioral_responses"):
                st.session_state.behavioral_responses = False

            policy_config["behavioral_responses"] = (
                st.session_state.behavioral_responses
            )

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
                    st.markdown(
                        "Revise your policy using the left sidebar (policy) to see an impact"
                    )
                else:
                    impact_word = "reduce" if total_revenue_impact > 0 else "increase"
                    impact_amount = abs(total_revenue_impact) / 1e12
                    if st.session_state.chart_index == 14:
                        st.markdown(
                            f"""
                            ### Your policy would {impact_word} the deficit by <span style="color: {BLUE}; font-weight: bold;">${impact_amount:.2f} trillion</span> over the 10-year budget window, compared to {st.session_state.baseline}
                            
                            """,
                            unsafe_allow_html=True,
                        )

                        # Show the 10-year impact graph without the title
                        fig = px.bar(
                            budget_window_impacts_df,
                            x="year",
                            y="total_income_change",
                            color_discrete_sequence=[BLUE],
                            labels={
                                "year": "Year",
                                "total_income_change": "Budgetary Impact (in billions)",
                            },
                            text=budget_window_impacts_df.total_income_change.apply(
                                lambda x: f"${abs(x/1e9):,.0f}B"
                            ),
                        )
                        fig = format_fig(fig)
                        # Add margin to ensure logo is visible
                        fig.update_layout(
                            margin=dict(
                                l=20, r=60, t=20, b=80
                            ),  # Increase bottom margin
                        )
                        st.plotly_chart(fig, use_container_width=False)
            else:
                st.warning("No budget window impacts found for the selected reform.")

            if not hasattr(st.session_state, "nationwide_impacts"):
                st.error("No impact data available. Please check data files.")
            else:
                if st.session_state.chart_index == 15:
                    # Construct reform name
                    reform_name = get_reform_name(
                        st.session_state.policy_config, st.session_state.baseline
                    )

                    # Get impact data for the selected reform
                    impacts_data = (
                        st.session_state.nationwide_impacts.single_year_impacts
                    )
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
                                dist_data = st.session_state.nationwide_impacts.get_income_distribution(
                                    reform_name
                                )
                                if dist_data is not None:

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
        elif st.session_state.chart_index == 16:
            st.markdown("### Key takeaways")
            st.markdown(
                """
            * AMT creates an effective SALT cap
            * This moves with the gap between regular tax and AMT (assuming no SALT), and the marginal tax rate
            * **Coming soon**: how custom policies affect your household 
            
            *This project was made possible with generous support from [Arnold Ventures](https://arnoldventures.org)*
        """
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
            st.markdown(f"**{available_charts[st.session_state.chart_index]}**")

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
        "Your inputs have changed. Click 'Calculate' in the sidebar to generate new charts."
    )
elif (
    "calculate_clicked" not in st.session_state
    or not st.session_state.calculate_clicked
):
    # No calculation has been performed yet
    st.info(
        "Please fill out your personal information in the sidebar and click 'Calculate' to continue."
    )
else:
    # Some other edge case
    st.warning("Please try recalculating your impacts from the sidebar.")


display_notes()
