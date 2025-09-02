# Chicago Air Quality Analysis Report (2000–2002)
#### By Zarrar Malik for UChicago Programming Supplement

## Summary
This analysis examines PM2.5, PM10, O3, and NO2 in Chicago (2000–2002). Visualizations and statistics are saved as PNGs.

## Data Overview
- Period: 2000-01-01 to 2002-12-31
- Days analyzed: 1096

## Data availability
- PM25: 1094 days (99.8% coverage)
- PM10: 1094 days (99.8% coverage)
- O3: 1096 days (100.0% coverage)
- NO2: 1096 days (100.0% coverage)

## Peak concentrations (Top 5 days by pollutant)
### PM25
- 2001-01-22: 49.47
- 2001-02-07: 47.50
- 2001-03-03: 47.40
- 2000-04-19: 46.70
- 2001-01-23: 45.70

### PM10
- 2001-05-03: 97.50
- 2001-11-14: 95.00
- 2002-07-03: 95.00
- 2001-10-31: 92.50
- 2002-07-17: 91.50

### O3
- 2000-06-09: 55.76
- 2002-06-23: 54.88
- 2002-06-24: 54.45
- 2001-06-13: 51.82
- 2002-06-09: 51.72

### NO2
- 2000-03-31: 50.81
- 2001-03-03: 48.72
- 2002-12-11: 47.76
- 2000-01-28: 47.25
- 2002-09-09: 45.26

## Trend test (Kendall tau) for PM2.5
- Observations: 1096
- Kendall tau: -0.074
- p-value: 0.000
- Interpretation: statistically significant monotonic trend detected (p < 0.05)

## Notes & Methods
- Missing daily values were interpolated for decomposition/visualization only (limit=7 days). All such decisions are documented.
- Seasonal decomposition (additive) was attempted for PM2.5 to separate trend/seasonality/residuals.

## Files generated
- pollutants_timeseries_zarrar.png
- monthly_pm25_distribution_zarrar.png
- monthly_boxplot_pm25_zarrar.png
- seasonal_analysis_zarrar.png

---
*Report generated with Python by Zarrar Malik*
