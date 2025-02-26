import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, BLUE


def display_introduction():
    st.markdown(
        """
    ## SALT and AMT Basics

    **SALT:** Filers can take an itemized deduction for (a) property taxes and (b) _either_ state and local income taxes or sales taxes. The TCJA capped the SALT deduction at \$10,000 from 2018 to 2025; beginning next year, it will be uncapped.

    **AMT:** Filers must calculate their tax liability under the regular tax code and the AMT and pay the higher amount. The AMT disallows certain deductions, including the SALT deduction. The TCJA has (1) expanded the exemption amount that applies to AMT-specific income and (2) increased the threshold at which this exemption phases out at a rate of 25%.
    
    ## What We'll Demonstrate

    In this analysis, we'll show how the interaction between SALT deductions and AMT creates an **effective SALT cap** even when the explicit SALT cap expires in 2026 (current law). We'll demonstrate that while the SALT cap is officially removed in 2026, the AMT effectively limits how much property tax high-income households can deduct, creating a de facto cap that's different from the explicit \$10,000 cap under current policy (2025).
    
    We'll examine this through:
    1. A detailed case study of an upper-middle-class household
    2. Analysis of property tax subsidy rates (how much tax relief households get per dollar of property tax)
    3. Visualization of these effects across different property tax amounts
    
    ## How SALT and AMT Affect a Sample Household
    
    ### SALT Deduction

    Consider a married filer in Texas with:
    * \$400,000 in wages and salaries 
    * \$15,000 in deductible mortgage interest 
    * \$10,000 in charitable cash donations 
    * One child aged 10

    """
    )

    # Add comparison table
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$8,672", "$8,672"],
        "$10k property taxes": ["$13,672", "$10,000"],
        "Difference": ["$5,000", "$1,328"],
    }
    df_comparison = pd.DataFrame(comparison_data)

    st.markdown(
        """
    #### SALT Deduction Amount by Scenario
    The table below shows how much of the property taxes as well as sales taxes can be deducted under each scenario:
    """
    )

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    Texas doesn't levy income taxes, but for SALT, the filer can claim either their actual sales taxes or an estimated amount based on [IRS tables](https://www.irs.gov/instructions/i1040sca#en_US_2023_publink10005349). 
    In this case, they can claim \$3,672 in sales taxes. 
    
    Under current law (2026), the entire amount of property taxes plus sales taxes is deductible. Under current policy (2025), this amount is subject to the SALT deduction cap of \$10,000, limiting the total deduction.
    """
    )

    st.markdown(
        """
    ### Regular Tax Liability
    The increased SALT deduction under current law will lower the household's taxable income, which in turn results in lower regular tax liabilities. The table below shows the regular tax liability (before considering AMT) for each scenario:
    """
    )
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$83,334", "$73,281"],
        "$10k property taxes": ["$81,684", "$73,035"],
        "Difference": ["-1,650", "-$246"],
    }
    df_comparison = pd.DataFrame(comparison_data)

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    ### Alternative Minimum Tax (AMT)

    The alternative minimum tax (AMT) begins with the regular taxable income and then makes specific adjustments to compute an alternative taxable income. For filers taking the standard deduction, that amount is simply used. However, for filers who itemize, only the SALT deduction—and a few other select items that are excluded from regular taxable income—is added back. This adjusted income is then reduced by an exemption amount, which phases out for higher levels of AMT income, before a tax rate of either 26% or 28% is applied to determine the **tentative minimum tax**. (Additional rules may apply for households with capital gains and dividend income.)
    
    The table below shows the tentative minimum tax for each scenario:
    """
    )

    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$80,982", "$61,139"],
        "$10k property taxes": ["$80,982", "$61,139"],
        "Difference": ["$0", "$0"],
    }
    df_comparison = pd.DataFrame(comparison_data)

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

    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$5k property taxes": [
            "$8,672",
            "$8,672",
            "$83,334",
            "$73,281",
            "$80,982",
            "$61,139",
            "$83,334",
            "$73,281",
        ],
        "$10k property taxes": [
            "$13,672",
            "$10,000",
            "$81,684",
            "$73,035",
            "$80,982",
            "$61,139",
            "$81,684",
            "$73,035",
        ],
        "Difference": [
            "$5,000",
            "$1,328",
            "-$1,650",
            "-$246",
            "$0",
            "$0",
            "-$1,650",
            "-$246",
        ],
        "Property Tax Subsidy Rate": ["-", "-", "-", "-", "-", "-", "33%", "5%"],
    }
    df_comparison = pd.DataFrame(comparison_data)

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    **Key Insight:** Under both current law and current policy, the regular tax liability exceeds the tentative minimum tax. The AMT does not apply in either scenario, allows the household to take full advantage of the SALT deduction under current law.
        
    ### Now let's examine the same household with \$10k and \$15k in property taxes.
    """
    )

    # Add comparison table
    comparison_data = {
        "Scenario": [
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
            "Current law",
            "Current policy",
        ],
        "Quantity": [
            "SALT deduction",
            "SALT deduction",
            "Regular Tax Liability",
            "Regular Tax Liability",
            "Tentative Minimum Tax",
            "Tentative Minimum Tax",
            "Federal Income Tax",
            "Federal Income Tax",
        ],
        "$10k property taxes": [
            "$13,672",
            "$10,000",
            "$81,684",
            "$73,035",
            "$80,982",
            "$61,139",
            "$81,684",
            "$73,035",
        ],
        "$15k property taxes": [
            "$18,672",
            "$10,000",
            "$80,034",
            "$73,035",
            "$80,982",
            "$61,139",
            "$80,982",
            "$73,035",
        ],
        "Difference": ["$5,000", "$0", "-$1,650", "$0", "$0", "$0", "-$702", "$0"],
        "Subsidy Rate": ["-", "-", "-", "-", "-", "-", "14%", "0%"],
    }

    df_comparison = pd.DataFrame(comparison_data)

    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    **Key Finding:** The increased alternative minimum tax liability under current law offsets the effects of the lifted SALT cap, reducing the property tax subsidy rate from 33% to 14% as property taxes increase.
    
    Any additional property taxes that are deducted under the SALT deduction for this household are partially taxed under the alternative minimum tax structure, creating an effective cap.
    
    ### The Effective SALT Cap for This Household Is:
    * **\$15,775 under Current Law** (due to the AMT)
    * **\$10,000 under Current Policy** (due to the explicit SALT deduction cap)
    
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
        df = pd.read_csv("personal_calculator/data/tax_calculations_2026_new.csv")

        # Create tax liability comparison plot
        fig2 = go.Figure()
        # Current Policy traces
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_policy_regular_tax_before_credits"],
                mode="lines",
                name="Current Policy Regular Tax",
                line=dict(color=DARK_GRAY, dash="solid"),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_policy_tentative_minimum_tax"],
                mode="lines",
                name="Current Policy Tentative AMT",
                line=dict(color=DARK_GRAY, dash="dash"),
            )
        )
        # Current Law traces
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_law_regular_tax_before_credits"],
                mode="lines",
                name="Current Law Regular Tax",
                line=dict(color=BLUE, dash="solid"),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=df["real_estate_taxes"],
                y=df["current_law_tentative_minimum_tax"],
                mode="lines",
                name="Current Law Tentative AMT",
                line=dict(color=BLUE, dash="dash"),
            )
        )
        fig2.update_layout(
            title="Tax Liability Comparison by Property Taxes",
            xaxis_title="Property Taxes ($)",
            yaxis_title="Tax Liability ($)",
            showlegend=True,
            template="simple_white",
            height=500,
        )

        st.markdown(
            """
        #### Tax Liability Chart
        This chart shows how regular tax and AMT change as property taxes increase. Where the dashed line (AMT) is above the solid line (regular tax), the household pays the AMT amount, limiting the benefit of SALT deductions.
        """
        )

        st.plotly_chart(format_fig(fig2))

        # Add subsidy rates plot for both years
        df_subsidy = pd.read_csv("personal_calculator/data/subsidy_rates.csv")

        # Filter data for 2025 and 2026
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
            title="Property Tax Marginal Subsidy Rate",
            xaxis_title="Property Taxes ($)",
            yaxis_title="Subsidy Rate (%)",
            showlegend=True,
            template="simple_white",
            height=500,
        )

        st.markdown(
            """
        #### Subsidy Rate Chart
        This chart shows the percentage of each additional dollar of property tax that is effectively subsidized through tax savings. The declining subsidy rate under current law demonstrates how the AMT creates an effective cap on SALT deductions.
        """
        )

        st.plotly_chart(format_fig(fig3))

        st.markdown(
            """
        These charts confirm our key finding: even when the explicit SALT cap expires in 2026, the AMT creates an effective cap that limits the tax benefits of property tax deductions for high-income households.
        """
        )
