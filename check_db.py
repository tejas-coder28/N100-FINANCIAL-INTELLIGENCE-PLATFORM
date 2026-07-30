import os
import sqlite3

data_dir = "data"
if os.path.exists(data_dir):
    files = [f for f in os.listdir(data_dir) if f.endswith((".db", ".sqlite", ".sqlite3"))]
    if not files:
        print("No database files found in data/ directory.")
    for file in files:
        path = os.path.join(data_dir, file)
        conn = sqlite3.connect(path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print(f"Database Path: {path}")
        print(f"Tables: {[t[0] for t in tables]}\n")
        conn.close()
else:
    print("data/ directory does not exist.")