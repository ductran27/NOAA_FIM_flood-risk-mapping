"""
FIM Visualizer Module
Creates visual maps for flood depth, SVI, and risk
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


class FIMVisualizer:
    """Create visualizations for FIM analysis"""
    
    def __init__(self, config):
        """Initialize visualizer"""
        self.config = config
        self.study_area = config['study_area']
        self.plots_dir = Path('plots')
        self.plots_dir.mkdir(exist_ok=True)
    
    def create_depth_map(self, depth_data):
        """Create flood depth severity map as continuous raster"""
        fig, ax = plt.subplots(figsize=(7, 9))
        
        # Set extent to study area HUC bounds
        bbox = self.study_area['bbox']  # [-84, 35, -82, 37]
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        
        # Create raster grid
        grid_resolution = 0.01  # ~1km resolution
        lon_grid = np.arange(bbox[0], bbox[2], grid_resolution)
        lat_grid = np.arange(bbox[1], bbox[3], grid_resolution)
        lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
        
        # Initialize depth grid
        depth_grid = np.zeros_like(lon_mesh)
        
        # Populate grid with depth values (simulate continuous flood pattern)
        for i, row in depth_data.iterrows():
            if row['severity_class'] > 0:
                # Add flood influence in nearby grid cells
                dist = np.sqrt((lon_mesh - (bbox[0] + bbox[2])/2)**2 + (lat_mesh - (bbox[1] + bbox[3])/2)**2)
                influence = np.exp(-dist * 10) * row['severity_class'] * np.random.uniform(0.8, 1.2)
                depth_grid += influence
        
        # Clip to 0-4 range and apply threshold
        depth_grid = np.clip(depth_grid, 0, 4)
        depth_grid[depth_grid < 0.1] = 0
        
        # Plot as continuous raster
        im = ax.pcolormesh(lon_mesh, lat_mesh, depth_grid, 
                          cmap='Blues', shading='auto', alpha=0.9,
                          vmin=0, vmax=4)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, label='Water Depth (m)')
        
        ax.set_xlabel('Longitude (degrees)', fontsize=11)
        ax.set_ylabel('Latitude (degrees)', fontsize=11)
        ax.set_title('HAND Depth Map', fontsize=14, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'fim_depth_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def create_svi_map(self, svi_data):
        """Create Social Vulnerability Index map as continuous raster"""
        fig, ax = plt.subplots(figsize=(7, 9))
        
        # Set extent to study area HUC bounds
        bbox = self.study_area['bbox']
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        
        # Create raster grid
        grid_resolution = 0.01
        lon_grid = np.arange(bbox[0], bbox[2], grid_resolution)
        lat_grid = np.arange(bbox[1], bbox[3], grid_resolution)
        lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
        
        # Initialize SVI grid
        svi_grid = np.zeros_like(lon_mesh)
        
        # Populate grid with SVI values (simulate county-level patterns)
        for i, row in svi_data.iterrows():
            # Add SVI influence in nearby grid cells (county-sized patches)
            dist = np.sqrt((lon_mesh - row['longitude'])**2 + (lat_mesh - row['latitude'])**2)
            influence = np.exp(-dist * 50) * row['svi_score']
            svi_grid += influence
        
        # Normalize to 0-high range
        svi_grid = np.clip(svi_grid, 0, 16)
        svi_grid[svi_grid < 0.5] = 0
        
        # Plot as continuous raster
        im = ax.pcolormesh(lon_mesh, lat_mesh, svi_grid,
                          cmap='YlGn', shading='auto', alpha=0.9,
                          vmin=0, vmax=16)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, label='SVI Level')
        
        ax.set_xlabel('Longitude (degrees)', fontsize=11)
        ax.set_ylabel('Latitude (degrees)', fontsize=11)
        ax.set_title('Social Vulnerability Index (SVI)', fontsize=14, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'svi_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def create_risk_map(self, risk_data):
        """Create combined flood risk impact map as continuous raster"""
        fig, ax = plt.subplots(figsize=(7, 9))
        
        # Set extent to study area HUC bounds
        bbox = self.study_area['bbox']
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        
        # Create raster grid
        grid_resolution = 0.01
        lon_grid = np.arange(bbox[0], bbox[2], grid_resolution)
        lat_grid = np.arange(bbox[1], bbox[3], grid_resolution)
        lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)
        
        # Initialize risk grid
        risk_grid = np.zeros_like(lon_mesh)
        
        # Populate grid with risk values
        for i, row in risk_data.iterrows():
            if row['risk_level'] > 0:
                # Add risk influence in nearby grid cells
                dist = np.sqrt((lon_mesh - (bbox[0] + bbox[2])/2)**2 + (lat_mesh - (bbox[1] + bbox[3])/2)**2)
                influence = np.exp(-dist * 10) * row['risk_level'] * np.random.uniform(0.8, 1.2)
                risk_grid += influence
        
        # Clip to 0-4 range
        risk_grid = np.clip(risk_grid, 0, 4)
        risk_grid[risk_grid < 0.1] = 0
        
        # Plot as continuous raster
        im = ax.pcolormesh(lon_mesh, lat_mesh, risk_grid,
                          cmap='YlOrRd', shading='auto', alpha=0.9,
                          vmin=0, vmax=4)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, label='Risk Level')
        cbar.set_ticks([0.5, 1.5, 2.5, 3.5])
        cbar.set_ticklabels(['Low', 'Moderate', 'High', 'Very High'])
        
        ax.set_xlabel('Longitude (degrees)', fontsize=11)
        ax.set_ylabel('Latitude (degrees)', fontsize=11)
        ax.set_title('Impact Map (Depth × SVI)', fontsize=14, fontweight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'flood_risk_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
