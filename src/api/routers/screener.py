import os
import sqlite3
from fastapi import APIRouter, Query

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/screener")
def screen_companies(
    min_roe: float = Query(None),
    max_debt_equity: float = Query(None),
    min_margin: float = Query(None),
    sector: str = Query(None)
):
    if not os.path.exists(DB_PATH):
        return {"results": [], "count": 0}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    conditions = []
    params = []
    
    if min_roe is not None:
        conditions.append("return_on_equity_pct >= ?")
        params.append(min_roe)
    if max_debt_equity is not None:
        conditions.append("debt_to_equity <= ?")
        params.append(max_debt_equity)
    if min_margin is not None:
        conditions.append("operating_profit_margin_pct >= ?")
        params.append(min_margin)
    if sector:
        conditions.append("broad_sector = ?")
        params.append(sector)
        
    query = "SELECT * FROM companies"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return {"results": [dict(r) for r in rows], "count": len(rows)}
    except Exception:
        return {"results": [], "count": 0}
    finally:
        conn.close()
