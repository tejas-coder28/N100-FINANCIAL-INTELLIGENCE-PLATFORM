from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    health,
    companies,
    sectors,
    screener,
    peers,
    portfolio,
    valuation,
    documents,
    analytics_routes,
)

app = FastAPI(
    title="N100 Financial Intelligence Platform API",
    version="1.0.0",
    description="Financial analytics and screener backend API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")

app.include_router(health.router, tags=["Health"])
app.include_router(companies.router, tags=["Companies"])
app.include_router(sectors.router, tags=["Sectors"])
app.include_router(screener.router, tags=["Screener"])
app.include_router(peers.router, tags=["Peers"])
app.include_router(portfolio.router, tags=["Portfolio"])
app.include_router(valuation.router, tags=["Valuation"])
app.include_router(documents.router, tags=["Documents"])
app.include_router(analytics_routes.router, tags=["Analytics"])
