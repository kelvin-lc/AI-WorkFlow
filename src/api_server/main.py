import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import colorlog
import sentry_sdk
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from src.api_server.api.api_v1 import api_router
from src.api_server.api.deps import create_tables
from src.api_server.api.errors import (
    APIError,
    api_error_handler,
    http_exception_handler,
)
from src.api_server.config import settings
from src.api_server.utils.logging_config import setup_logging as configure_logging
from src.api_server.utils.middleware import SecurityHeadersMiddleware, TimingMiddleware


def setup_sentry() -> None:
    """Initialize Sentry for error tracking."""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0 if settings.is_development else 0.1,
            environment=settings.ENVIRONMENT,
            release=settings.VERSION,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    configure_logging()
    setup_sentry()

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    if settings.is_development:
        await create_tables()
        logger.info("Database tables created/updated")

    yield

    # Shutdown
    logger.info("Application shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI WorkFlow - Bring Your Own Agent Platform",
        version=settings.VERSION,
        debug=settings.DEBUG,
        terms_of_service="https://example.com/terms",
        contact={
            "name": "AI WorkFlow Team",
            "email": "support@example.com",
            "url": "https://example.com/contact",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )

    # Custom middleware (order matters - last added runs first)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )

    # Static files
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount(
            "/static",
            StaticFiles(directory=str(static_dir)),
            name="static",
        )

    # Exception handlers
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    return app


app = create_app()


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with local static files."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.PROJECT_NAME} - API Documentation",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


def run_server():
    """Run the development server."""
    uvicorn.run(
        "src.api_server.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.is_development,
        workers=1 if settings.is_development else settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.is_development,
    )


if __name__ == "__main__":
    run_server()
