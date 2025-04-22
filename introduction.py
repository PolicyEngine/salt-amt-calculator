import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, BLUE, TEAL_ACCENT, TEAL_LIGHT, TEAL_PRESSED
from household_examples import (
    STATE_CODES,
    INCOME_LEVELS,
    TAX_CALCULATIONS,
    get_salt_deduction_table,
    get_tax_liability_table,
    get_amt_table,
    get_state_tax_description,
    get_higher_property_tax_comparison,
    get_comprehensive_tax_table,
)
from personal_calculator.salt_cap_calculator import (
    calculate_single_axis_effective_salt_cap,
    process_effective_cap_data,
    calculate_effective_salt_cap_over_earnings,
    create_max_salt_line_graph,
)


def display_salt_basics():
    """Display the basic description of SALT and AMT"""
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


def create_state_income_selectors():
    """Create state and income level selectors"""
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

    return selected_state, selected_income, state_code, income_value


def display_salt_deduction_section(
    selected_state, selected_income, state_code, income_value
):
    """Display the SALT deduction comparison section"""
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


def display_tax_liability_section(
    selected_state, selected_income, state_code, income_value
):
    """Display the tax liability comparison section"""
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


def display_amt_section(selected_state, selected_income, state_code, income_value):
    """Display the AMT comparison section"""
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


def display_subsidy_rates_section(
    selected_state, selected_income, state_code, income_value
):
    """Display the property tax subsidy rates section"""
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

    return tax_calcs


def display_higher_property_tax_section(
    selected_state, selected_income, state_code, income_value, tax_calcs
):
    """Display the higher property tax comparison section"""
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

    st.markdown(
        f"""
    
    {higher_property_tax_finding}
    """
    )

    return tax_calcs["effective_salt_cap"]


def display_effective_salt_cap(
    state_code,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    employment_income,
    policy=None,
    reform_params=None,
    threshold=0.1,
):

    # Calculate for single axis (fixed employment income)
    result_df = calculate_single_axis_effective_salt_cap(
        state_code,
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        employment_income,
        baseline_scenario=policy,
        reform_params=reform_params,
    )

    # Process the data to calculate marginal rates
    processed_df = process_effective_cap_data(result_df)

    # Find the effective cap (maximum SALT where marginal rate > threshold)
    filtered_df = processed_df[processed_df["marginal_property_tax_rate"] > threshold]

    if not filtered_df.empty:
        effective_cap = filtered_df["salt_and_property_tax"].max()
        has_cap = True
    else:
        effective_cap = float("inf")
        has_cap = False

    # Format the cap value (round to nearest 100)
    def format_cap(cap_value):
        if cap_value == float("inf"):
            return None
        else:
            # Round to nearest 100
            rounded_cap = round(cap_value / 100) * 100
            return f"${rounded_cap:,.0f}"

    # Get formatted value for display
    cap_display = format_cap(effective_cap)

    # Display the effective cap message
    st.markdown(
        f"""
        <div style="text-align: center; margin: 5px 0;">
            <h3 style="color: #777777;">Your household faces {f'an effective SALT cap of <span style="color: {BLUE}; font-weight: bold;">{cap_display}</span>' if has_cap else 'no effective SALT cap'} under {policy}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return effective_cap


def display_tax_visualization(
    selected_state, selected_income, state_code, income_value
):
    """Display tax visualizations with charts"""
    st.markdown(
        """
    ### Visualizing These Effects Across Different Property Tax Amounts
    
    The charts below show how tax liabilities and subsidy rates change as property taxes increase from \$0 to \$50k.
    """
    )

    # Read the CSV files
    with st.expander("See detailed tax calculations and charts"):
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

        st.plotly_chart(format_fig(fig3))


def display_effective_salt_caps_table():
    """Display the table of effective SALT caps for all states and income levels"""

    st.markdown("## Effective SALT Caps by State and Income Level")
    st.markdown(
        """
    The graphs below show the effective SALT cap for married couples across different income levels under current law in 2026. 
    """
    )

    st.image("images/single-cap.png")


def display_notes():
    """Display notes section at the bottom of the app"""
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


def display_introduction():
    # Display SALT and AMT basics
    display_salt_basics()

    # Section header for case studies
    st.markdown(
        """
    ## How SALT and AMT Affect Sample Households
    """
    )

    # Create state and income selectors
    selected_state, selected_income, state_code, income_value = (
        create_state_income_selectors()
    )

    # Display SALT deduction section
    display_salt_deduction_section(
        selected_state, selected_income, state_code, income_value
    )

    # Display tax liability section
    display_tax_liability_section(
        selected_state, selected_income, state_code, income_value
    )

    # Display AMT section
    display_amt_section(selected_state, selected_income, state_code, income_value)

    # Display subsidy rates section and get tax calculations
    tax_calcs = display_subsidy_rates_section(
        selected_state, selected_income, state_code, income_value
    )

    # Display higher property tax section and get effective caps
    effective_caps = display_higher_property_tax_section(
        selected_state, selected_income, state_code, income_value, tax_calcs
    )

    # Display effective SALT cap
    display_effective_salt_cap(effective_caps)

    # Display tax visualization
    display_tax_visualization(selected_state, selected_income, state_code, income_value)


def display_effective_salt_cap_graph(
    state_code,
    is_married,
    num_children,
    child_ages,
    qualified_dividend_income,
    long_term_capital_gains,
    short_term_capital_gains,
    deductible_mortgage_interest,
    charitable_cash_donations,
    policy=None,
    reform_params=None,
    threshold=0.1,
):
    """Display the effective SALT cap graph using the two axes situation"""

    # Calculate for two axes (varying employment income)
    result_df = calculate_effective_salt_cap_over_earnings(
        state_code,
        is_married,
        num_children,
        child_ages,
        qualified_dividend_income,
        long_term_capital_gains,
        short_term_capital_gains,
        deductible_mortgage_interest,
        charitable_cash_donations,
        baseline_scenario=policy,
        reform_params=reform_params,
    )

    # Process the data to calculate marginal rates
    processed_df = process_effective_cap_data(result_df)

    # Create the graph
    fig = create_max_salt_line_graph(processed_df, policy=policy, threshold=threshold)

    # Display the graph
    st.plotly_chart(format_fig(fig), use_container_width=True)

    return processed_df
