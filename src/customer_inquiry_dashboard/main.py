"""FastAPI app factory with lifespan and routers."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from customer_inquiry_dashboard.routers import health, inquiries
from customer_inquiry_dashboard.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_settings()
    # startup
    yield
    # shutdown


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.service_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(inquiries.router)
    return app


app = create_app()
