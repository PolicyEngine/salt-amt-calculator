import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import DARK_GRAY, BLUE


def display_introduction():
    st.markdown(
        """
    ## SALT and AMT basics

    **SALT:** Filers can take an itemized deduction for (a) property taxes, and (b) _either_ state and local income taxes, or sales taxes. TCJA capped the SALT deduction at \$10,000 from 2018 to 2025; beginning next year, it will be uncapped.

    **AMT:** Filers must calculate their tax liability under the regular tax code and the AMT, and pay the higher amount. The AMT disallows certain deductions, including the SALT deduction. TCJA has (1) expanded the exemption amount which applies to the AMT specific income and (2) increased the threshold at which this exemption is being phased-out at a 25% rate.
    
    ## How SALT and AMT affect a sample household
    
    ### SALT Deduction

    Consider a married filer in Texas with:
    * $500,000 in employment income
    * $15,000 in deductible mortgage interest
    * $10,000 in charitable cash donations

    """
    )

    # Add comparison table
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$8,672", "$8,672"],
        "$10k property taxes": ["$13,672", "$10,000"],
        "Difference": ["$5,000", "$1,328"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    st.table(df_comparison.set_index("Scenario"))
    
    st.markdown(
        """
    Texas doesn't levy income taxes, but for SALT, the filer can claim their actual sales taxes or estimated from [IRS tables](https://www.irs.gov/instructions/i1040sca#en_US_2023_publink10005349). 
    In this case, they can claim \$3,672. 
    
    Under current law and current policy the entire \$5,000 in property taxes is deductible. Under current policy, this amount is subject to the SALT deduction cap of \$10,000. Allowing for a maximum property tax deduction of $6,328.


    """
    )

    st.markdown(
        """
    ### Regular Tax Liability
    The increased SALT deduction will lower the household's taxable income, which in turn results in lower regular tax liabilities.
    """
    )  
    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$116,272", "$102,453"],
        "$10k property taxes": ["$114,622", "$102,028"],
        "Difference": ["-$1,650", "-$425"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    st.table(df_comparison.set_index("Scenario"))



    st.markdown(
        """
    ### Alternative Minimum Tax (AMT)

    The alternative minimum tax (AMT) is computed by adding the standard or the SALT deduction to the filer's taxable income, depending on the itemization choice. The first $243,800 of AMT specific income, which is reduced by the exemption amount, is taxed at a 26% rate. The remaining amount is taxed at a 28% rate, with specific taxation rules applying for households with capital gains and dividend income.
    This is used to compute the tentative minimum tax.

    """
    )

    comparison_data = {
        "Scenario": ["Current law", "Current policy"],
        "$5k property taxes": ["$115,066", "$88,966"],
        "$10k property taxes": ["$115,066", "$88,966"],
        "Difference": ["$0", "$0"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    
    The excess of the tentative minimum tax over the regular tax liability is added back to compute the AMT liability. 
    

    Under current policy, since the SALT deduction is subject to the cap, not reducing tax liability enough to trigger the AMT.
    """
    )
    
    st.markdown(
        """
    ### Current Property Tax Subsidy Rates

    One way to assess the impact of these tax policies is by examining how much of a household's property taxes are offset by reductions in income tax liability:


    This illustrates how tax policy changes—such as lifting the SALT cap—can impact the extent to which property taxes are deductible and how much tax relief a household receives. high

    """
    )

    comparison_data = {
        "Scenario": ["Current law", "Current policy", "Current law", "Current policy", "Current law", "Current policy", "Current law", "Current policy"],
        "Quantity": ["SALT deduction", "SALT deduction", "Regular Tax Liability", "Regular Tax Liability", "Tentative Minimum Tax", "Tentative Minimum Tax", "Federal Income Tax", "Federal Income Tax"],
        "$5k property taxes": ["$8,672", "$8,672", "$116,272", "$102,453", "$115,066", "$88,966", "$116,272", "$102,453"],
        "$10k property taxes": ["$13,672", "$10,000", "$114,622", "$102,028", "$115,066", "$88,966", "$115,066", "$102,028"],
        "Difference": ["$5,000", "$1,328", "-$1,650", "-$425", "$0", "$0", "-$1,206", "-$425"],
        "Property Tax Subsidy Rate": ["-", "-", "-", "-", "-", "-", "24%", "8%"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    st.table(df_comparison.set_index("Scenario"))

    st.markdown(
        """
    ### Now let's examine the same household with \$10k and $15k in property taxes.
    """
    )

    # Add comparison table
    comparison_data = {
        "Scenario": ["Current law", "Current policy", "Current law", "Current policy", "Current law", "Current policy", "Current law", "Current policy"],
        "Quantity": ["SALT deduction", "SALT deduction", "Regular Tax Liability", "Regular Tax Liability", "Tentative Minimum Tax", "Tentative Minimum Tax", "Federal Income Tax", "Federal Income Tax"],
        "$10k property taxes": ["$13,672", "$10,000", "$114,622", "$102,028", "$115,066", "$88,966", "$115,066", "$102,028"],
        "$15k property taxes": ["$18,672", "$10,000", "$112,972", "$102,028", "$115,066", "$88,966", "$115,066", "$102,028"],
        "Difference": ["$5,000", "$0", "-$1,650", "$0", "$0", "$0", "$0", "$0"],
        "Subsidy Rate": ["-", "-", "-", "-", "-", "-", "0%", "0%"]
    }

    df_comparison = pd.DataFrame(comparison_data)
    
    st.table(df_comparison.set_index("Scenario"))



    st.markdown(
        """
    The increased Alternative Minimum Tax liability under current law offsets the effects of the lifted SALT cap, making the property tax subsidy rate neutral.

    Any property taxes that are deducted under the SALT deduction for this hosuehold are fully taxed under the Alternative Minimum Tax.

    ### The Effective SALT cap for this household under Current Law is \$12,184 and $10,000 under Current Policy.
    
    """
    )


    st.markdown(
        """
    ### We can also look at the SALT deduction, AMT and the Property Tax Subsidy Rate over the a property tax range of 0 to $50k.
    """
    )
    # Read the CSV files
    with st.expander("See detailed tax calculations"):
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

        # Display the plot in Streamlit
        st.plotly_chart(format_fig(fig3))
