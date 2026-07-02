from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.core.telemetry import telemetry
from app.database import Base, engine
from app.models import Content, Idea, Trend
from app.routers.content import router as content_router
from app.routers.idea import router as idea_router
from app.routers.trend import router as trend_router

configure_logging()

app = FastAPI(
    title="INSight OS API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(content_router)
app.include_router(trend_router)
app.include_router(idea_router)
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "insight-os-api"}


@app.get("/telemetry")
def get_telemetry():
    return telemetry.snapshot()
