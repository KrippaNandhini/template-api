import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import metrics as m
from . import settings
from .logging_config import setup_logging

setup_logging()
log = logging.getLogger("template-api")


async def _periodic_heartbeat(stop: asyncio.Event) -> None:
    """Example repeating task; replace body with your real job."""
    while not stop.is_set():
        log.info("heartbeat")
        # custom metric for your background task
        m.HEARTBEAT_TOTAL.labels(task="periodic_heartbeat").inc()
        await asyncio.sleep(60)  # run every 60s


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # ---- startup ----
    # Mark service up (process is accepting requests)
    m.UP.set(1)

    # If you have external deps (DB, cache), validate here first.
    # For now we consider ready on startup:
    m.READY.set(1)

    # Publish build info (labels show in Prometheus)
    # app.version is set when we construct FastAPI(app, version="...")
    m.BUILD_INFO.info(
        {
            "app_name": settings.settings.APP_NAME,
            "version": getattr(app, "version", "unknown"),
        }
    )

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
    periodic_task = asyncio.create_task(_periodic_heartbeat(stop))

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
        # Expose that we are going down
        m.READY.set(0)
        m.UP.set(0)
        log.info("service_shutdown")


app = FastAPI(title="Template API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    """Readiness probe for orchestrators; you can gate on DB ping etc."""
    # For richer checks, toggle m.READY based on dependency status.
    return {"status": "ready"}


# Prometheus /metrics (includes default HTTP metrics + our custom ones)
# Note: Instrumentator adds request/latency metrics with good defaults.
Instrumentator().instrument(app).expose(
    app, endpoint="/metrics", include_in_schema=False
)
