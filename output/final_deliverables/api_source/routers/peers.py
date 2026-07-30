import os
import sqlite3
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/peers")
def get_peers(company_id: str = Query(...)):
    if not os.path.exists(DB_PATH):
        return {"company_id": company_id, "peers": []}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT broad_sector FROM companies WHERE company_id = ?", (company_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Target company not found")
            
        sector = row["broad_sector"]
        cursor.execute(
            "SELECT * FROM companies WHERE broad_sector = ? AND company_id != ? LIMIT 5",
            (sector, company_id)
        )
        peers = cursor.fetchall()
        return {"company_id": company_id, "sector": sector, "peers": [dict(p) for p in peers]}
    except HTTPException:
        raise
    except Exception:
        return {"company_id": company_id, "peers": []}
    finally:
        conn.close()
