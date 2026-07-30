import os
import sqlite3
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/valuation")
def get_valuation_metrics(company_id: str = Query(None)):
    if not os.path.exists(DB_PATH):
        return {"data": []}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if company_id:
            cursor.execute("SELECT * FROM valuation_multiples WHERE company_id = ?", (company_id,))
            rows = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM valuation_multiples LIMIT 50")
            rows = cursor.fetchall()
            
        return {"data": [dict(r) for r in rows]}
    except Exception:
        return {"data": []}
    finally:
        conn.close()
