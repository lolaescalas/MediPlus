"""
main.py — Entrypoint de la API FastAPI.

Ejecutar con:
    uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import mongo_router, neo4j_router
from app.db.mongo import close_mongo
from app.db.neo4j_db import close_neo4j


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    print("🚀 API iniciando...")
    yield
    # ── Shutdown ─────────────────────────────────────────────
    print("🛑 Cerrando conexiones...")
    close_mongo()
    close_neo4j()
    print("✅ Conexiones cerradas.")


app = FastAPI(
    title="DataViz API",
    description="Backend Python para visualizar datos de MongoDB Atlas y Neo4j Aura desde WinForms.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: permite que el cliente C# (localhost) consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(mongo_router.router)
app.include_router(neo4j_router.router)


@app.get("/", tags=["General"])
def root():
    return {"mensaje": "DataViz API corriendo ✅", "docs": "/docs"}


@app.get("/health", tags=["General"])
def health():
    """Health check general de la API."""
    from app.db.mongo import ping_mongo
    from app.db.neo4j_db import ping_neo4j
    return {
        "api": "ok",
        "mongodb": ping_mongo(),
        "neo4j": ping_neo4j(),
    }
