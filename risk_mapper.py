"""
Risk Mapper Module
Generates flood risk maps by combining depth and SVI data
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime


class RiskMapper:
    """Generate flood risk impact maps"""
    
    # Risk level definitions
    RISK_LEVELS = {
        1: 'Low Risk',
        2: 'Moderate Risk',
        3: 'High Risk',
        4: 'Very High Risk'
    }
    
    def __init__(self, config):
        """Initialize risk mapper"""
        self.config = config
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
        self.results_dir = Path('results')
        self.results_dir.mkdir(exist_ok=True)
    
    def generate_risk_map(self, depth_data, svi_data):
        """
        Generate risk map by combining flood depth and social vulnerability
        
        Args:
            depth_data: DataFrame with depth classifications
            svi_data: DataFrame with SVI scores
        
        Returns:
            pandas.DataFrame: Combined risk map
        """
        print(f"  Combining depth and SVI data...")
        
        # Simulate spatial join by matching based on proximity
        # In production, this would use actual raster algebra
        risk_data = self._combine_depth_and_svi(depth_data, svi_data)
        
        if risk_data is not None:
            self._save_risk_map(risk_data)
            return risk_data
        
        return None
    
    def _combine_depth_and_svi(self, depth_data, svi_data):
        """
        Combine flood depth and SVI to calculate risk
        Risk = Depth Severity × SVI Score
        """
        # Sample locations that overlap with flooded reaches
        flooded_reaches = depth_data[depth_data['severity_class'] > 0]
        
        risk_data = []
        
        # For each flooded reach, combine with SVI data
        for idx, reach in flooded_reaches.iterrows():
            # Simulate coupling: higher depth severity × higher SVI = higher risk
            coupled_value = reach['severity_class'] * np.random.choice(svi_data['svi_score'])
            
            risk_data.append({
                'feature_id': reach['feature_id'],
                'depth_m': reach['depth_m'],
                'depth_severity': reach['severity_name'],
                'coupled_risk_value': coupled_value,
                'risk_level': 0  # Will be assigned next
            })
        
        risk_df = pd.DataFrame(risk_data)
        
        # Classify into risk levels using quantiles
        risk_df = self._classify_risk_levels(risk_df)
        
        print(f"  Generated risk map for {len(risk_df)} locations")
        
        return risk_df
    
    def _classify_risk_levels(self, risk_df):
        """Classify coupled risk values into quantile-based levels"""
        valid_values = risk_df[risk_df['coupled_risk_value'] > 0]['coupled_risk_value']
        
        if len(valid_values) > 0:
            quantiles = np.quantile(valid_values, [0.25, 0.50, 0.75])
            
            risk_df['risk_level'] = np.digitize(
                risk_df['coupled_risk_value'], 
                bins=quantiles, 
                right=True
            ) + 1
            
            risk_df['risk_level'] = np.clip(risk_df['risk_level'], 1, 4)
            risk_df['risk_name'] = risk_df['risk_level'].map(self.RISK_LEVELS)
        
        return risk_df
    
    def calculate_statistics(self, risk_df):
        """Calculate statistics for risk map"""
        total = len(risk_df)
        
        stats = {
            'total_locations': total,
            'low_risk_count': len(risk_df[risk_df['risk_level'] == 1]),
            'moderate_risk_count': len(risk_df[risk_df['risk_level'] == 2]),
            'high_risk_count': len(risk_df[risk_df['risk_level'] == 3]),
            'very_high_risk_count': len(risk_df[risk_df['risk_level'] == 4])
        }
        
        stats['low_risk_pct'] = (stats['low_risk_count'] / total) * 100
        stats['moderate_risk_pct'] = (stats['moderate_risk_count'] / total) * 100
        stats['high_risk_pct'] = (stats['high_risk_count'] / total) * 100
        stats['very_high_risk_pct'] = (stats['very_high_risk_count'] / total) * 100
        
        # Save statistics
        self._save_statistics(stats)
        
        return stats
    
    def _save_risk_map(self, df):
        """Save risk map data"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = self.output_dir / f"flood_risk_map_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"  Risk map saved to {filename}")
    
    def _save_statistics(self, stats):
        """Save statistics to JSON"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = self.results_dir / f"risk_statistics_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"  Statistics saved to {filename}")
