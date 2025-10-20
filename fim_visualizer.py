"""
FIM Visualizer Module
Creates visual maps for flood depth, SVI, and risk
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from pathlib import Path
import cartopy.crs as ccrs
import cartopy.feature as cfeature


class FIMVisualizer:
    """Create visualizations for FIM analysis"""
    
    def __init__(self, config):
        """Initialize visualizer"""
        self.config = config
        self.study_area = config['study_area']
        self.plots_dir = Path('plots')
        self.plots_dir.mkdir(exist_ok=True)
    
    def create_depth_map(self, depth_data):
        """Create flood depth severity map"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        
        # Set extent to study area
        bbox = self.study_area['bbox']
        ax.set_extent(bbox, crs=ccrs.PlateCarree())
        
        # Add geographic features
        ax.add_feature(cfeature.LAND, facecolor='#F5F5DC', alpha=0.3)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#333333')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#666666', alpha=0.7)
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='#888888', alpha=0.5)
        ax.add_feature(cfeature.RIVERS, edgecolor='blue', linewidth=0.5, alpha=0.6)
        
        # Plot flood depth by severity
        colors = {
            'Low': '#FFFF00',
            'Moderate': '#FFA500', 
            'High': '#FF4500',
            'Very High': '#8B0000'
        }
        
        for severity, color in colors.items():
            data = depth_data[depth_data['severity_name'] == severity]
            if len(data) > 0:
                # Simulate spatial distribution
                lons = np.random.uniform(bbox[0], bbox[2], len(data))
                lats = np.random.uniform(bbox[1], bbox[3], len(data))
                ax.scatter(lons, lats, c=color, s=100, alpha=0.7,
                          edgecolors='black', linewidth=0.5,
                          transform=ccrs.PlateCarree(), label=severity)
        
        ax.set_title(f'HAND-FIM Flood Depth Map\n{self.study_area["name"]} - HUC {self.study_area["huc_id"]}',
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', framealpha=0.95, fontsize=11, title='Flood Severity')
        
        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.top_labels = False
        gl.right_labels = False
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'fim_depth_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def create_svi_map(self, svi_data):
        """Create Social Vulnerability Index map"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        
        # Set extent to study area
        bbox = self.study_area['bbox']
        ax.set_extent(bbox, crs=ccrs.PlateCarree())
        
        # Add geographic features
        ax.add_feature(cfeature.LAND, facecolor='#F5F5DC', alpha=0.3)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#333333')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#666666', alpha=0.7)
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='#888888', alpha=0.5)
        
        # Plot SVI scores
        scatter = ax.scatter(svi_data['longitude'], svi_data['latitude'],
                           c=svi_data['svi_score'], s=80, cmap='YlOrRd',
                           alpha=0.7, edgecolors='black', linewidth=0.5,
                           transform=ccrs.PlateCarree(), vmin=1, vmax=16)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='SVI Score', shrink=0.7)
        cbar.ax.text(0.5, 0.02, 'Less Vulnerable', transform=cbar.ax.transAxes,
                    ha='center', fontsize=9)
        cbar.ax.text(0.5, 0.98, 'More Vulnerable', transform=cbar.ax.transAxes,
                    ha='center', va='top', fontsize=9)
        
        ax.set_title(f'Social Vulnerability Index (SVI)\n{self.study_area["name"]} - CDC SVI 2022',
                    fontsize=16, fontweight='bold', pad=20)
        
        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.top_labels = False
        gl.right_labels = False
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'svi_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
    
    def create_risk_map(self, risk_data):
        """Create combined flood risk impact map"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        
        # Set extent to study area
        bbox = self.study_area['bbox']
        ax.set_extent(bbox, crs=ccrs.PlateCarree())
        
        # Add geographic features
        ax.add_feature(cfeature.LAND, facecolor='#F5F5DC', alpha=0.3)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8, edgecolor='#333333')
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='#666666', alpha=0.7)
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='#888888', alpha=0.5)
        ax.add_feature(cfeature.RIVERS, edgecolor='blue', linewidth=0.5, alpha=0.6)
        
        # Plot risk levels with distinct colors
        colors = {
            'Low Risk': '#90EE90',
            'Moderate Risk': '#FFD700',
            'High Risk': '#FF8C00',
            'Very High Risk': '#DC143C'
        }
        
        for risk_level, color in colors.items():
            data = risk_data[risk_data['risk_name'] == risk_level]
            if len(data) > 0:
                # Simulate spatial distribution
                lons = np.random.uniform(bbox[0], bbox[2], len(data))
                lats = np.random.uniform(bbox[1], bbox[3], len(data))
                ax.scatter(lons, lats, c=color, s=120, alpha=0.75,
                          edgecolors='black', linewidth=0.8,
                          transform=ccrs.PlateCarree(), label=risk_level)
        
        ax.set_title(f'Flood Risk Impact Map\n{self.study_area["name"]} - Combining Flood Depth & Social Vulnerability',
                    fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', framealpha=0.95, fontsize=11, title='Risk Level')
        
        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.top_labels = False
        gl.right_labels = False
        
        # Add info box
        stats_text = f"HUC: {self.study_area['huc_id']}\n"
        stats_text += f"Total Locations: {len(risk_data)}\n"
        stats_text += f"High/Very High Risk: {len(risk_data[risk_data['risk_level'] >= 3])}"
        ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
                fontsize=10, verticalalignment='bottom',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                         edgecolor='darkred', alpha=0.95, linewidth=2))
        
        plt.tight_layout()
        
        filepath = self.plots_dir / 'flood_risk_map.png'
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return filepath
