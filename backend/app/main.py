"""
Mindease FastAPI application entry point.
"""
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import Base, engine

# Register ORM models before create_all.
import app.models.chat  # noqa: F401
import app.models.diary  # noqa: F401
import app.models.mood  # noqa: F401

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("Mindease")

BACKEND_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BACKEND_DIR / "static"
INDEX_HTML = STATIC_DIR / "index.html"

app = FastAPI(
    title="Mindease API",
    description=(
        "Privacy-first AI mental health companion backend. "
        "Backed by SQLAlchemy. No external APIs."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.utils.error_handlers import (  # noqa: E402
    generic_exception_handler,
    http_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

from app.routes import chat, diary, insights, mood  # noqa: E402

app.include_router(mood.router)
app.include_router(chat.router)
app.include_router(diary.router)
app.include_router(insights.router)

app.include_router(mood.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(diary.router, prefix="/api")
app.include_router(insights.router, prefix="/api")

if (STATIC_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


def health_response():
    return {
        "status": "ok",
        "message": "Mindease API is running",
        "version": "2.0.0",
        "docs": "/api/docs",
    }


@app.get("/", tags=["Frontend"])
def root():
    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)
    return health_response()


@app.get("/api", tags=["Health"])
@app.get("/api/", tags=["Health"])
def api_root():
    return health_response()


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")

    requested_file = STATIC_DIR / full_path
    if requested_file.is_file():
        return FileResponse(requested_file)

    if INDEX_HTML.exists():
        return FileResponse(INDEX_HTML)

    return health_response()
