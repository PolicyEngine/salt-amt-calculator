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
    * Sales taxes

    """
    )
    with st.expander("Show example household description"):
        st.markdown(
            """
            > We will show the respecitve impacts of the SALT deduction and the Alternative Minimum Tax (AMT) in 2026 on a married household in Texas with:
            > * $500,000 in employment income
            > * $10,000 in deductible mortgage interest
            > * $20,000 in charitable cash donation
            """
        )
    st.markdown(
        """
    For this household, the state and local tax (SALT) deduction is calculated as follows:

    Under current law, the married couple pays \$3,700 in sales taxes, which they can fully deduct because it falls within the allowable SALT deduction limit.
    If the household starts paying property taxes, they can deduct an additional $5,300, but only up to the current SALT deduction cap.
    
    Under current law, the SALT deduction cap is lifted, which allows the household to fully deduct all of their property taxes without limitation.

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
        title="SALT Deduction by Employment Income",
        xaxis_title="Employment Income ($)",
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
