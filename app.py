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
from household_examples import TAX_CALCULATIONS, STATE_CODES, INCOME_LEVELS


# Set up the Streamlit page
st.set_page_config(page_title="SALT and AMT Policy Calculator", layout="wide")


# Set up sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Go to",
        ["Introduction", "Case Studies", "Policy Configuration", "Personalized Calculator"]
    )
    
    st.markdown("---")
    st.markdown("""
    _This tool is designed to help you understand and model SALT and AMT policy changes_
    """)


# Main content
st.title("What's the SALTernative?")
st.markdown(
    """
    _The state and local tax (SALT) deduction and alternative minimum tax (AMT) are scheduled to change next year. We'll walk you through these policies and allow you to model your custom reform._\n
    This tool starts by describing the SALT deduction and AMT, both under _current law_ (given the expiration of the Tax Cuts and Jobs Act (TCJA) in 2026) and under _current policy_ (if the TCJA was extended beyond 2025). Then we'll explain these policies in the context of sample households. Finally, we'll put you in the driver's seat - you can design and simulate a range of SALT and AMT reforms, and we'll calculate how it affects the US and your household. Let's dive in!
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
    st.markdown(
        """
    ## SALT and AMT Basics

    **SALT:** Filers can take an itemized deduction for (a) property taxes and (b) _either_ state and local income or sales taxes. The TCJA capped the SALT deduction at \$10,000 from 2018 to 2025; beginning next year, it is scheduled to be uncapped. [Learn more about how we model SALT](https://docs.google.com/document/d/1ATmkzrq8e5TS-p4JrIgyXovqFdHEHvnPtqpUC0z8GW0/preview).

    **AMT:** Filers must calculate their tax liability under the regular tax code as well as the alternative minimum tax and pay the higher amount. The AMT disallows certain preference items, including but not limited to the SALT deduction, the miscellaneous deductions, and the personal exemptions. The TCJA has (1) expanded the exemption amount that applies to AMT-specific income and (2) increased the threshold at which this exemption phases out at a rate of 25%. [Learn more about how we model AMT](https://docs.google.com/document/d/1uAwllrnbS7Labq7LvxSEjUdZESv0H5roDhmknldqIDA/preview).
    
    ## What We'll Demonstrate

    In this analysis, we'll show how the interaction between the SALT deduction and AMT creates an **effective SALT cap**. We'll demonstrate that while the SALT cap is officially removed in 2026, the AMT effectively limits how much state and local as well as property tax certain households can deduct, creating a de facto cap that's different from the current explicit \$10,000 cap.
    
    Along the way, we'll introduce two key concepts:
    - **"Property tax subsidy rate"** - a new metric that measures what percentage of each additional dollar in property taxes is effectively subsidized through federal tax savings
    - **"Effective SALT cap"** - the maximum SALT deduction a household can benefit from, even when no explicit cap exists
    
    We'll examine these through:
    1. Detailed case studies of multiple households at different income levels
    2. Comparison of tax calculations at \$5K, \$10K, and \$15K property tax levels to reveal how the benefit of additional property taxes changes
    3. Visualization of these effects across a wider range of property tax amounts
    """
    )

elif page == "Case Studies":
    # Only show the case studies part
    st.markdown(
        """
    ## How SALT and AMT Affect Sample Households
        
    **Please select a state and income level to see how SALT and AMT affect a sample household.**
    """
    )
    
    # Add state and income selectors from the display_introduction function
    from household_examples import STATE_CODES, INCOME_LEVELS, TAX_CALCULATIONS
    
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox("Select State", list(STATE_CODES.keys()), index=0)
    with col2:
        selected_income = st.selectbox(
            "Select Earnings Level", list(INCOME_LEVELS.keys()), index=1
        )
    
    # Get the state code and income value
    state_code = STATE_CODES[selected_state]
    income_value = INCOME_LEVELS[selected_income]
    
    # Continue with the sample household analysis
    from household_examples import (
        get_salt_deduction_table,
        get_tax_liability_table,
        get_amt_table,
        get_state_tax_description,
        get_higher_property_tax_comparison,
        get_comprehensive_tax_table,
    )
    from constants import TEAL_ACCENT
    
    st.markdown(
        f"""
    
    Let's consider a married filer in {selected_state} with:
    * {selected_income} in wages and salaries 
    * \$15,000 in deductible mortgage interest 
    * \$10,000 in charitable cash donations 

    
     *We can calculate the effective SALT cap for any household in the personal calculator below.*
    
    ### SALT Deduction
    """
    )
    
    # Get the SALT deduction comparison table
    df_comparison = get_salt_deduction_table(state_code, income_value)
    
    st.markdown(
        """
    Table 1 shows how much of the property taxes plus state and local taxes can be deducted under each scenario.
    """
    )
    
    st.markdown(
        f"**Table 1: SALT Deduction Comparison for a Household in {selected_state} with {selected_income} in Earnings**"
    )
    st.table(df_comparison.set_index("Scenario"))
    
    # Get state tax description
    state_tax_description = get_state_tax_description(state_code, income_value)
    
    st.markdown(
        f"""
    {state_tax_description}
    
    Under current law, the entire amount of property taxes plus state and local taxes is deductible. Under current policy, this amount is subject to the SALT deduction cap of \$10,000, limiting the total deduction amount.
    """
    )
    
    st.markdown(
        """
    ### Regular Tax Liability
    The increased SALT deduction under current law will lower the household's taxable income, which in turn results in lower regular tax liabilities. Table 2 shows the regular tax liability (before considering AMT) for each scenario.
    """
    )
    
    # Get the tax liability comparison table
    df_comparison = get_tax_liability_table(state_code, income_value)
    
    st.markdown(
        f"**Table 2: Regular Tax Liability Comparison for a Household in {selected_state} with {selected_income} in Earnings**"
    )
    st.table(df_comparison.set_index("Scenario"))
    
    st.markdown(
        """
    ### Alternative Minimum Tax
    
    The alternative minimum tax computation begins with the regular taxable income which is increased to compute the alternative minimum taxable income (AMTI). Firstly, the personal exemption amount, which was reduced to $0 under the TCJA, is added back to the taxable income. For non-itemizers the standard deduction amount is also added back. For filers who itemize, the SALT deduction and other preference items, which are excluded from regular taxable income, are included in the AMTI calculation.
    
    The AMTI is then reduced by an exemption amount, which phases out for higher income levels, before a tax rate of either 26% or 28% is applied to determine the **tentative minimum tax**. (Additional rules may apply for households with capital gains and dividend income.) Table 3 shows the tentative minimum tax for each scenario.
    """
    )
    
    # Get the AMT comparison table
    df_comparison = get_amt_table(state_code, income_value)
    
    st.markdown(
        f"**Table 3: AMT Comparison for a Household in {selected_state} with {selected_income} in Earnings**"
    )
    st.table(df_comparison.set_index("Scenario"))
    
    st.markdown(
        """
    The household is required to pay the higher of the regular tax or the tentative minimum tax amount.
    """
    )
    
    st.markdown(
        """
    ### Property Tax Subsidy Rates
    
    One way to assess the impact of these tax policies is by examining how much of a household's property taxes is offset by reductions in income tax liability. The **property tax subsidy rate** measures what percentage of each additional dollar in property taxes is effectively subsidized through tax savings.
    
    For example, if a household pays an additional \$5,000 in property taxes and their federal tax bill decreases by \$1,250, their property tax subsidy rate is 25% (\$1,250 ÷ \$5,000). This means 25% of each additional property tax dollar is effectively subsidized through federal tax savings.
    
    When a household is subject to the AMT or hits the SALT deduction cap, their property tax subsidy rate can drop significantly or even reach zero, meaning they receive no federal tax benefit from additional property tax payments. Table 4 summarizes the key tax calculations and shows the resulting property tax subsidy rates.
    """
    )
    
    # Get the comprehensive tax table with subsidy rates
    df_comparison = get_comprehensive_tax_table(state_code, income_value)
    
    st.markdown(
        f"**Table 4: Tax Calculations and Property Tax Subsidy Rates for a Household in {selected_state} with {selected_income} in Earnings**"
    )
    st.table(df_comparison.set_index(["Scenario", "Quantity"]))
    
    # Extract only the AMT and regular tax values needed for determining if AMT applies
    # Make sure we're using the correct state and income level data
    if state_code in TAX_CALCULATIONS and income_value in TAX_CALCULATIONS[state_code]:
        tax_calcs = TAX_CALCULATIONS[state_code][income_value]
    else:
        # If the specific combination doesn't exist, show an error or use a fallback
        st.error(
            f"Tax calculation data not available for {selected_state} at {selected_income} income level."
        )
        # Use NY at 250k as absolute fallback only if needed
        tax_calcs = TAX_CALCULATIONS["NY"][250000]
    
    # Extract values directly from tax_calcs dictionary
    current_law_5k_amt = tax_calcs["current_law"]["5k_property_taxes"]["amt"]
    current_law_5k_regular = tax_calcs["current_law"]["5k_property_taxes"][
        "regular_tax"
    ]
    current_policy_5k_amt = tax_calcs["current_policy"]["5k_property_taxes"]["amt"]
    current_policy_5k_regular = tax_calcs["current_policy"]["5k_property_taxes"][
        "regular_tax"
    ]
    
    # Check if AMT applies (when AMT >= Regular Tax)
    amt_applies_current_law = current_law_5k_amt >= current_law_5k_regular
    amt_applies_current_policy = current_policy_5k_amt >= current_policy_5k_regular
    
    # Add information about current law
    if amt_applies_current_law:
        subsidy_finding = "Under current law, the AMT applies for this household. Even though the explicit SALT cap is removed, additional property taxes are not fully subsidized because the AMT disallows the SALT deduction."
    else:
        subsidy_finding = "Under current law, the regular tax applies for this household. Property taxes are subsidized through the SALT deduction with no explicit cap."
    
    # Add another line break before current policy information
    subsidy_finding += "\n\n"
    
    # Add information about current policy
    if amt_applies_current_policy:
        subsidy_finding += "Under current policy, the AMT applies for this household. Property taxes are not fully subsidized due to both the explicit $10,000 SALT cap and the AMT disallowing the SALT deduction."
    else:
        subsidy_finding += "Under current policy, the regular tax applies for this household. Property taxes are subsidized through the SALT deduction but limited by the explicit $10,000 SALT cap."
    
    # Display the subsidy finding without the heading
    st.markdown(f"{subsidy_finding}")
    
    # Display the heading separately
    st.markdown(
        """
    ### Now let's examine the same household with higher property taxes
    
    By comparing tax calculations at \$5k, \$10k, and \$15k property tax levels, we can determine:
    1. How the property tax subsidy rate changes as property taxes increase
    2. Whether the AMT begins to apply at higher property tax levels
    3. The point at which additional property taxes no longer provide tax benefits (the effective SALT cap)
    """
    )
    
    # Get the higher property tax comparison table
    df_comparison = get_higher_property_tax_comparison(state_code, income_value)
    
    st.markdown(
        f"**Table 5: Tax Liability Comparison at Different Property Tax Levels for a Household in {selected_state} with {selected_income} in Earnings**"
    )
    st.table(df_comparison.set_index("Scenario"))
    
    # Extract AMT and regular tax values for 10k and 15k property taxes
    # Make sure we're using the correct state and income level data
    if state_code in TAX_CALCULATIONS and income_value in TAX_CALCULATIONS[state_code]:
        tax_calcs = TAX_CALCULATIONS[state_code][income_value]
    else:
        # If the specific combination doesn't exist, show an error or use a fallback
        st.error(
            f"Tax calculation data not available for {selected_state} at {selected_income} income level."
        )
        # Use NY at 250k as absolute fallback only if needed
        tax_calcs = TAX_CALCULATIONS["NY"][250000]
    
    # Check if AMT applies at 10k property tax level
    current_law_10k_amt = tax_calcs["current_law"]["10k_property_taxes"]["amt"]
    current_law_10k_regular = tax_calcs["current_law"]["10k_property_taxes"][
        "regular_tax"
    ]
    current_policy_10k_amt = tax_calcs["current_policy"]["10k_property_taxes"]["amt"]
    current_policy_10k_regular = tax_calcs["current_policy"]["10k_property_taxes"][
        "regular_tax"
    ]
    
    amt_applies_current_law_10k = current_law_10k_amt >= current_law_10k_regular
    amt_applies_current_policy_10k = (
        current_policy_10k_amt >= current_policy_10k_regular
    )
    
    # Check if AMT applies at 15k property tax level
    current_law_15k_amt = tax_calcs["current_law"]["15k_property_taxes"]["amt"]
    current_law_15k_regular = tax_calcs["current_law"]["15k_property_taxes"][
        "regular_tax"
    ]
    current_policy_15k_amt = tax_calcs["current_policy"]["15k_property_taxes"]["amt"]
    current_policy_15k_regular = tax_calcs["current_policy"]["15k_property_taxes"][
        "regular_tax"
    ]
    
    amt_applies_current_law_15k = current_law_15k_amt >= current_law_15k_regular
    amt_applies_current_policy_15k = (
        current_policy_15k_amt >= current_policy_15k_regular
    )
    
    # Create dynamic finding for the higher property tax comparison
    if amt_applies_current_law_10k and amt_applies_current_law_15k:
        higher_property_tax_finding = "The AMT applies under current law at both \$10k and $15k property tax levels. Even though the explicit SALT cap is removed, the AMT effectively limits the benefit of additional property tax deductions."
    elif amt_applies_current_law_15k and not amt_applies_current_law_10k:
        higher_property_tax_finding = "As property taxes increase to $15k under current law, the household becomes subject to the AMT, which limits the benefit of additional property tax deductions despite the removal of the explicit SALT cap."
    elif not amt_applies_current_law_10k and not amt_applies_current_law_15k:
        higher_property_tax_finding = "Under current law, the household remains on the regular tax system even at higher property tax levels, allowing them to more fully benefit from the removal of the SALT cap."
    
    # Add a line break before current policy information
    higher_property_tax_finding += "\n\n"
    
    # Add information about current policy
    if amt_applies_current_policy_10k and amt_applies_current_policy_15k:
        higher_property_tax_finding += " Under current policy, the AMT applies at both property tax levels, further limiting deductions beyond the explicit $10,000 SALT cap."
    elif amt_applies_current_policy_15k and not amt_applies_current_policy_10k:
        higher_property_tax_finding += " Under current policy, the household becomes subject to the AMT at the $15k property tax level, which works alongside the explicit $10,000 SALT cap to limit deductions."
    elif not amt_applies_current_policy_10k and not amt_applies_current_policy_15k:
        higher_property_tax_finding += " Under current policy, the household remains on the regular tax system due to the explicit $10,000 SALT cap."
    
    # Get effective SALT caps directly from TAX_CALCULATIONS
    effective_caps = {
        "current_law": tax_calcs["effective_salt_cap"]["current_law"],
        "current_policy": tax_calcs["effective_salt_cap"]["current_policy"],
    }
    
    # Create formatted strings for the effective SALT caps
    current_law_cap_str = (
        "No effective SALT cap"
        if effective_caps["current_law"] == float("inf")
        else f"<span style='color: {TEAL_ACCENT}; font-weight: bold;'>${effective_caps['current_law']:,}</span>"
    )
    current_policy_cap_str = (
        "No effective SALT cap"
        if effective_caps["current_policy"] == float("inf")
        else f"<span style='color: {TEAL_ACCENT}; font-weight: bold;'>${effective_caps['current_policy']:,}</span>"
    )
    
    st.markdown(
        f"""
    
    {higher_property_tax_finding}
    """
    )
    
    # Format the SALT cap text with no effective SALT cap handling
    if effective_caps["current_law"] == float("inf") and effective_caps[
        "current_policy"
    ] == float("inf"):
        st.markdown(
            """
            <div style="text-align: center; margin: 25px 0;">
                <h3 style="color: #777777;">This household faces no effective SALT cap under either current law or current policy</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif effective_caps["current_law"] == float("inf"):
        st.markdown(
            f"""
            <div style="text-align: center; margin: 25px 0;">
                <h3 style="color: #777777;">This household faces no effective SALT cap under current law but faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${effective_caps['current_policy']:,}</span> under current policy</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif effective_caps["current_policy"] == float("inf"):
        st.markdown(
            f"""
            <div style="text-align: center; margin: 25px 0;">
                <h3 style="color: #777777;">This household faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${effective_caps['current_law']:,}</span> under current law but faces no effective SALT cap under current policy</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="text-align: center; margin: 25px 0;">
                <h3 style="color: #777777;">This household faces an effective SALT cap of <span style="color: {TEAL_ACCENT}; font-weight: bold;">${effective_caps['current_law']:,}</span> under current law and <span style="color: {TEAL_ACCENT}; font-weight: bold;">${effective_caps['current_policy']:,}</span> under current policy</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown(
        """
    ### Visualizing These Effects Across Different Property Tax Amounts
    
    The charts below show how tax liabilities and subsidy rates change as property taxes increase from \$0 to \$50k.
    """
    )
    # Read the CSV files
    with st.expander("See detailed tax calculations and charts"):
        import pandas as pd
        import plotly.graph_objects as go
        from policyengine_core.charts import format_fig
        from constants import DARK_GRAY, BLUE
        
        # Load the data for all states and income levels
        df_all = pd.read_csv(
            "personal_calculator/data/all_state_income_tax_calculations_2026.csv"
        )
        
        # Filter the data based on the selected state and income
        df = df_all[
            (df_all["state"] == state_code) & (df_all["income"] == income_value)
        ]
        
        # Create tax liability comparison plot
        fig2 = go.Figure()
        # Current Policy traces
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_policy_regular_tax"],
                mode="lines",
                name="Current Policy Regular Tax",
                line=dict(color=DARK_GRAY, dash="solid"),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_policy_amt"],
                mode="lines",
                name="Current Policy Tentative AMT",
                line=dict(color=DARK_GRAY, dash="dash"),
            )
        )
        # Current Law traces
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_law_regular_tax"],
                mode="lines",
                name="Current Law Regular Tax",
                line=dict(color=BLUE, dash="solid"),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_law_amt"],
                mode="lines",
                name="Current Law Tentative AMT",
                line=dict(color=BLUE, dash="dash"),
            )
        )
        fig2.update_layout(
            title=f"Figure 1: Tax Liability Comparison by Property Taxes ({selected_state}, {selected_income})",
            xaxis_title="Property Taxes ($)",
            yaxis_title="Tax Liability ($)",
            showlegend=True,
            template="simple_white",
            height=500,
            xaxis=dict(range=[0, None]),
            yaxis=dict(range=[0, None]),
        )
        
        st.markdown(
            """
        #### Figure 1: Tax Liability Chart
        This chart shows how regular tax and AMT change as property taxes increase. Where the dashed line (AMT) is above the solid line (regular tax), the household pays the AMT amount, potentially limiting the benefit of the SALT deduction.
        """
        )
        
        st.plotly_chart(format_fig(fig2))
        
        # Add subsidy rates plot for both years
        df_all_subsidy = pd.read_csv(
            "personal_calculator/data/all_state_income_subsidy_rates_2026.csv"
        )
        
        # Filter data based on selected state and income
        df_subsidy = df_all_subsidy[
            (df_all_subsidy["state"] == state_code)
            & (df_all_subsidy["income"] == income_value)
        ]
        
        # Filter data for current policy and current law
        df_2025 = df_subsidy[df_subsidy["Simulation"] == "Current Policy"]
        df_2026 = df_subsidy[df_subsidy["Simulation"] == "Current Law"]
        
        # Create the plot
        fig3 = go.Figure()
        fig3.add_trace(
            go.Scatter(
                x=df_2025["Property Taxes"],
                y=df_2025["Subsidy Rate (%)"],
                mode="lines",
                name="Current Policy",
                line=dict(color=DARK_GRAY),
            )
        )
        fig3.add_trace(
            go.Scatter(
                x=df_2026["Property Taxes"],
                y=df_2026["Subsidy Rate (%)"],
                mode="lines",
                name="Current Law",
                line=dict(color=BLUE),
            )
        )
        fig3.update_layout(
            title=f"Figure 2: Property Tax Marginal Subsidy Rate ({selected_state}, {selected_income})",
            xaxis_title="Property Taxes ($)",
            yaxis_title="Subsidy Rate (%)",
            showlegend=True,
            template="simple_white",
            height=500,
        )
        
        st.markdown(
            """
        #### Figure 2: Subsidy Rate Chart
        This chart shows the property tax subsidy rate - the percentage of each additional dollar of property tax that is effectively subsidized through tax savings. 
        
        Several key patterns to observe:
        - Flat lines indicate no additional tax benefit from property tax increases (0% subsidy rate)
        - Downward slopes indicate diminishing benefits as property taxes increase
        - Step changes often indicate when a household transitions from regular tax to AMT or hits deduction limits
        
        Some of the marginal subsidy rates also reflect state-level property tax related deductions and credits.
        """
        )

    # Create a table showing effective SALT caps for each state and income level
    st.markdown("## Effective SALT Caps by State and Income Level")
    st.markdown("""
    This table shows the effective SALT cap for married households across different states and income levels under current law (2026). 
    Each household has \$15,000 in mortgage interest and $10,000 in charitable donations.
    """)

    st.markdown(
        f"**Table 6: Effective SALT Caps by State and Income Level**"
    )

    # Extract data from TAX_CALCULATIONS in household_examples.py
    from household_examples import TAX_CALCULATIONS, STATE_CODES, INCOME_LEVELS

    # Create a DataFrame to hold the effective SALT caps
    import pandas as pd
    import numpy as np

    # Get state codes and income levels
    states = list(STATE_CODES.values())
    incomes = list(INCOME_LEVELS.values())
    income_labels = list(INCOME_LEVELS.keys())

    # Create empty DataFrame with states as rows and income levels as columns
    effective_salt_caps = pd.DataFrame(index=states, columns=income_labels)

    # Fill the DataFrame with effective SALT cap values
    for state in states:
        for i, income in enumerate(incomes):
            if state in TAX_CALCULATIONS and income in TAX_CALCULATIONS[state]:
                cap = TAX_CALCULATIONS[state][income]["effective_salt_cap"]["current_law"]
                # Format the cap value
                if cap == float("inf"):
                    effective_salt_caps.loc[state, income_labels[i]] = "∞"
                else:
                    effective_salt_caps.loc[state, income_labels[i]] = f"${cap:,.0f}"
            else:
                effective_salt_caps.loc[state, income_labels[i]] = "N/A"

    # Create a mapping of state codes to state names for better readability
    state_names = {v: k for k, v in STATE_CODES.items()}
    effective_salt_caps.index = [state_names.get(state, state) for state in effective_salt_caps.index]

    # Display the table
    st.table(effective_salt_caps)

elif page == "Policy Configuration":
    # Display baseline impacts section first
    display_baseline_impacts()
    
    # Display policy configuration section
    st.markdown("## Configure Your Policy")
    policy_config = display_policy_config()

elif page == "Personalized Calculator":
    # Create the Personalized Calculator section
    st.markdown("## Personalized Calculator")
    
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
    
    # Household calculator tab content
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

# Add Notes section at the app level after any sections are displayed
if page in ["Case Studies", "Policy Configuration", "Personalized Calculator"]:
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