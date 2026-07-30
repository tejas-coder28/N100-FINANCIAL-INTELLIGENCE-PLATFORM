from fastapi import APIRouter
import sqlite3
import os
import time

router = APIRouter()
start_time = time.time()

@router.get("/health")
def get_health():
    db_path = os.path.join("data", "financial_analytics.db")
    counts = {}
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        for t in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {t}")
                counts[t] = cursor.fetchone()[0]
            except Exception:
                counts[t] = 0
        conn.close()
        
    return {
        "status": "ok",
        "db_row_counts": counts,
        "uptime_seconds": round(time.time() - start_time, 2),
        "version": "1.0.0"
    }
