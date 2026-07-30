from fastapi import APIRouter, HTTPException
import sqlite3, os, json
import pandas as pd

router = APIRouter()

def get_db():
    return sqlite3.connect(os.path.join("data", "financial_analytics.db"))

def sanitize_records(df):
    """Safely convert DataFrame to JSON-compliant list of dicts (handling NaN/Inf as null)."""
    return json.loads(df.to_json(orient="records"))

@router.get("/companies")
def list_companies(sector: str = None, search: str = None):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    
    if sector and 'broad_sector' in df.columns:
        df = df[df['broad_sector'].str.contains(sector, case=False, na=False)]
    if search:
        mask = df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        df = df[mask]
        
    return sanitize_records(df)

@router.get("/companies/{ticker}")
def get_company(ticker: str):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM companies", conn)
    conn.close()
    
    id_col = [c for c in df.columns if c in ['id', 'ticker', 'symbol', 'company_id']][0]
    match = df[df[id_col].astype(str).str.upper() == ticker.upper()]
    
    if match.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    return sanitize_records(match)[0]

@router.get("/companies/{ticker}/pl")
def get_pl(ticker: str):
    conn = get_db()
    try:
        df = pd.read_sql_query("SELECT * FROM income_statement", conn)
        conn.close()
        id_col = [c for c in df.columns if c in ['id', 'ticker', 'symbol', 'company_id']][0]
        match = df[df[id_col].astype(str).str.upper() == ticker.upper()]
        return sanitize_records(match)
    except Exception:
        conn.close()
        return []

@router.get("/companies/{ticker}/bs")
def get_bs(ticker: str):
    conn = get_db()
    try:
        df = pd.read_sql_query("SELECT * FROM balance_sheet", conn)
        conn.close()
        id_col = [c for c in df.columns if c in ['id', 'ticker', 'symbol', 'company_id']][0]
        match = df[df[id_col].astype(str).str.upper() == ticker.upper()]
        return sanitize_records(match)
    except Exception:
        conn.close()
        return []

@router.get("/companies/{ticker}/cashflow")
def get_cashflow(ticker: str):
    conn = get_db()
    try:
        df = pd.read_sql_query("SELECT * FROM cash_flow", conn)
        conn.close()
        id_col = [c for c in df.columns if c in ['id', 'ticker', 'symbol', 'company_id']][0]
        match = df[df[id_col].astype(str).str.upper() == ticker.upper()]
        return sanitize_records(match)
    except Exception:
        conn.close()
        return []

@router.get("/companies/{ticker}/ratios")
def get_ratios(ticker: str):
    conn = get_db()
    try:
        df = pd.read_sql_query("SELECT * FROM financial_ratios", conn)
        conn.close()
        id_col = [c for c in df.columns if c in ['id', 'ticker', 'symbol', 'company_id']][0]
        match = df[df[id_col].astype(str).str.upper() == ticker.upper()]
        return sanitize_records(match)
    except Exception:
        conn.close()
        return []
