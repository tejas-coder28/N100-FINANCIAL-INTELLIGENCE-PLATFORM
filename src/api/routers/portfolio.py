import os
import sqlite3
from fastapi import APIRouter

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/portfolio/stats")
def get_portfolio_stats():
    if not os.path.exists(DB_PATH):
        return {"total_companies": 0, "avg_roe": 0, "avg_debt_equity": 0}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total_companies,
                AVG(return_on_equity_pct) as avg_roe,
                AVG(debt_to_equity) as avg_debt_equity,
                AVG(operating_profit_margin_pct) as avg_margin
            FROM companies
        """)
        row = cursor.fetchone()
        if row and row["total_companies"] > 0:
            return {
                "total_companies": row["total_companies"],
                "avg_roe": round(row["avg_roe"] or 0, 2),
                "avg_debt_equity": round(row["avg_debt_equity"] or 0, 2),
                "avg_operating_margin": round(row["avg_margin"] or 0, 2)
            }
        return {"total_companies": 0, "avg_roe": 0, "avg_debt_equity": 0}
    except Exception:
        return {"total_companies": 0, "avg_roe": 0, "avg_debt_equity": 0}
    finally:
        conn.close()
