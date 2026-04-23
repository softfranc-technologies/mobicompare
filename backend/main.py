"""
main.py — MobiCompare FastAPI Application
Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from database import db
from routes import mobiles, compare, filters, search, prices, auth, admin
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print("✅ MongoDB connected")
    yield
    await db.disconnect()
    print("🔌 MongoDB disconnected")


app = FastAPI(
    title="MobiCompare API",
    description="India's best mobile price comparison backend",
    version="2.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routers ───────────────────────────────────────────────────────────────
app.include_router(mobiles.router, prefix="/api/mobiles",  tags=["Mobiles"])
app.include_router(compare.router, prefix="/api/compare",  tags=["Compare"])
app.include_router(filters.router, prefix="/api/filters",  tags=["Filters"])
app.include_router(search.router,  prefix="/api/search",   tags=["Search"])
app.include_router(prices.router,  prefix="/api/prices",   tags=["Prices"])
app.include_router(auth.router,    prefix="/api/auth",     tags=["Auth"])
app.include_router(admin.router,   prefix="/api/admin",    tags=["Admin"])


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health():
    db_ok = await db.ping()
    return {"api": "ok", "database": "ok" if db_ok else "error"}


# ── Serve Frontend ────────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
