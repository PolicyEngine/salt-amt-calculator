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

    **AMT:** Filers must calculate their tax liability under the regular tax code and the AMT, and pay the higher amount. The AMT disallows certain deductions, including the SALT deduction. The AMT exemption amount is indexed to inflation.
    
    ## How SALT and AMT affect a sample household
    
    Consider a married filer in Texas with:
    * $500,000 in employment income
    * $10,000 in deductible mortgage interest
    * $20,000 in charitable cash donations
    * $5,000 in property taxes

    Texas doesn't levy income taxes, but for SALT, the filer can claim their actual sales taxes or estimated from [IRS tables](https://www.irs.gov/instructions/i1040sca#en_US_2023_publink10005349). In this case, they can claim \$3,700. Overall, they can deduct $8,700 in SALT, both under current law and current policy.
    """
    )
    # Read the CSV files
    df = pd.read_csv("personal_calculator/data/tax_calculations_2026.csv")

    # Create SALT deduction plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["real_estate_taxes"],
            y=df["current_policy_salt_deduction"],
            mode="lines",
            name="Current Policy",
            line=dict(color=DARK_GRAY),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["real_estate_taxes"],
            y=df["current_law_salt_deduction"],
            mode="lines",
            name="Current Law",
            line=dict(color=BLUE),
        )
    )
    fig.update_layout(
        title="SALT Deduction by Property Taxes",
        xaxis_title="Property Taxes ($)",
        yaxis_title="SALT Deduction ($)",
        showlegend=True,
        template="simple_white",
        height=500,
    )

    st.plotly_chart(format_fig(fig))

    st.markdown(
        """
    ## What is the Alternative Minimum Tax (AMT)?

    The Alternative Minimum Tax (AMT) is a parallel tax system designed to ensure that high-income individuals, corporations, trusts, and estates pay a minimum level of federal taxes, even if they claim numerous deductions or credits under the regular tax system.                

    Based on this household’s specific composition, they will begin itemizing their deductions once their real estate taxes reach $8,000.

    However, at this level, the deduction will be added back under the Alternative Minimum Tax (AMT) and taxed at a rate of 26% or 28%.

    """
    )

    # Create AMT comparison plot
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df["real_estate_taxes"],
            y=df["current_policy_amt"],
            mode="lines",
            name="Current Policy",
            line=dict(color=DARK_GRAY),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=df["real_estate_taxes"],
            y=df["current_law_amt"],
            mode="lines",
            name="Current Law",
            line=dict(color=BLUE),
        )
    )
    fig2.update_layout(
        title="Alternative Minimum Tax by Property Taxes",
        xaxis_title="Property Taxes ($)",
        yaxis_title="Alternative Minimum Tax ($)",
        showlegend=True,
        template="simple_white",
        height=500,
    )

    st.plotly_chart(format_fig(fig2))

    st.markdown(
        """
    ## Current Property Tax Subsidy Rates

    One way to assess the impact of these tax policies is by examining how much of a household’s property taxes are offset by reductions in income tax liability:

    Under current policy, the household can deduct up to \$6,000 in property taxes before reaching the state and local tax (SALT) deduction cap. 
    This effectively provides a marginal subsidy rate of 33% on property taxes up to this limit.

    Under current law, if the SALT cap is removed, the household would be able to deduct property taxes exceeding the previous \$6,000 limit, allowing for greater tax savings.
    However, at $8,000 in real estate taxes, the SALT deduction is added back under the Alternative Minimum Tax (AMT), which can reduce the overall benefit of the deduction.

    This illustrates how tax policy changes—such as lifting the SALT cap—can impact the extent to which property taxes are deductible and how much tax relief a household receives.

    """
    )

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
