# Flood Risk Impact Mapping System

Automated flood risk assessment system combining NOAA National Water Model forecasts, HAND-FIM flood depth mapping, and Social Vulnerability Index to generate comprehensive flood risk impact maps.

## Overview

This system integrates hydrological forecasting, flood inundation modeling, and social vulnerability analysis to identify areas at highest risk during flood events. The workflow processes real-time streamflow data through HAND-FIM methodology and combines it with social vulnerability data to produce actionable risk maps for emergency management.

## Methodology

### 1. Hydrological Data Retrieval
- Retrieves reach IDs from AWS S3 (CIROH HAND-FIM data)
- Downloads National Water Model forecasts from Google Cloud
- Extracts maximum discharge for each stream reach

### 2. Flood Inundation Mapping
- Applies Height Above Nearest Drainage (HAND) methodology
- Generates flood depth maps using NOAA-OWP inundation mapping tools
- Classifies flood severity into 4 levels (Low, Moderate, High, Very High)

### 3. Social Vulnerability Mapping
- Processes CDC Social Vulnerability Index data
- Rasterizes SVI at 10m resolution
- Aligns with flood depth maps

### 4. Risk Map Generation
- Combines flood depth and social vulnerability
- Produces quantile-based risk classification
- Identifies high-priority areas for emergency response

## Data Sources

- **National Water Model**: NOAA real-time streamflow forecasts
- **HAND-FIM**: NOAA-OWP Height Above Nearest Drainage
- **SVI**: CDC Social Vulnerability Index geodatabases

## Applications

- Emergency response planning
- Evacuation priority mapping
- Resource allocation for disaster response
- Community resilience assessment
- Flood impact forecasting

## Outputs

Generated products:
- Flood depth maps (reclassified by severity)
- Social vulnerability rasters
- Combined flood risk impact maps
- Statistical summaries

## Learning Resources

**Want to learn more about operational flood forecasting and HAND-FIM methodology?**

Complete course available at:
**https://edx.hydrolearn.org/courses/course-v1:CIROH_HydroLearn+OP_040+2025/about**

This HydroLearn course covers:
- NOAA National Water Model operations
- HAND-FIM flood inundation mapping
- Real-time flood forecasting workflows
- Emergency management applications

## Notes

Integrates multiple federal datasets (NOAA, CDC) for comprehensive flood risk assessment. Focuses on actionable information for emergency managers and disaster response teams.

Based on methodologies taught in CIROH HydroLearn operational flood forecasting course.
