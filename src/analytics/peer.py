import os
import sqlite3
import numpy as np
import pandas as pd

def calculate_peer_percentiles(data_df: pd.DataFrame, peer_groups_path="data/peer_groups.xlsx", db_path="db/financials.db", current_year=2026):
    if not os.path.exists(peer_groups_path):
        return "No peer group assigned"
        
    try:
        peer_df = pd.read_excel(peer_groups_path)
    except Exception:
        return "No peer group assigned"
        
    if 'company_id' not in peer_df.columns or 'peer_group_name' not in peer_df.columns:
        return "No peer group assigned"
        
    merged_df = pd.merge(data_df, peer_df[['company_id', 'peer_group_name']], on='company_id', how='left')
    
    unassigned = merged_df[merged_df['peer_group_name'].isna() | (merged_df['peer_group_name'] == '')]
    assigned_df = merged_df[merged_df['peer_group_name'].notna() & (merged_df['peer_group_name'] != '')].copy()
    
    metrics_to_rank = [
        'roe', 'roce', 'npm', 'debt_to_equity', 'fcf', 
        'pat_cagr_5yr', 'revenue_cagr_5yr', 'eps_cagr_5yr', 
        'interest_coverage', 'asset_turnover'
    ]
    
    for m in metrics_to_rank:
        if m in assigned_df.columns:
            assigned_df[m] = pd.to_numeric(assigned_df[m], errors='coerce')
            
    records = []
    
    for group_name, group_df in assigned_df.groupby('peer_group_name'):
        for idx, row in group_df.iterrows():
            cid = row['company_id']
            for m in metrics_to_rank:
                if m not in group_df.columns:
                    continue
                val = row[m]
                if pd.isna(val):
                    continue
                    
                valid_series = group_df[m].dropna()
                if len(valid_series) <= 1:
                    rank = 1.0
                else:
                    if m == 'debt_to_equity':
                        rank = 1.0 - (valid_series.rank(pct=True).loc[idx])
                    else:
                        rank = valid_series.rank(pct=True).loc[idx]
                        
                records.append({
                    'company_id': cid,
                    'peer_group_name': group_name,
                    'metric': m,
                    'value': float(val),
                    'percentile_rank': float(rank * 100.0),
                    'year': int(current_year)
                })
                
    if not records:
        return
        
    res_df = pd.DataFrame(records)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peer_percentiles (
            company_id TEXT,
            peer_group_name TEXT,
            metric TEXT,
            value REAL,
            percentile_rank REAL,
            year INTEGER
        )
    """)
    
    cursor.execute("DELETE FROM peer_percentiles WHERE year = ?", (int(current_year),))
    
    res_df.to_sql('peer_percentiles', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    
    if not unassigned.empty:
        print("No peer group assigned")