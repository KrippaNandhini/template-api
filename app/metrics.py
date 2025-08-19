from __future__ import annotations

from typing import Final

from prometheus_client import Counter, Gauge, Info

# Namespace keeps your metrics grouped and avoids name clashes
NAMESPACE: Final = "template_api"

UP = Gauge(f"{NAMESPACE}_up", "Service up (1), down (0)")
READY = Gauge(f"{NAMESPACE}_ready", "Readiness (1=ready, 0=not ready)")

HEARTBEAT_TOTAL = Counter(
    f"{NAMESPACE}_heartbeat_total",
    "Background heartbeat iterations",
    labelnames=("task",),
)

BUILD_INFO = Info(
    f"{NAMESPACE}_build_info",
    "Build/version info for the running service",
)
