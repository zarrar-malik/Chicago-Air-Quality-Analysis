"""
Chicago Air Quality Analysis (2000-2002)
Author: Zarrar Malik
Date: 2025-08-30
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import warnings
from scipy.stats import kendalltau
from statsmodels.tsa.seasonal import seasonal_decompose
import joypy
import seaborn as sns

warnings.filterwarnings("ignore")
np.random.seed(42)

# Config / filenames
INPUT_CSV = "chicago_air_pollution.csv"   
OUT_TIMESERIES = "pollutants_timeseries_zarrar.png"
OUT_JOYPLOT = "monthly_pm25_distribution_zarrar.png"
OUT_SEASONAL = "seasonal_analysis_zarrar.png"
OUT_BOX = "monthly_boxplot_pm25_zarrar.png"
OUT_REPORT = "chicago_air_quality_report_zarrar.md"

# style
def set_custom_style():
    sns.set_style("whitegrid")  # Using seaborns whitegrid theme 
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.facecolor'] = '#F8F9FA'
    plt.rcParams['figure.facecolor'] = '#F8F9FA'
    plt.rcParams['grid.alpha'] = 0.25
    colors = {
        'pm25': '#E63946',
        'pm10': '#457B9D',
        'o3': '#FCA311',
        'no2': '#588157',
        'background': '#F8F9FA',
        'text': '#343A40',
        'dark_pm25': '#A62633',
        'dark_pm10': '#315B79',
        'dark_o3': '#C5820E',
        'dark_no2': '#406545'
    }
    return colors

# loading and preprocessor
def find_date_column(df):
    """Find a likely date column (case-insensitive)."""
    candidates = [c for c in df.columns if c.lower() in ('date', 'datetime', 'time', 'day')]
    if candidates:
        return candidates[0]
    # fallback: try columns that look like dates by dtype
    for c in df.columns:
        if np.issubdtype(df[c].dtype, np.datetime64):
            return c
    return None

def find_pollutant_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    # try case-insensitive match
    low = {col.lower(): col for col in df.columns}
    for c in candidates:
        if c.lower() in low:
            return low[c.lower()]
    return None

def load_and_preprocess_data(path=INPUT_CSV, start_year=2000, end_year=2002):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input CSV not found: {path}")

    # read without enforcing parse_dates (will detect)
    df = pd.read_csv(path, low_memory=False)

    # detect date column and parse it
    date_col = find_date_column(df)
    if date_col is None:
        raise ValueError("No date column found in the input CSV. Please include a date column named 'date' or similar.")
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce', infer_datetime_format=True)
    df = df.dropna(subset=[date_col])
    df = df.rename(columns={date_col: 'date'})

    # filter years
    df = df[(df['date'].dt.year >= start_year) & (df['date'].dt.year <= end_year)]

    # find pollutant columns with fallbacks
    pm25_col = find_pollutant_column(df, ['pm25tmean2', 'pm25', 'PM2.5', 'pm25_mean'])
    pm10_col = find_pollutant_column(df, ['pm10tmean2', 'pm10', 'PM10'])
    o3_col   = find_pollutant_column(df, ['o3tmean2', 'o3', 'O3'])
    no2_col  = find_pollutant_column(df, ['no2tmean2', 'no2', 'NO2'])

    # create a DataFrame, fill missing columns with NaN
    air = pd.DataFrame({'date': df['date']})
    air['pm25'] = df[pm25_col] if pm25_col in df.columns else np.nan
    air['pm10'] = df[pm10_col] if pm10_col in df.columns else np.nan
    air['o3']   = df[o3_col]   if o3_col   in df.columns else np.nan
    air['no2']  = df[no2_col]  if no2_col  in df.columns else np.nan

    # report what columns were used
    used = {
        'pm25': pm25_col, 'pm10': pm10_col, 'o3': o3_col, 'no2': no2_col
    }
    print("Detected pollutant columns:", used)
    return air

# stats
def data_availability_report(air):
    n_total = len(air)
    report = {}
    for col in ['pm25','pm10','o3','no2']:
        count = int(air[col].count())
        report[col] = {'count': count, 'pct': 100 * count / max(1, n_total)}
    return report

def trend_test_kendall(series):
    # series: pandas Series indexed by date or int; must drop NaNs
    s = series.dropna().reset_index(drop=True)
    if len(s) < 8:
        return {'tau': np.nan, 'p': np.nan, 'n': len(s)}
    tau, p = kendalltau(np.arange(len(s)), s.values)
    return {'tau': float(tau), 'p': float(p), 'n': len(s)}

# Visualizations
def create_visualizations(air, colors):
    pollutants = ['pm25','pm10','o3','no2']
    titles = ['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'Ozone (ppm)', 'Nitrogen Dioxide (ppb)']
    darks = [colors['dark_pm25'], colors['dark_pm10'], colors['dark_o3'], colors['dark_no2']]
    cols = [colors['pm25'], colors['pm10'], colors['o3'], colors['no2']]

    # ensure date is datetime
    air['date'] = pd.to_datetime(air['date'])
    air = air.sort_values('date').reset_index(drop=True)

    # Multi-panel time series
    fig, axes = plt.subplots(2,2, figsize=(16,12))
    fig.suptitle('Chicago Air Quality (2000–2002) — Zarrar Malik', fontsize=20, weight='bold', color=colors['text'])
    for i, (poll, title, color, dark) in enumerate(zip(pollutants, titles, cols, darks)):
        ax = axes[i//2, i%2]
        ax.plot(air['date'], air[poll], color=color, alpha=0.6, linewidth=1)
        # 30-day rolling trend
        trend = air.set_index('date')[poll].rolling(window=30, min_periods=10).mean()
        ax.plot(trend.index, trend.values, color=dark, linewidth=2.2, label='30-day trend')
        # annotate top 5 peaks
        if air[poll].dropna().size > 0:
            top5 = air.nlargest(5, poll)[['date',poll]]
            for _, row in top5.iterrows():
                ax.scatter(row['date'], row[poll], color='k', s=20)
                ax.annotate(int(round(row[poll],0)), (row['date'], row[poll]),
                            textcoords="offset points", xytext=(0,6), ha='center', fontsize=8)
        ax.set_title(title)
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=3))
        ax.grid(True, alpha=0.25)
        ax.legend()
        ax.set_facecolor(colors['background'])
        ax.text(0.02, 0.95, 'Zarrar Malik', transform=ax.transAxes, fontsize=8, alpha=0.25)

    plt.tight_layout(rect=[0,0,1,0.95])
    plt.savefig(OUT_TIMESERIES, dpi=300, bbox_inches='tight', facecolor=colors['background'])
    plt.close()
    print(f"Saved: {OUT_TIMESERIES}")

    # Joyplot (monthly distributions) — PM2.5 only
    air['month'] = air['date'].dt.month
    air['month_name'] = air['date'].dt.strftime('%b')
    # Ensure month ordering
    month_order = [calendar.month_abbr[i] for i in range(1,13)]
    air['month_name'] = pd.Categorical(air['month_name'], categories=month_order, ordered=True)

    fig, axes = joypy.joyplot(air, by='month_name', column='pm25',
                              colormap=plt.cm.plasma, overlap=1.8, linewidth=1.2,
                              fade=True, figsize=(12,10))
    plt.title('Monthly Distribution of PM2.5 (2000–2002) — Zarrar Malik', fontsize=16)
    plt.xlabel('PM2.5 (µg/m³)')
    plt.savefig(OUT_JOYPLOT, dpi=300, bbox_inches='tight', facecolor=colors['background'])
    plt.close()
    print(f"Saved: {OUT_JOYPLOT}")

    # Boxplot of PM2.5 by month for a different viewpoint
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    air.boxplot(column='pm25', by='month_name', ax=ax, grid=False)
    plt.suptitle('')
    plt.title('Monthly PM2.5 Boxplot (2000–2002)')
    plt.xlabel('')
    plt.ylabel('PM2.5 (µg/m³)')
    plt.xticks(rotation=45)
    plt.savefig(OUT_BOX, dpi=300, bbox_inches='tight', facecolor=colors['background'])
    plt.close()
    print(f"Saved: {OUT_BOX}")

    # Seasonal grouped bar chart
    season_map = {12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',
                  6:'Summer',7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall'}
    air['season'] = air['date'].dt.month.map(season_map)
    seasonal_avg = air.groupby('season')[pollutants].mean().reindex(['Winter','Spring','Summer','Fall'])
    # Plot grouped bars
    fig, ax = plt.subplots(figsize=(12,8))
    x = np.arange(len(seasonal_avg.index))
    width = 0.2
    for i, poll in enumerate(pollutants):
        ax.bar(x + i*width, seasonal_avg[poll], width, label=poll.upper())
    ax.set_xticks(x + width*1.5)
    ax.set_xticklabels(seasonal_avg.index)
    ax.set_ylabel('Avg concentration')
    ax.set_title('Seasonal Averages by Pollutant (2000–2002)')
    ax.legend()
    plt.savefig(OUT_SEASONAL, dpi=300, bbox_inches='tight', facecolor=colors['background'])
    plt.close()
    print(f"Saved: {OUT_SEASONAL}")

# Decomposition and trend test
def decomposition_and_trend(air):
    out = {}
    # pm25 (daily series)
    pm25 = air.set_index('date')['pm25'].dropna()
    if pm25.empty:
        return {'decomp': None, 'trend_test': None}
    # resample to daily full index (fills gaps with NaN)
    pm25_daily = pm25.resample('D').mean()
    # simple interpolation (advisory: document this)
    pm25_daily_interp = pm25_daily.interpolate(limit=7)
    # seasonal_decompose requires at least two seasons; for daily data, period ~365
    try:
        decomposition = seasonal_decompose(pm25_daily_interp, model='additive', period=365, extrapolate_trend='freq')
        out['decomp'] = decomposition
    except Exception:
        out['decomp'] = None
    # trend test (Kendall)
    tt = trend_test_kendall(pm25_daily_interp.dropna())
    out['trend_test'] = tt
    return out

# Report generation
def generate_report(air, availability, decomp_res):
    # header
    md = "# Chicago Air Quality Analysis Report (2000–2002)\n"
    md += "#### By Zarrar Malik for UChicago Programming Supplement\n\n"
    md += "## Summary\nThis analysis examines PM2.5, PM10, O3, and NO2 in Chicago (2000–2002). Visualizations and statistics are saved as PNGs.\n\n"

    md += "## Data Overview\n"
    md += f"- Period: {air['date'].min().date()} to {air['date'].max().date()}\n"
    md += f"- Days analyzed: {len(air)}\n\n"
    md += "## Data availability\n"
    for k, v in availability.items():
        md += f"- {k.upper()}: {v['count']} days ({v['pct']:.1f}% coverage)\n"
    md += "\n"

    md += "## Peak concentrations (Top 5 days by pollutant)\n"
    for poll in ['pm25','pm10','o3','no2']:
        if air[poll].dropna().empty:
            continue
        top5 = air.nlargest(5, poll)[['date', poll]]
        md += f"### {poll.upper()}\n"
        for _, r in top5.iterrows():
            md += f"- {r['date'].date()}: {r[poll]:.2f}\n"
        md += "\n"

    # trend test
    md += "## Trend test (Kendall tau) for PM2.5\n"
    tt = decomp_res.get('trend_test') if decomp_res else None
    if tt:
        md += f"- Observations: {tt['n']}\n"
        md += f"- Kendall tau: {tt['tau']:.3f}\n"
        md += f"- p-value: {tt['p']:.3f}\n"
        if not np.isnan(tt['p']) and tt['p'] < 0.05:
            md += "- Interpretation: statistically significant monotonic trend detected (p < 0.05)\n\n"
        else:
            md += "- Interpretation: no statistically significant monotonic trend detected (p >= 0.05)\n\n"
    else:
        md += "- Not enough data for trend testing.\n\n"

    md += "## Notes & Methods\n"
    md += "- Missing daily values were interpolated for decomposition/visualization only (limit=7 days). All such decisions are documented.\n"
    md += "- Seasonal decomposition (additive) was attempted for PM2.5 to separate trend/seasonality/residuals.\n\n"
    md += "## Files generated\n"
    md += f"- {OUT_TIMESERIES}\n- {OUT_JOYPLOT}\n- {OUT_BOX}\n- {OUT_SEASONAL}\n\n"
    md += "---\n*Report generated with Python by Zarrar Malik*\n"

    with open(OUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Saved: {OUT_REPORT}")

def main():
    print("Chicago Air Quality Analysis (2000–2002) — Created By: Zarrar Malik")
    colors = set_custom_style()
    air = load_and_preprocess_data(INPUT_CSV)
    print(f"Loaded {len(air)} rows: {air['date'].min().date()} to {air['date'].max().date()}\n")

    availability = data_availability_report(air)
    for k,v in availability.items():
        print(f"{k.upper():5s}: {v['count']:4d} days ({v['pct']:.1f}%)")

    # Visualizations
    create_visualizations(air, colors)

    # Trend and decomposition
    decomp_res = decomposition_and_trend(air)

    # Report
    generate_report(air, availability, decomp_res)

    print("\nDone. Generated files:")
    print(f" - {OUT_TIMESERIES}")
    print(f" - {OUT_JOYPLOT}")
    print(f" - {OUT_BOX}")
    print(f" - {OUT_SEASONAL}")
    print(f" - {OUT_REPORT}")

if __name__ == "__main__":
    main()
