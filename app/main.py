from contextlib import asynccontextmanager
import asyncio
import logging
from typing import AsyncIterator

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .logging_config import setup_logging
from . import settings

setup_logging()
log = logging.getLogger("template-api")


async def _periodic_heartbeat(stop: asyncio.Event) -> None:
    """Example repeating task; replace body with your real job."""
    while not stop.is_set():
        log.info("heartbeat")
        await asyncio.sleep(60)  # run every 60s


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # ---- startup ----
    log.info(
        "service_startup",
        extra={
            "app_name": settings.settings.APP_NAME,
            "db_host": settings.settings.DB_HOST,
        },
    )
    log.info(
        "settings_loaded",
        extra={
            "app_name": settings.settings.APP_NAME,
            "db_host": settings.settings.DB_HOST,
        },
    )
    stop = asyncio.Event()
    periodic_task = asyncio.create_task(
        _periodic_heartbeat(stop)
    )  # optional repeating task

    try:
        yield
    finally:
        # ---- shutdown ----
        stop.set()
        periodic_task.cancel()
        try:
            await periodic_task
        except asyncio.CancelledError:
            pass
        log.info("service_shutdown")


app = FastAPI(title="Template API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
