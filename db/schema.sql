PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sectors (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    sector_id INTEGER,
    FOREIGN KEY (sector_id) REFERENCES sectors(sector_id)
);

CREATE TABLE IF NOT EXISTS profitandloss (
    pnl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    sales REAL,
    opm REAL,
    net_profit REAL,
    eps REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    UNIQUE(company_id, year)
);

CREATE TABLE IF NOT EXISTS balancesheet (
    bs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    share_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_assets REAL,
    total_assets REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    UNIQUE(company_id, year)
);

CREATE TABLE IF NOT EXISTS cashflow (
    cf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    operating_cash_flow REAL,
    investing_cash_flow REAL,
    financing_cash_flow REAL,
    net_cash_flow REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    UNIQUE(company_id, year)
);

CREATE TABLE IF NOT EXISTS analysis (
    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    document_type TEXT NOT NULL,
    document_url TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS prosandcons (
    pc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('PRO', 'CON')),
    point_text TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    close_price REAL NOT NULL,
    volume INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    ratio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    pe_ratio REAL,
    pb_ratio REAL,
    roe REAL,
    roce REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    UNIQUE(company_id, year)
);

CREATE TABLE IF NOT EXISTS peer_groups (
    peer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    peer_company_id INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (peer_company_id) REFERENCES companies(company_id)
);