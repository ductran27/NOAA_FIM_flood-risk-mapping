#!/usr/bin/env python3
"""
Flood Risk Impact Mapping - Main Workflow
Automated system for generating flood risk maps from NWM forecasts
"""

import sys
from datetime import datetime
from pathlib import Path
import yaml

from nwm_retriever import NWMRetriever
from fim_generator import FIMGenerator
from svi_processor import SVIProcessor
from risk_mapper import RiskMapper


def load_config():
    """Load configuration"""
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main FIM workflow execution"""
    print(f"=== Flood Risk Impact Mapping System ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Load configuration
        config = load_config()
        print(f"Configuration loaded")
        print(f"HUC ID: {config['study_area']['huc_id']}")
        
        # Initialize modules
        nwm_retriever = NWMRetriever(config)
        fim_generator = FIMGenerator(config)
        svi_processor = SVIProcessor(config)
        risk_mapper = RiskMapper(config)
        print(f"Modules initialized")
        
        # Step 1: Retrieve NWM streamflow data
        print(f"\n=== Step 1: Retrieving NWM Streamflow Data ===")
        max_discharge = nwm_retriever.get_max_discharge()
        if max_discharge is None:
            print("Failed to retrieve discharge data")
            return
        print(f"Max discharge retrieved for {len(max_discharge)} reaches")
        
        # Step 2: Generate HAND-FIM depth map
        print(f"\n=== Step 2: Generating HAND-FIM Depth Map ===")
        depth_map = fim_generator.generate_depth_map(max_discharge)
        if depth_map is None:
            print("Failed to generate depth map")
            return
        print(f"Depth map generated and reclassified")
        
        # Step 3: Process SVI data
        print(f"\n=== Step 3: Processing Social Vulnerability Index ===")
        svi_raster = svi_processor.create_svi_raster()
        if svi_raster is None:
            print("Failed to create SVI raster")
            return
        print(f"SVI raster created and aligned")
        
        # Step 4: Generate risk map
        print(f"\n=== Step 4: Generating Flood Risk Impact Map ===")
        risk_map = risk_mapper.generate_risk_map(depth_map, svi_raster)
        if risk_map is None:
            print("Failed to generate risk map")
            return
        print(f"Risk map successfully generated")
        
        # Summary statistics
        stats = risk_mapper.calculate_statistics(risk_map)
        print(f"\nRisk Map Statistics:")
        print(f"  Low Risk: {stats['low_risk_pct']:.1f}%")
        print(f"  Moderate Risk: {stats['moderate_risk_pct']:.1f}%")
        print(f"  High Risk: {stats['high_risk_pct']:.1f}%")
        print(f"  Very High Risk: {stats['very_high_risk_pct']:.1f}%")
        
        print(f"\n=== Workflow Complete ===")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Results saved in output/ and results/ directories")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
