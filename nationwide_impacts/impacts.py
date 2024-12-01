import pandas as pd
from pathlib import Path

class NationwideImpacts:
    def __init__(self):
        """Initialize nationwide impacts data loader"""
        self.data_dir = Path(__file__).parent / "data"
        self.single_year_impacts = self._load_data("single_year_impacts.csv")
        self.budget_window_impacts = self._load_data("budget_window_impacts_temporary.csv")
        
        # Parse available options from reform names when data is loaded
        if not self.single_year_impacts.empty:
            self.filter_options = self._parse_reform_options()
            self.income_cols = [col for col in self.single_year_impacts.columns 
                              if col.startswith('income_p')]
        
    def _load_data(self, filename):
        """Load impact data with error handling for malformed CSV files"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"Warning: File not found: {filename}")
            return pd.DataFrame()
        
        try:
            # Explicitly list all numeric columns from the CSV
            numeric_cols = [
                'revenue_impact', 'poverty_impact', 'inequality_impact',
                'pct_better_off', 'pct_worse_off'
            ] + [f'income_p{i:02d}_{i+10}' for i in range(0, 100, 10)]
            
            return pd.read_csv(
                filepath,
                on_bad_lines='skip',
                dtype={col: float for col in numeric_cols}
            )
        except Exception as e:
            print(f"Warning: Error loading {filename}: {str(e)}")
            return pd.DataFrame()
    
    def _parse_reform_options(self):
        """Parse reform names to extract filter options."""
        # Get unique reform names from the data
        reform_names = self.single_year_impacts['reform'].unique() if 'reform' in self.single_year_impacts.columns else []
        
        filter_options = {
            'amt_type': set(),
            'tcja_status': set(),
            'behavioral_response': set()
        }
        
        for reform in reform_names:
            if not isinstance(reform, str):
                continue
            
            parts = reform.split('_')
            
            # Skip if this isn't a SALT reform
            if 'salt' not in parts:
                continue
            
            try:
                salt_idx = parts.index('salt')
                
                # Extract AMT type
                amt_parts = []
                for part in parts[salt_idx+1:]:
                    if part in ['amt', 'repealed', 'extended', 'behavioral', 'responses']:
                        break
                    amt_parts.append(part)
                if amt_parts:
                    filter_options['amt_type'].add('_'.join(amt_parts))
                
                # Extract TCJA status
                if 'tcja' in parts:
                    tcja_status = None
                    if 'extended' in parts:
                        tcja_status = 'extended'
                    elif 'repealed' in parts:
                        tcja_status = 'repealed'
                    if tcja_status:
                        filter_options['tcja_status'].add(tcja_status)
                
                # Extract behavioral response
                if 'behavioral' in parts:
                    response = 'yes' if parts[parts.index('behavioral')+2] == 'yes' else 'no'
                    filter_options['behavioral_response'].add(response)
                    
            except (ValueError, IndexError):
                # Skip reforms we can't parse
                continue
        
        return filter_options



    def filter_reforms(self, tcja=None, salt_cap=None, salt_phase_out=None, 
                      amt_exemptions=None, amt_phase_out=None, behavioral=None):
        """Filter reforms based on selected options"""
        df = self.single_year_impacts.copy()
        
        if df.empty:
            return df
            
        mask = pd.Series(True, index=df.index)
        
        if tcja is not None:
            mask &= df['reform'].str.contains('extended' if tcja == 'extended' else 'repealed')
            
        if salt_cap is not None:
            mask &= df['reform'].str.contains(f'salt_{salt_cap}_')
            
        if salt_phase_out is not None:
            mask &= df['reform'].str.contains(salt_phase_out)
            
        if amt_exemptions is not None:
            mask &= df['reform'].str.contains(f'amt_{amt_exemptions}_')
            
        if amt_phase_out is not None:
            mask &= df['reform'].str.contains(amt_phase_out)
            
        if behavioral is not None:
            mask &= df['reform'].str.contains('yes' if behavioral == 'yes' else 'no')
            
        return df[mask]

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
        """Get time series data for a specific reform."""
        # Check if data is loaded
        if self.budget_window_impacts is None or self.budget_window_impacts.empty:
            return None
        
        # Ensure 'reform' column exists
        if 'reform' not in self.budget_window_impacts.columns:
            print("Available columns:", self.budget_window_impacts.columns)  # Debug info
            return None
        
        # Get reform data
        reform_data = self.budget_window_impacts[self.budget_window_impacts['reform'] == reform_name]
        
        if reform_data.empty:
            return None
        
        return reform_data
    
    def get_filter_options(self):
        """Get all available filter options"""
        if not hasattr(self, 'filter_options'):
            return {}
        return self.filter_options