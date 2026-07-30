import os
import sqlite3
import pandas as pd

DB_PATH = "data/financial_analytics.db"

FILES_TO_EXPORT = [
    ("output/analysis_parsed.csv", "nlp_analysis_parsed"),
    ("output/parse_failures.csv", "nlp_parse_failures"),
    ("output/pros_cons_generated.csv", "nlp_pros_cons"),
    ("output/cashflow_intelligence.xlsx", "analytics_cashflow_intelligence"),
    ("output/distress_alerts.csv", "analytics_distress_alerts"),
    ("output/pattern_changes.csv", "analytics_pattern_changes")
]

def export_all_to_sqlite():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
        
    conn = sqlite3.connect(DB_PATH)

    for file_path, table_name in FILES_TO_EXPORT:
        if not os.path.exists(file_path):
            continue
            
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                continue

            df.to_sql(table_name, conn, if_exists="replace", index=False)
        except Exception:
            pass

    conn.close()

if __name__ == "__main__":
    export_all_to_sqlite()