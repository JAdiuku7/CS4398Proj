import logging
from contextlib import asynccontextmanager
 
from fastapi import FastAPI
 
from app.core.exceptions import register_exception_handlers
from app.src.base import Base
from app.src.session import engine
from app.routers import admin, auth
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)
 
 
# ── Startup / shutdown ─────────────────────────────────────────────────────────
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup (use Alembic for production migrations)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ready")
    yield
    await engine.dispose()
    logger.info("Database connection closed")
 
 
# ── App factory ────────────────────────────────────────────────────────────────
 
app = FastAPI(
    title="Fitness Coaching — Admin API",
    version="1.0.0",
    description="Admin module: login, user CRUD, trainer CRUD, access control.",
    lifespan=lifespan,
)
 
register_exception_handlers(app)
 
app.include_router(auth.router)
app.include_router(admin.router)
 
 
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}