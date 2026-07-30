import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.makedirs("reports", exist_ok=True)
os.makedirs("output", exist_ok=True)

db_path = os.path.join("data", "financial_analytics.db")
conn = sqlite3.connect(db_path)

# Load full tables
companies = pd.read_sql_query("SELECT * FROM companies", conn)

# Standardize company identifier column safely
for col in ['id', 'ticker', 'symbol', 'company_id']:
    if col in companies.columns:
        companies.rename(columns={col: 'company_id'}, inplace=True)
        break

companies = companies.loc[:, ~companies.columns.duplicated()]

if 'broad_sector' not in companies.columns:
    if 'sector' in companies.columns:
        companies.rename(columns={'sector': 'broad_sector'}, inplace=True)
    else:
        companies['broad_sector'] = 'General'

# Load ratios if table exists
try:
    ratios = pd.read_sql_query("SELECT * FROM financial_ratios", conn)
    for col in ['id', 'ticker', 'symbol', 'company_id']:
        if col in ratios.columns:
            ratios.rename(columns={col: 'company_id'}, inplace=True)
            break
    ratios = ratios.loc[:, ~ratios.columns.duplicated()]
    
    if 'year' in ratios.columns:
        ratios = ratios.sort_values('year').groupby('company_id').last().reset_index()
except Exception:
    ratios = pd.DataFrame({'company_id': companies['company_id']})

conn.close()

# Force company_id to string type to avoid merge errors
companies['company_id'] = companies['company_id'].astype(str)
ratios['company_id'] = ratios['company_id'].astype(str)

# Merge tables
df = pd.merge(companies, ratios, on='company_id', how='left', suffixes=('', '_ratios'))
df = df.loc[:, ~df.columns.duplicated()]

def find_col(df_cols, targets):
    for t in targets:
        for c in df_cols:
            if t in c.lower():
                return c
    return None

col_map = {
    'roe_pct': ['roe', 'return_on_equity'],
    'roce_pct': ['roce', 'return_on_capital'],
    'debt_to_equity': ['debt_to_equity', 'de_ratio', 'd_e'],
    'interest_coverage_ratio': ['interest_coverage', 'icr'],
    'operating_profit_margin_pct': ['operating_profit_margin', 'opm', 'operating_margin'],
    'net_profit_margin_pct': ['net_profit_margin', 'npm', 'net_margin'],
    'revenue_cagr_5yr': ['revenue_cagr', 'rev_cagr'],
    'pat_cagr_5yr': ['pat_cagr'],
    'fcf_cagr_5yr': ['fcf_cagr', 'fcf'],
    'cfo_to_pat_ratio': ['cfo_to_pat', 'cfo_pat', 'cfo']
}

kpi_cols = list(col_map.keys())

for feat, keywords in col_map.items():
    found = find_col(df.columns, keywords)
    if found:
        df[feat] = pd.to_numeric(df[found], errors='coerce')
    else:
        df[feat] = np.nan

# Impute NaNs with sector median, fallback to global median
for col in kpi_cols:
    df[col] = df.groupby('broad_sector')[col].transform(lambda x: x.fillna(x.median()))
    df[col] = df[col].fillna(df[col].median()).fillna(0)

# 1. Pearson Correlation Heatmap
plt.figure(figsize=(10, 8))
corr = df[kpi_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, square=True)
plt.title('Pearson Correlation Heatmap of Core KPIs')
plt.tight_layout()
plt.savefig(os.path.join("reports", "correlation_heatmap.png"), dpi=300)
plt.close()
print("Generated reports/correlation_heatmap.png")

# 2. Outlier Detection (Z-score > 3 per broad_sector)
outliers = []
for sector, group in df.groupby('broad_sector'):
    for col in kpi_cols:
        vals = group[col].dropna()
        if len(vals) > 2 and vals.std() > 0:
            z_scores = (group[col] - vals.mean()) / vals.std()
            outlier_rows = group[abs(z_scores) > 3]
            for idx, row in outlier_rows.iterrows():
                outliers.append({
                    'company_id': row['company_id'],
                    'broad_sector': sector,
                    'metric': col,
                    'value': row[col],
                    'z_score': round(z_scores.loc[idx], 2)
                })

outlier_df = pd.DataFrame(outliers)
outlier_df.to_csv(os.path.join("output", "outlier_report.csv"), index=False)
print(f"Generated output/outlier_report.csv ({len(outlier_df)} outliers flagged)")

# 3. Portfolio Percentile Stats Table
stats_list = []
for col in kpi_cols:
    s = df[col].dropna()
    if not s.empty:
        stats_list.append({
            'kpi': col,
            'P10': round(s.quantile(0.10), 2),
            'P25': round(s.quantile(0.25), 2),
            'P50': round(s.quantile(0.50), 2),
            'P75': round(s.quantile(0.75), 2),
            'P90': round(s.quantile(0.90), 2),
            'Mean': round(s.mean(), 2),
            'Std': round(s.std(), 2)
        })

stats_df = pd.DataFrame(stats_list)
stats_df.to_csv(os.path.join("output", "portfolio_stats.csv"), index=False)
print("Generated output/portfolio_stats.csv")