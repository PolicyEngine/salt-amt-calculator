import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, BLUE
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


def display_introduction():
    st.markdown(
        """
    ## SALT and AMT Basics

    **SALT:** Filers can take an itemized deduction for (a) property taxes and (b) _either_ state and local income taxes or sales taxes. The TCJA capped the SALT deduction at \$10,000 from 2018 to 2025; beginning next year, it will be uncapped.

    **AMT:** Filers must calculate their tax liability under the regular tax code and the AMT and pay the higher amount. The AMT disallows certain deductions, including the SALT deduction. The TCJA has (1) expanded the exemption amount that applies to AMT-specific income and (2) increased the threshold at which this exemption phases out at a rate of 25%.
    
    ## What We'll Demonstrate

    In this analysis, we'll show how the interaction between SALT deductions and AMT creates an **effective SALT cap** even when the explicit SALT cap expires in 2026 (current law). We'll demonstrate that while the SALT cap is officially removed in 2026, the AMT effectively limits how much property tax high-income households can deduct, creating a de facto cap that's different from the explicit \$10,000 cap under current policy (2025).
    
    We'll examine this through:
    1. Detailed case study of mutliple households at different income levels
    2. Analysis of property tax subsidy rates (how much tax relief households get per dollar of property tax)
    3. Visualization of these effects across different property tax amounts
    
    ## How SALT and AMT Affect a Sample Household
    """
    )
    st.markdown(
        """
    **Please select a state and income level to see how SALT and AMT affect a sample household.**

    *Please note - we can calculate the effective SALT cap for any household in the personal calculator below.*
    """
    )

    # Add state and income selectors
    col1, col2 = st.columns(2)
    with col1:
        selected_state = st.selectbox("Select State", list(STATE_CODES.keys()), index=0)
    with col2:
        selected_income = st.selectbox(
            "Select Income Level", list(INCOME_LEVELS.keys()), index=1
        )

    # Get the state code and income value
    state_code = STATE_CODES[selected_state]
    income_value = INCOME_LEVELS[selected_income]

    st.markdown(
        f"""
    

    Let's consider a married filer in {selected_state} with:
    * {selected_income} in wages and salaries 
    * \$15,000 in deductible mortgage interest 
    * \$10,000 in charitable cash donations 

    
    ### SALT Deduction
    """
    )

    # Get the SALT deduction comparison table
    df_comparison = get_salt_deduction_table(state_code, income_value)

    st.markdown(
        """
    The table below shows how much of the property taxes plus state and local taxes can be deducted under each scenario:
    """
    )

    st.table(df_comparison.set_index("Scenario"))

    # Get state tax description
    state_tax_description = get_state_tax_description(state_code, income_value)

    st.markdown(
        f"""
    {state_tax_description}
    
    Under current law (2026), the entire amount of property taxes plus state and local taxes is deductible. Under current policy (2025), this amount is subject to the SALT deduction cap of \$10,000, limiting the total deduction amount.
    """
    )

    st.markdown(
        """
    ### Regular Tax Liability
    The increased SALT deduction under current law will lower the household's taxable income, which in turn results in lower regular tax liabilities. The table below shows the regular tax liability (before considering AMT) for each scenario:
    """
    )

    # Get the tax liability comparison table
    df_comparison = get_tax_liability_table(state_code, income_value)

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    ### Alternative Minimum Tax (AMT)

    The alternative minimum tax (AMT) begins with the regular taxable income and then makes specific adjustments to compute an alternative taxable income. For filers taking the standard deduction, that amount is simply used. However, for filers who itemize, only the SALT deduction—and a few other select items that are excluded from regular taxable income—is added back. This adjusted income is then reduced by an exemption amount, which phases out for higher levels of AMT income, before a tax rate of either 26% or 28% is applied to determine the **tentative minimum tax**. (Additional rules may apply for households with capital gains and dividend income.)
    
    The table below shows the tentative minimum tax for each scenario:
    """
    )

    # Get the AMT comparison table
    df_comparison = get_amt_table(state_code, income_value)

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    The excess of the tentative minimum tax over the regular tax liability is added back to compute the AMT liability. The household must pay the higher of the regular tax or the tentative minimum tax.
    """
    )

    st.markdown(
        """
    ### Property Tax Subsidy Rates

    One way to assess the impact of these tax policies is by examining how much of a household's property taxes is offset by reductions in income tax liability. The **property tax subsidy rate** measures what percentage of each additional dollar in property taxes is effectively subsidized through tax savings.
    
    The table below summarizes all the key tax calculations and shows the resulting property tax subsidy rates:
    """
    )

    # Get the comprehensive tax table with subsidy rates
    df_comparison = get_comprehensive_tax_table(state_code, income_value)

    st.table(df_comparison.set_index(["Scenario", "Quantity"]))


    # Extract only the AMT and regular tax values needed for determining if AMT applies
    amt_rows = df_comparison[df_comparison["Quantity"] == "Tentative Minimum Tax"]
    current_law_5k_amt = float(
        amt_rows["$5k property taxes"].iloc[0].replace("$", "").replace(",", "")
    )
    current_policy_5k_amt = float(
        amt_rows["$5k property taxes"].iloc[1].replace("$", "").replace(",", "")
    )

    regular_tax_rows = df_comparison[
        df_comparison["Quantity"] == "Regular Tax Liability"
    ]
    current_law_5k_regular = float(
        regular_tax_rows["$5k property taxes"].iloc[0].replace("$", "").replace(",", "")
    )
    current_policy_5k_regular = float(
        regular_tax_rows["$5k property taxes"].iloc[1].replace("$", "").replace(",", "")
    )

    # Check if AMT applies (when AMT >= Regular Tax)
    amt_applies_current_law = current_law_5k_amt >= current_law_5k_regular
    amt_applies_current_policy = current_policy_5k_amt >= current_policy_5k_regular

    # Create detailed explanations based on AMT application
    if amt_applies_current_law:
        current_law_explanation = "Under current law, the AMT applies for this household. Even though the explicit SALT cap is removed, additional property taxes are not fully subsidized because the AMT disallows the SALT deduction."
    else:
        current_law_explanation = "Under current law, the regular tax applies for this household. Property taxes are subsidized through the SALT deduction with no explicit cap."
        
    if amt_applies_current_policy:
        current_policy_explanation = "Under current policy, the AMT applies for this household. Property taxes are not fully subsidized due to both the explicit $10,000 SALT cap and the AMT disallowing the SALT deduction."
    else:
        current_policy_explanation = "Under current policy, the regular tax applies for this household. Property taxes are subsidized through the SALT deduction but limited by the explicit $10,000 SALT cap."

    # Create findings for the Property Tax Subsidy Rates table
    if amt_applies_current_law and amt_applies_current_policy:
        subsidy_finding = "Under both current law and current policy, the AMT applies, limiting the benefit of the SALT deduction."
    elif amt_applies_current_law:
        subsidy_finding = "Under current law, the AMT applies, limiting the benefit of the SALT deduction. Under current policy, the regular tax liability exceeds the tentative minimum tax."
    elif amt_applies_current_policy:
        subsidy_finding = "Under current policy, the AMT applies, limiting the benefit of the SALT deduction. Under current law, the regular tax liability exceeds the tentative minimum tax."
    else:
        subsidy_finding = "Under both current law and current policy, the regular tax liability exceeds the tentative minimum tax. The AMT does not apply in either scenario."

    st.markdown(
        f"""
    
    {subsidy_finding}
    
    {current_law_explanation}
    
    {current_policy_explanation}
        
    ### Now let's examine the same household with \$10k and \$15k in property taxes.
    """
    )

    # Get the higher property tax comparison table
    df_comparison = get_higher_property_tax_comparison(state_code, income_value)

    st.table(df_comparison.set_index("Scenario"))

    # Get effective SALT caps directly from TAX_CALCULATIONS
    tax_calcs = TAX_CALCULATIONS.get(state_code, TAX_CALCULATIONS["NY"]).get(
        income_value, TAX_CALCULATIONS["NY"][250000]
    )
    effective_caps = {
        "current_law": tax_calcs["effective_salt_cap"]["current_law"],
        "current_policy": tax_calcs["effective_salt_cap"]["current_policy"],
    }

    # Create formatted strings for the effective SALT caps
    current_law_cap_str = (
        "No effective SALT cap"
        if effective_caps["current_law"] == float("inf")
        else f"**${effective_caps['current_law']:,}**"
    )
    current_policy_cap_str = (
        "No effective SALT cap"
        if effective_caps["current_policy"] == float("inf")
        else f"**${effective_caps['current_policy']:,}**"
    )

    # Create finding for the higher property tax comparison
    higher_property_tax_finding = "The increased alternative minimum tax liability under current law offsets the effects of the lifted SALT cap, reducing the property tax subsidy rate as property taxes increase."

    st.markdown(
        f"""
    
    {higher_property_tax_finding}
    
    Any additional property taxes that are deducted under the SALT deduction for this household are partially taxed under the alternative minimum tax structure, creating an effective cap.
    
    ### The Effective SALT Cap for This Household Is:
    * {current_law_cap_str} under Current Law 
    * {current_policy_cap_str} under Current Policy 
    
    This demonstrates that even when the SALT cap officially expires, the AMT creates an effective cap for certain households.
    """
    )

    st.markdown(
        """
    ### Visualizing These Effects Across Different Property Tax Amounts
    
    The charts below show how tax liabilities and subsidy rates change as property taxes increase from \$0 to \$50k, helping us understand the broader implications of these policies.
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
            title=f"Tax Liability Comparison by Property Taxes ({selected_state}, {selected_income})",
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
        #### Tax Liability Chart
        This chart shows how regular tax and AMT change as property taxes increase. Where the dashed line (AMT) is above the solid line (regular tax), the household pays the AMT amount, limiting the benefit of SALT deductions.
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
            title=f"Property Tax Marginal Subsidy Rate ({selected_state}, {selected_income})",
            xaxis_title="Property Taxes ($)",
            yaxis_title="Subsidy Rate (%)",
            showlegend=True,
            template="simple_white",
            height=500,
        )

        st.markdown(
            """
        #### Subsidy Rate Chart
        This chart shows the percentage of each additional dollar of property tax that is effectively subsidized through tax savings.
        Some of the marginal subsidy rates reflect state level property tax related deductions and credits.
        """
        )

        st.plotly_chart(format_fig(fig3))
