import streamlit as st
import plotly.graph_objects as go
from nationwide_impacts.impacts import NationwideImpacts

class BaselineImpacts:
    def __init__(self):
        self.impacts = NationwideImpacts()
        
    def get_baseline_data(self, baseline_type="current_law"):
        """Get time series data for either current law or current policy"""
        if baseline_type == "current_law":
            reform_name = "salt_uncapped_amt_tcja_both_tcja_repealed_behavioral_responses_yes"
        else:  # current policy
            reform_name = "salt_tcja_base_amt_tcja_both_tcja_repealed_behavioral_responses_yes"
            
        return self.impacts.get_time_series(reform_name)
    
    def create_metric_chart(self, current_law_data, current_policy_data, metric):
        """Create a line chart comparing current law and policy for a given metric"""
        fig = go.Figure()
        
        # Add current law line
        fig.add_trace(go.Scatter(
            x=current_law_data['year'],
            y=current_law_data[metric],
            name='Current Law',
            line=dict(color='blue')
        ))
        
        # Add current policy line
        fig.add_trace(go.Scatter(
            x=current_policy_data['year'],
            y=current_policy_data[metric],
            name='Current Policy (TCJA)',
            line=dict(color='red')
        ))
        
        # Update layout
        fig.update_layout(
            title=f"{metric.replace('_', ' ').title()} Over Time",
            xaxis_title="Year",
            yaxis_title=metric.replace('_', ' ').title(),
            hovermode='x unified'
        )
        
        return fig

def display_baseline_impacts():
    """Main function to display baseline impacts section"""
    st.markdown("## Baseline Policy Impacts (2026-2035)")
    
    # Initialize baseline impacts
    if 'baseline_impacts' not in st.session_state:
        with st.spinner("Loading baseline data..."):
            st.session_state.baseline_impacts = BaselineImpacts()
    
    # Get data
    current_law_data = st.session_state.baseline_impacts.get_baseline_data("current_law")
    current_policy_data = st.session_state.baseline_impacts.get_baseline_data("current_policy")
    
    if current_law_data is not None and current_policy_data is not None:
        # Metric selector
        available_metrics = ['revenue', 'poverty_rate', 'gini_coefficient']
        selected_metric = st.selectbox(
            "Select Metric",
            available_metrics,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        # Create and display chart
        fig = st.session_state.baseline_impacts.create_metric_chart(
            current_law_data,
            current_policy_data,
            selected_metric
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation
        st.markdown("""
        This chart shows the projected impacts of Current Law (pre-TCJA) and 
        Current Policy (TCJA provisions) over the 10-year budget window from 2026-2035.
        """)
    else:
        st.error("Unable to load baseline impact data")
