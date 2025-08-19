from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint_exposes_prometheus_text() -> None:
    r = client.get("/metrics")
    assert r.status_code == 200
    # Prometheus text exposition format
    assert r.headers["content-type"].startswith("text/plain")
    body = r.text
    # Custom metrics should appear
    assert "template_api_up" in body
    assert "template_api_ready" in body
    assert "template_api_build_info" in body


def test_ready_probe_ok() -> None:
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}
