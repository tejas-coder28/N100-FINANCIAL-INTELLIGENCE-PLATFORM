Set-Content -Path "README.md" -Value '# N100 Financial Intelligence Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A high-performance financial intelligence backend designed for real-time stock screening, sector analysis, and automated portfolio reporting.

## 🚀 Key Features
* **Stock Screener**: Dynamic filtering by ROE, P/E, and Sector.
* **Sector Analysis**: Automated aggregation and sector-level performance metrics.
* **Reporting**: Automated generation of company tearsheet PDFs.
* **Test-Driven**: 100% test coverage for core financial KPIs and API routes.

---

## 📂 Project Structure
```text
N100-FINANCIAL-INTELLIGENCE-PLATFORM/
├── data/               # SQLite database storage
├── reports/            # Generated PDF tearsheets
├── scripts/            # Deployment and utility scripts
├── src/api/            # FastAPI Routers (companies, screener, sectors)
├── tests/              # Pytest integration/unit tests
└── vercel.json         # Deployment configuration