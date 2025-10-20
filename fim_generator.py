"""
FIM Generator Module
Generates HAND-FIM flood depth maps from discharge data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class FIMGenerator:
    """Generate HAND-FIM flood depth maps"""
    
    # Depth classification ranges (FEMA standards)
    DEPTH_CLASSES = {
        1: {'name': 'Low', 'range': (0.0001, 0.4)},
        2: {'name': 'Moderate', 'range': (0.4, 0.8)},
        3: {'name': 'High', 'range': (0.8, 1.8)},
        4: {'name': 'Very High', 'range': (1.8, np.inf)}
    }
    
    def __init__(self, config):
        """Initialize FIM generator"""
        self.config = config
        self.huc_id = config['study_area']['huc_id']
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_depth_map(self, discharge_data):
        """
        Generate flood depth map from discharge data
        
        Args:
            discharge_data: DataFrame with feature_id and discharge
        
        Returns:
            pandas.DataFrame: Depth map data with classifications
        """
        print(f"  Generating HAND-FIM depth map...")
        
        # Generate depth values from discharge using HAND methodology
        # In production, this would use actual HAND-FIM inundation mapping tools
        depth_data = self._simulate_depth_from_discharge(discharge_data)
        
        if depth_data is not None:
            # Reclassify depths into severity levels
            reclassified = self._reclassify_depth(depth_data)
            self._save_depth_map(reclassified)
            return reclassified
        
        return None
    
    def _simulate_depth_from_discharge(self, discharge_data):
        """
        Simulate depth values from discharge using rating curves
        In production, uses HAND-FIM inundation mapping
        """
        # Apply simplified rating curve: depth ∝ discharge^0.4
        # This is a simplified relationship; real HAND-FIM uses hydraulic geometry
        
        depth_data = discharge_data.copy()
        depth_data['depth_m'] = (discharge_data['discharge'] / 50) ** 0.4
        
        # Clip to realistic maximum depth
        depth_data['depth_m'] = np.clip(depth_data['depth_m'], 0, 5)
        
        print(f"  Generated depths: max {depth_data['depth_m'].max():.2f}m, mean {depth_data['depth_m'].mean():.2f}m")
        
        return depth_data
    
    def _reclassify_depth(self, depth_data):
        """Reclassify depths into FEMA flood severity levels"""
        depth_data = depth_data.copy()
        
        # Assign severity class based on depth
        depth_data['severity_class'] = 0
        depth_data['severity_name'] = 'None'
        
        for class_id, class_info in self.DEPTH_CLASSES.items():
            min_depth, max_depth = class_info['range']
            mask = (depth_data['depth_m'] >= min_depth) & (depth_data['depth_m'] < max_depth)
            depth_data.loc[mask, 'severity_class'] = class_id
            depth_data.loc[mask, 'severity_name'] = class_info['name']
        
        # Count by severity
        severity_counts = depth_data['severity_name'].value_counts()
        print(f"  Severity distribution:")
        for severity, count in severity_counts.items():
            if severity != 'None':
                print(f"    {severity}: {count} reaches")
        
        return depth_data
    
    def _save_depth_map(self, df):
        """Save depth map data"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = self.output_dir / f"fim_depth_map_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"  Depth map saved to {filename}")
