import os
import sqlite3
from fastapi import APIRouter, Query

router = APIRouter()
DB_PATH = os.path.join("data", "financial_analytics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/documents")
def list_documents(company_id: str = Query(None), doc_type: str = Query(None)):
    if not os.path.exists(DB_PATH):
        return {"documents": []}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    conditions = []
    params = []
    
    if company_id:
        conditions.append("company_id = ?")
        params.append(company_id)
    if doc_type:
        conditions.append("doc_type = ?")
        params.append(doc_type)
        
    query = "SELECT * FROM documents"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return {"documents": [dict(r) for r in rows]}
    except Exception:
        return {"documents": []}
    finally:
        conn.close()
