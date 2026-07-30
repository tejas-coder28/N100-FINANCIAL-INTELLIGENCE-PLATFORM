from fastapi import APIRouter, HTTPException
import sqlite3, os, json
import pandas as pd

screener_router = APIRouter()
sectors_router = APIRouter()
peers_router = APIRouter()
portfolio_router = APIRouter()

def get_db():
    return sqlite3.connect(os.path.join("data", "financial_analytics.db"))

def sanitize_records(df):
    """Safely convert DataFrame to JSON-compliant list of dicts (handling NaN/Inf as null)."""
    return json.loads(df.to_json(orient="records"))

@screener_router.get("/screener")
def run_screener(min_roe: float = None):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    if min_roe is not None:
        roe_col = [c for c in df.columns if 'roe' in c.lower()]
        if roe_col:
            df = df[pd.to_numeric(df[roe_col[0]], errors='coerce') >= min_roe]
    return sanitize_records(df)

@sectors_router.get("/sectors")
def list_sectors():
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    sector_col = 'broad_sector' if 'broad_sector' in df.columns else 'sector'
    if sector_col in df.columns:
        sectors = df[sector_col].dropna().unique().tolist()
        return [{"sector": s} for s in sectors]
    return []

@peers_router.get("/peers/{group_name}")
def get_peers(group_name: str):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    return sanitize_records(df.head(10))

@portfolio_router.get("/portfolio/stats")
def get_portfolio_stats():
    stats_path = os.path.join("output", "portfolio_stats.csv")
    if os.path.exists(stats_path):
        df = pd.read_csv(stats_path)
        return sanitize_records(df)
    return []
