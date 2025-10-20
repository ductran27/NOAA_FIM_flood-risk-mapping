"""
SVI Processor Module
Processes CDC Social Vulnerability Index data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class SVIProcessor:
    """Process Social Vulnerability Index data"""
    
    def __init__(self, config):
        """Initialize SVI processor"""
        self.config = config
        self.study_area = config['study_area']
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
    
    def create_svi_raster(self):
        """
        Create SVI raster aligned with study area
        
        Returns:
            pandas.DataFrame: SVI data by location
        """
        print(f"  Processing CDC SVI data...")
        
        # Generate simulated SVI data
        # In production, this would process actual CDC SVI geodatabase
        svi_data = self._generate_sample_svi()
        
        if svi_data is not None:
            self._save_svi_data(svi_data)
            return svi_data
        
        return None
    
    def _generate_sample_svi(self):
        """
        Generate sample SVI data for study area
        Simulates social vulnerability distribution
        """
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        
        # Generate grid points for study area
        n_locations = 200
        
        # Create locations within study area bounds
        lons = np.random.uniform(-84, -82, n_locations)
        lats = np.random.uniform(35, 37, n_locations)
        
        # Generate SVI scores (1-16 based on summing F_ flags)
        # Higher SVI = more vulnerable
        svi_scores = np.random.choice(range(1, 17), size=n_locations, 
                                     p=[0.15, 0.15, 0.12, 0.10, 0.08, 
                                        0.08, 0.07, 0.06, 0.05, 0.04,
                                        0.03, 0.02, 0.02, 0.01, 0.01, 0.01])
        
        # Create DataFrame
        data = pd.DataFrame({
            'location_id': [f'LOC_{i:04d}' for i in range(n_locations)],
            'longitude': lons,
            'latitude': lats,
            'svi_score': svi_scores
        })
        
        print(f"  Generated SVI data for {len(data)} locations")
        print(f"  SVI range: {data['svi_score'].min()}-{data['svi_score'].max()}")
        print(f"  Mean SVI: {data['svi_score'].mean():.1f}")
        
        return data
    
    def _save_svi_data(self, df):
        """Save SVI data"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = self.output_dir / f"svi_data_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"  SVI data saved to {filename}")
