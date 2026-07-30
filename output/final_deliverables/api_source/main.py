from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import health, companies, analytics_routes

app = FastAPI(title="N100 Financial Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(analytics_routes.screener_router, prefix="/api/v1", tags=["Screener"])
app.include_router(analytics_routes.sectors_router, prefix="/api/v1", tags=["Sectors"])
app.include_router(analytics_routes.peers_router, prefix="/api/v1", tags=["Peers"])
app.include_router(analytics_routes.portfolio_router, prefix="/api/v1", tags=["Portfolio"])
