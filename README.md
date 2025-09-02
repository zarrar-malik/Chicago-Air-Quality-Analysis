# Chicago Air Quality Analysis (2000-2002)

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-red.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **A comprehensive statistical analysis of air pollution trends in Chicago from 2000-2002, featuring advanced visualizations and time series decomposition.**

*Created by Zarrar Malik for UChicago Programming Supplement*

## 🎯 Project Overview

This project provides an in-depth analysis of Chicago's air quality during the early 2000s, examining four key pollutants: **PM2.5**, **PM10**, **Ozone (O3)**, and **Nitrogen Dioxide (NO2)**. The analysis combines robust statistical methods with compelling visualizations to uncover pollution patterns, seasonal trends, and long-term changes.

### 🔍 Key Features

- **Multi-pollutant Time Series Analysis** - Comprehensive tracking of four major air pollutants
- **Advanced Statistical Testing** - Kendall's tau correlation for trend detection
- **Beautiful Visualizations** - Custom-styled plots with professional aesthetics
- **Seasonal Decomposition** - Separates trend, seasonal, and residual components
- **Automated Reporting** - Generates detailed markdown reports
- **Joy Plots** - Elegant monthly distribution visualizations

## 📊 Sample Visualizations

The analysis generates four main visualization types:

1. **Multi-Panel Time Series** - Shows pollutant concentrations over time with 30-day rolling averages
2. **Joy Plots** - Monthly PM2.5 distribution patterns using plasma colormap
3. **Seasonal Analysis** - Grouped bar charts comparing pollutant levels across seasons
4. **Box Plots** - Monthly concentration distributions for detailed statistical insights

## Tech Stack

```python
# Core Libraries
pandas>=1.3.0          # Data manipulation and analysis
numpy>=1.21.0           # Numerical computing
matplotlib>=3.4.0       # Plotting and visualization
seaborn>=0.11.0         # Statistical data visualization

# Specialized Libraries  
scipy>=1.7.0            # Statistical functions (Kendall's tau)
statsmodels>=0.12.0     # Time series decomposition
joypy>=0.2.4           # Joy plot generation
```

## Quick Start

### Prerequisites

Make sure you have Python 3.7+ installed, then install the required packages:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels joypy
```

### Expected Input Format

Your CSV should contain columns similar to:
```csv
date,pm25tmean2,pm10tmean2,o3tmean2,no2tmean2
2000-01-01,15.2,25.8,0.025,18.5
2000-01-02,12.8,22.1,0.031,16.2
...
```

## Output Files

The analysis generates several output files:

| File | Description |
|------|-------------|
| `pollutants_timeseries_zarrar.png` | Multi-panel time series with trend lines |
| `monthly_pm25_distribution_zarrar.png` | Joy plot of monthly PM2.5 distributions |
| `seasonal_analysis_zarrar.png` | Seasonal comparison bar chart |
| `monthly_boxplot_pm25_zarrar.png` | Monthly boxplot analysis |
| `chicago_air_quality_report_zarrar.md` | Comprehensive markdown report |

## Analysis Features

### Statistical Methods
- **Kendall's Tau Test** - Non-parametric trend detection
- **Seasonal Decomposition** - Additive model separating trend/seasonal/residual components
- **Data Availability Assessment** - Coverage statistics for each pollutant
- **Peak Detection** - Identification of top 5 concentration events

### Data Processing
- **Intelligent Column Detection** - Automatically identifies date and pollutant columns
- **Flexible Date Parsing** - Handles various date formats
- **Missing Data Handling** - Limited interpolation with full documentation
- **Year Filtering** - Focuses analysis on 2000-2002 period

### Visualization Design
- **Custom Color Palette** - Professional styling with consistent branding
- **Interactive Elements** - Peak annotations and trend overlays
- **Multiple Chart Types** - Time series, distributions, seasonal comparisons
- **High-Resolution Output** - 300 DPI publication-ready graphics

## 📈 Sample Results

The analysis typically reveals:
- **Seasonal Patterns** - Higher PM2.5 concentrations in winter months
- **Long-term Trends** - Potential decreasing or increasing trends over the study period
- **Peak Events** - Identification of extreme pollution episodes
- **Data Quality** - Coverage statistics showing data completeness

## Customization

### Modifying Time Period
```python
# Change the analysis period
air = load_and_preprocess_data(INPUT_CSV, start_year=2000, end_year=2005)
```

### Custom Styling
```python
# Modify the color palette in set_custom_style()
colors = {
    'pm25': '#YOUR_COLOR',
    'pm10': '#YOUR_COLOR',
    # ... etc
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Zarrar Malik**

*This analysis demonstrates advanced Python skills in data science, statistical analysis, and scientific visualization - perfect for academic and professional applications.*
