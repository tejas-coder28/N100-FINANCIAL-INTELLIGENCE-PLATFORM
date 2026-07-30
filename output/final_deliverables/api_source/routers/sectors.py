import os
import sqlite3
from fastapi import APIRouter

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/sectors")
def list_sectors():
    if not os.path.exists(DB_PATH):
        return {"sectors": []}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT DISTINCT broad_sector FROM companies WHERE broad_sector IS NOT NULL")
        rows = cursor.fetchall()
        return {"sectors": [r["broad_sector"] for r in rows]}
    except Exception:
        return {"sectors": []}
    finally:
        conn.close()
