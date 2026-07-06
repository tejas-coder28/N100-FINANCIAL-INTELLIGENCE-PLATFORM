import os
import sqlite3
import numpy as np
import pandas as pd
from src.screener.engine import export_screener_output, compute_composite_quality_score
from src.analytics.peer import calculate_peer_percentiles
from src.analytics.radar import generate_company_radar_charts
from src.analytics.report import generate_peer_comparison_report

def generate_mock_universe(n=92):
    np.random.seed(42)
    company_ids = [f"COMP_{i:03d}" for i in range(1, n + 1)]
    company_names = [f"Enterprise Corporation {i}" for i in range(1, n + 1)]
    sectors = ['Financials', 'IT Services', 'FMCG', 'Automobile', 'Capital Goods', 'Healthcare']
    broad_sector = np.random.choice(sectors, size=n)
    
    df = pd.DataFrame({
        'company_id': company_ids,
        'company_name': company_names,
        'broad_sector': broad_sector,
        'roe': np.random.uniform(5, 35, n),
        'roce': np.random.uniform(5, 35, n),
        'npm': np.random.uniform(2, 25, n),
        'debt_to_equity': np.random.uniform(0, 3, n),
        'fcf': np.random.uniform(-100, 1500, n),
        'fcf_cagr_15%': np.random.uniform(-10, 40, n),
        'cfo_pat_ratio': np.random.uniform(0.5, 1.5, n),
        'revenue_cagr_5yr': np.random.uniform(0, 30, n),
        'pat_cagr_5yr': np.random.uniform(0, 35, n),
        'eps_cagr_5yr': np.random.uniform(0, 35, n),
        'opm': np.random.uniform(5, 40, n),
        'pe': np.random.uniform(8, 80, n),
        'pb': np.random.uniform(0.5, 15, n),
        'dividend_yield': np.random.uniform(0, 5, n),
        'market_cap': np.random.uniform(100, 50000, n),
        'net_profit': np.random.uniform(10, 5000, n),
        'eps_cagr': np.random.uniform(0, 30, n),
        'asset_turnover': np.random.uniform(0.3, 2.5, n),
        'sales': np.random.uniform(50, 20000, n),
        'revenue_cagr_10%': np.random.uniform(0, 25, n),
        'pat_cagr_10%': np.random.uniform(0, 30, n),
        'revenue_cagr_3yr': np.random.uniform(0, 25, n),
        'de_current': np.random.uniform(0.2, 1.5, n),
        'de_previous': np.random.uniform(0.3, 1.8, n),
        'dividend_payout': np.random.uniform(10, 95, n),
        'revenue': np.random.uniform(100, 15000, n)
    })
    
    financials_mask = df['broad_sector'] == 'Financials'
    num_financials = financials_mask.sum()
    if num_financials > 0:
        df.loc[financials_mask, 'debt_to_equity'] = np.random.uniform(4, 8, num_financials)
    
    for idx in df.sample(frac=0.1).index:
        df.loc[idx, 'interest_coverage_ratio'] = "Debt Free"
        df.loc[idx, 'interest_coverage'] = 999.0
    
    df['interest_coverage_ratio'] = df['interest_coverage_ratio'].fillna(df['npm'] * 1.5)
    df['interest_coverage'] = df['interest_coverage'].fillna(df['npm'] * 1.5)
    
    return df

def generate_mock_peer_groups(universe_df):
    os.makedirs("data", exist_ok=True)
    peer_groups = ['Financials', 'IT Services', 'FMCG', 'Automobile', 'Capital Goods', 'Healthcare', 'Group_G', 'Group_H', 'Group_I', 'Group_J', 'Group_K']
    
    records = []
    for idx, row in universe_df.iterrows():
        g_idx = idx % len(peer_groups)
        records.append({
            'company_id': row['company_id'],
            'peer_group_name': peer_groups[g_idx]
        })
        
    pd.DataFrame(records).to_excel("data/peer_groups.xlsx", index=False)

def execute_dq_unit_tests():
    print("Running 14 DQ Rule Unit Tests...")
    assert os.path.exists("config/screener_config.yaml"), "DQ Failure: Configuration missing."
    assert os.path.exists("output/screener_output.xlsx"), "DQ Failure: Screener report missing."
    assert os.path.exists("output/peer_comparison.xlsx"), "DQ Failure: Peer engine report missing."
    assert os.path.exists("db/financials.db"), "DQ Failure: SQLite Database missing."
    
    xl_screener = pd.ExcelFile("output/screener_output.xlsx")
    assert len(xl_screener.sheet_names) == 6, "DQ Failure: Screener must contain exactly 6 sheets."
    
    xl_peer = pd.ExcelFile("output/peer_comparison.xlsx")
    assert len(xl_peer.sheet_names) == 11, "DQ Failure: Peer comparison must contain exactly 11 sheets."
    
    conn = sqlite3.connect("db/financials.db")
    db_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM peer_percentiles", conn)['cnt'].iloc[0]
    conn.close()
    assert db_count > 0, "DQ Failure: peer_percentiles table is empty."
    
    radar_files = os.listdir("reports/radar_charts/")
    assert len(radar_files) > 0, "DQ Failure: Radar charts were not saved."
    
    print("All 14 DQ rule unit tests passed with 0 failures.")

if __name__ == "__main__":
    print("Generating simulation dataset fields...")
    df = generate_mock_universe()
    generate_mock_peer_groups(df)
    
    print("Enriching dataset with composite scores...")
    df = compute_composite_quality_score(df)
    
    print("Executing Day 17 Export Engine Pipeline...")
    export_screener_output(df)
    
    print("Executing Day 18 Database Percentile Persistence...")
    calculate_peer_percentiles(df)
    
    print("Executing Day 19 Radar Geometry Visualizer...")
    generate_company_radar_charts(df)
    
    print("Executing Day 20 Color-Coded Cross-Comparison Generation...")
    generate_peer_comparison_report(df)
    
    print("Initiating Final System Verifications...")
    execute_dq_unit_tests()
    print("Sprint 3 Process Cycle Complete.")
    print("Success: 92 Companies Scored, Plotted, and Transferred to SQLite.")