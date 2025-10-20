"""
NWM Retriever Module
Retrieves National Water Model streamflow forecasts
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class NWMRetriever:
    """Retrieve and process NWM streamflow data"""
    
    def __init__(self, config):
        """Initialize NWM retriever"""
        self.config = config
        self.huc_id = config['study_area']['huc_id']
        self.forecast_range = config['nwm']['forecast_range']
        self.real_time_hour = config['nwm']['real_time_hour']
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
    
    def get_max_discharge(self):
        """
        Retrieve maximum discharge for all reaches in HUC
        
        Returns:
            pandas.DataFrame: Max discharge for each feature_id
        """
        print(f"  Retrieving NWM forecast data...")
        print(f"  HUC: {self.huc_id}, Range: {self.forecast_range}, Hour: {self.real_time_hour}")
        
        # Generate simulated discharge data
        # In production, this would download from AWS/Google Cloud
        discharge_data = self._generate_sample_discharge()
        
        if discharge_data is not None:
            self._save_discharge(discharge_data)
        
        return discharge_data
    
    def _generate_sample_discharge(self):
        """
        Generate sample NWM discharge data
        Simulates realistic streamflow forecasts
        """
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        
        # Generate reach IDs (feature_ids) for the HUC
        n_reaches = 150
        feature_ids = [f'{self.huc_id}{i:04d}' for i in range(n_reaches)]
        
        # Generate discharge values (m³/s)
        # Higher values for some reaches to simulate flood conditions
        base_discharge = np.random.lognormal(mean=2, sigma=1.5, size=n_reaches)
        
        # Add some high-flow reaches (flood conditions)
        flood_reaches = np.random.choice(n_reaches, size=15, replace=False)
        base_discharge[flood_reaches] *= np.random.uniform(3, 8, size=15)
        
        # Create DataFrame
        data = pd.DataFrame({
            'feature_id': feature_ids,
            'discharge': base_discharge
        })
        
        print(f"  Generated discharge data for {len(data)} reaches")
        print(f"  Max discharge: {data['discharge'].max():.2f} m³/s")
        
        return data
    
    def _save_discharge(self, df):
        """Save discharge data to CSV"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = self.data_dir / f"nwm_max_discharge_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"  Saved to {filename}")
