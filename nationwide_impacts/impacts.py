import pandas as pd
from pathlib import Path

class NationwideImpacts:
    def __init__(self):
        """Initialize nationwide impacts data loader"""
        self.data_dir = Path(__file__).parent / "data"
        self.single_year_impacts = self._load_data("single_year_impacts.csv")
        self.budget_window_impacts = self._load_data("budget_window_impacts.csv")
        
        # Get income column names
        if not self.single_year_impacts.empty:
            self.income_cols = [col for col in self.single_year_impacts.columns if col.startswith('income_p')]
        
    def _load_data(self, filename):
        """Load impact data"""
        try:
            return pd.read_csv(self.data_dir / filename)
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
            return pd.DataFrame()
    
    def get_available_reforms(self):
        """Get list of available reforms"""
        reforms = set()
        if not self.single_year_impacts.empty:
            reforms.update(self.single_year_impacts['reform'].unique())
        if not self.budget_window_impacts.empty:
            reforms.update(self.budget_window_impacts['reform'].unique())
        return sorted(list(reforms))
    
    def get_reform_impact(self, reform_name, impact_type="single_year"):
        """Get impact data for specific reform"""
        data = self.single_year_impacts if impact_type == "single_year" else self.budget_window_impacts
        if data.empty:
            return None
            
        return data[data['reform'] == reform_name].iloc[0] if not data[data['reform'] == reform_name].empty else None
    
    def get_income_distribution(self, reform_name):
        """Get income distribution impacts for a reform"""
        if self.single_year_impacts.empty or not self.income_cols:
            return None
            
        reform_data = self.single_year_impacts[self.single_year_impacts['reform'] == reform_name]
        if reform_data.empty:
            return None
            
        return reform_data[self.income_cols].iloc[0].rename(lambda x: x.replace('income_p', ''))
    
    def get_time_series(self, reform_name):
        """Get time series data for a reform"""
        if self.budget_window_impacts.empty:
            return None
            
        reform_data = self.budget_window_impacts[self.budget_window_impacts['reform'] == reform_name]
        if reform_data.empty:
            return None
            
        year_cols = [col for col in self.budget_window_impacts.columns if col.startswith('year_')]
        return reform_data[year_cols].iloc[0].rename(lambda x: int(x.replace('year_', '')))