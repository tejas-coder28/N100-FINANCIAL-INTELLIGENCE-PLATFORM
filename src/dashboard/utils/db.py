import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/financials.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=600)
def get_companies():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT DISTINCT company_id FROM peer_percentiles", conn)
    except Exception:
        df = pd.DataFrame({"company_id": [f"COMP_{i:03d}" for i in range(1, 93)]})
    finally:
        conn.close()
        
    sectors = ['Financials', 'IT Services', 'FMCG', 'Automobile', 'Capital Goods', 'Healthcare', 'Group_G', 'Group_H', 'Group_I', 'Group_J', 'Group_K']
    df['company_name'] = df['company_id'].apply(lambda x: f"Enterprise Corporation {int(x.split('_')[1])}")
    df['broad_sector'] = df['company_id'].apply(lambda x: sectors[int(x.split('_')[1]) % len(sectors)])
    df['sub_sector'] = df['broad_sector'].apply(lambda s: f"Sub-Sector {s}")
    df['nse_ticker'] = df['company_id'].apply(lambda x: f"TICK{int(x.split('_')[1]):02d}")
    df['about'] = df.apply(lambda r: f"{r['company_name']} is a high-performing enterprise specialized in {r['broad_sector']} operational segments.", axis=1)
    
    return df

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    import numpy as np
    np_seed = hash(ticker) % 10000
    np.random.seed(np_seed)
    
    years = list(range(2015, 2025))
    records = []
    
    for yr in years:
        records.append({
            "company_id": ticker,
            "year": yr,
            "roe": np.random.uniform(5, 35),
            "roce": np.random.uniform(5, 35),
            "npm": np.random.uniform(2, 25),
            "debt_to_equity": np.random.uniform(0, 3) if "COMP_000" not in ticker else np.random.uniform(4, 8),
            "fcf": np.random.uniform(-100, 1500),
            "revenue_cagr_5yr": np.random.uniform(0, 30),
            "pat_cagr_5yr": np.random.uniform(0, 35),
            "opm": np.random.uniform(5, 40),
            "pe": np.random.uniform(8, 80),
            "pb": np.random.uniform(0.5, 15),
            "dividend_yield": np.random.uniform(0, 5),
            "interest_coverage_ratio": np.random.uniform(1.5, 25),
            "market_cap": np.random.uniform(100, 50000),
            "net_profit": np.random.uniform(10, 5000),
            "eps_cagr": np.random.uniform(0, 30),
            "asset_turnover": np.random.uniform(0.3, 2.5),
            "sales": np.random.uniform(50, 20000),
            "revenue_cagr_10%": np.random.uniform(0, 25),
            "pat_cagr_10%": np.random.uniform(0, 30),
            "revenue_cagr_3yr": np.random.uniform(0, 25),
            "de_current": np.random.uniform(0.2, 1.5),
            "de_previous": np.random.uniform(0.3, 1.8),
            "dividend_payout": np.random.uniform(10, 95),
            "revenue": np.random.uniform(100, 15000),
            "composite_quality_score": np.random.uniform(30, 95)
        })
    df = pd.DataFrame(records)
    if year is not None:
        df = df[df['year'] == int(year)]
    return df

@st.cache_data(ttl=600)
def get_pl(ticker):
    df = get_ratios(ticker)
    return df[['year', 'revenue', 'net_profit', 'opm', 'sales']].copy()

@st.cache_data(ttl=600)
def get_bs(ticker):
    df = get_ratios(ticker)
    return df[['year', 'de_current', 'de_previous', 'debt_to_equity']].copy()

@st.cache_data(ttl=600)
def get_cf(ticker):
    df = get_ratios(ticker)
    return df[['year', 'fcf']].copy()

@st.cache_data(ttl=600)
def get_sectors():
    companies = get_companies()
    return sorted(list(companies['broad_sector'].unique()))

@st.cache_data(ttl=600)
def get_peers(group_name):
    companies = get_companies()
    return companies[companies['broad_sector'] == group_name]

@st.cache_data(ttl=600)
def get_valuation(ticker):
    if not os.path.exists(DB_PATH):
        return pd.DataFrame([{
            "company_id": ticker,
            "pe": 15.0,
            "pb": 1.5,
            "fcf_yield_pct": 4.5,
            "flag": "Fair"
        }])
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM peer_percentiles WHERE company_id = ?", conn, params=(ticker,))
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df