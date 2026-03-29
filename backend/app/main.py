"""MindMirror FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine, Base
from app.routers import public, admin, automation

# Create all tables on startup (for dev; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MindMirror API",
    description="每日正向心理測驗平台 API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

settings = get_settings()
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router)
app.include_router(admin.router)
app.include_router(automation.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "mindmirror"}
