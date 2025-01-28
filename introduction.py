import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from policyengine_core.charts import format_fig
from constants import LIGHT_GRAY, DARK_GRAY, BLUE


def display_introduction():
    st.markdown(
        """

    ## What is the SALT Deduction?

    The State and Local Tax (SALT) deduction allows taxpayers in the United States to deduct certain state and local taxes from their federal taxable income. These taxes can include:

    * State and local income taxes
    * Property taxes 
    * Sales taxes (as an alternative to income taxes in some cases)

    This deduction aims to reduce the impact of double taxation, as individuals are already paying taxes at the state and local levels.
    """
    )
    with st.expander("Show example household description"):
        st.markdown(
            """
            > We will show the respecitve impacts of the SALT deduction and the Alternative Minimum Tax (AMT) in 2026 on a married household in California with:
            > * Two children (both aged 10)
            > * $200,000 in capital gains
            > * $50,000 in real estate taxes
            """
        )

    # Read the CSV files
    df_2025 = pd.read_csv("personal_calculator/data/tax_calculations_2025.csv")
    df_2026 = pd.read_csv("personal_calculator/data/tax_calculations_2026.csv")

    # Create SALT deduction plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_2025["employment_income"],
            y=df_2025["salt_deduction"],
            mode="lines",
            name="Current Policy",
            line=dict(color=DARK_GRAY),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_2026["employment_income"],
            y=df_2026["salt_deduction"],
            mode="lines",
            name="Current Law",
            line=dict(color=BLUE),
        )
    )
    fig.update_layout(
        title="SALT Deduction by Employment Income",
        xaxis_title="Employment Income ($)",
        yaxis_title="SALT Deduction ($)",
        xaxis_range=[0, 200_000],
        yaxis_range=[0, 20_000],
        showlegend=True,
        template="simple_white",
        height=500,
    )

    st.plotly_chart(format_fig(fig))

    st.markdown(
        """
    ## What is the Alternative Minimum Tax (AMT)?

    The Alternative Minimum Tax (AMT) is a parallel tax system designed to ensure that high-income individuals, corporations, trusts, and estates pay a minimum level of federal taxes, even if they claim numerous deductions or credits under the regular tax system.                

    The AMT operates by following these steps:

    * Calculate Regular Taxable Income: Determine your taxable income under the regular federal tax system, taking into account all applicable deductions and credits.

    * Adjust for AMT Preferences: Add back specific deductions and tax-preference items that are not allowed under the AMT system. These include:
        * State and local taxes (SALT deduction)
        * Certain miscellaneous itemized deductions
        * Incentive stock option profits
        * Depreciation adjustments on property

    * Determine Alternative Minimum Taxable Income (AMTI): After adding back the disallowed items, calculate your AMTI.

    * Apply the AMT Exemption: Subtract the AMT exemption amount from your AMTI. The exemption amount is phased out for higher-income taxpayers.

    * Calculate AMT Liability: Apply the AMT tax rates (26% and 28%, depending on your income level) to the AMTI above the exemption threshold.

    * Compare with Regular Tax Liability: Compare the AMT liability with your regular federal tax liability. If the AMT amount is higher, you must pay the AMT.
    """
    )

    # Create AMT comparison plot
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df_2025["employment_income"],
            y=df_2025["alternative_minimum_tax"],
            mode="lines",
            name="Current Policy",
            line=dict(color=DARK_GRAY),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=df_2026["employment_income"],
            y=df_2026["alternative_minimum_tax"],
            mode="lines",
            name="Current Law",
            line=dict(color=BLUE),
        )
    )
    fig2.update_layout(
        title="Alternative Minimum Tax by Employment Income",
        xaxis_title="Employment Income ($)",
        yaxis_title="Alternative Minimum Tax ($)",
        showlegend=True,
        template="simple_white",
        height=500,
    )

    st.plotly_chart(format_fig(fig2))

    st.markdown(
        """
    ## Current Real Estate Tax Subsidy Rates

    The subsidy rate represents how much the federal government effectively subsidizes real estate taxes through various provisions. 
    """
    )
    with st.expander("Show example household description"):
        st.markdown(
            """
    > For the marginal subsidy rate computation in 2026, the example household is a married couple in Texas with:
    > * Two children (both aged 10)
    > * $100,000 in capital gains
    > * $200,000 in employment income
    > * $30,000 in medical expenses
    > * $20,000 in charitable cash donations

    """
        )

    # Add subsidy rates plot for both years
    df_subsidy = pd.read_csv("personal_calculator/data/subsidy_rates.csv")

    # Filter data for 2025 and 2026
    df_2025 = df_subsidy[df_subsidy["Year"] == 2025]
    df_2026 = df_subsidy[df_subsidy["Year"] == 2026]

    # Create the plot
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=df_2025["Real Estate Taxes"],
            y=df_2025["Subsidy Rate (%)"],
            mode="lines",
            name="Current Policy",
            line=dict(color=DARK_GRAY),
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=df_2026["Real Estate Taxes"],
            y=df_2026["Subsidy Rate (%)"],
            mode="lines",
            name="Current Law",
            line=dict(color=BLUE),
        )
    )
    fig3.update_layout(
        title="Real Estate Tax Marginal Subsidy Rate",
        xaxis_title="Real Estate Taxes ($)",
        yaxis_title="Subsidy Rate (%)",
        showlegend=True,
        template="simple_white",
        height=500,
    )

    # Display the plot in Streamlit
    st.plotly_chart(format_fig(fig3))
