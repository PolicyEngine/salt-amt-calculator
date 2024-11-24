import streamlit as st
import pandas as pd

class ImpactTables:
    @staticmethod
    def display_summary_metrics(impact_data, impact_type):
        """Display summary metrics based on impact type"""
        # All metrics in one row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Revenue Impact",
                f"${impact_data['revenue_impact']/1e9:.1f}B",
                help="Change in federal revenue"
            )
        
        with col2:
            st.metric(
                "Households Better Off",
                f"{impact_data['pct_better_off']*100:.1f}%",
                help="Percentage of households with increased net income"
            )
        
        with col3:
            st.metric(
                "Households Worse Off",
                f"{impact_data['pct_worse_off']*100:.1f}%",
                help="Percentage of households with decreased net income"
            )
        
        with col4:
            st.metric(
                "Poverty Impact",
                f"{impact_data['poverty_impact']*100:+.1f}pp",
                help="Change in poverty rate (percent)"
            )
        
        with col5:
            st.metric(
                "Inequality Impact",
                f"{impact_data['inequality_impact']*100:+.1f}%",
                help="Change in Gini coefficient (percent)"
            )