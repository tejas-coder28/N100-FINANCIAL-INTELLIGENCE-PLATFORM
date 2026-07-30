import sqlite3

db_path = "data/financial_platform.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    sector TEXT
)
""")

cur.execute("SELECT COUNT(*) FROM companies")
count = cur.fetchone()[0]

if count < 92:
    companies_data = []
    for i in range(1, 93):
        companies_data.append((f"TICKER_{i:02d}", f"Company {i}", "IT" if i % 2 == 0 else "Finance"))
    
    cur.executemany("INSERT OR IGNORE INTO companies (ticker, company_name, sector) VALUES (?, ?, ?)", companies_data)
    conn.commit()
    print(f"Successfully created and seeded {len(companies_data)} companies into {db_path}.")
else:
    print(f"Table 'companies' already exists with {count} records.")

conn.close()