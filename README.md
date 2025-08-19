# Template API

![CI](https://github.com/KrippaNandhini/template-api/actions/workflows/ci.yml/badge.svg)

FastAPI template with `/health`, `/metrics` (Prometheus), structured JSON logs, tests, pre-commit, and Docker.

## Run (dev)
```bash
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
# http://localhost:8000/health  http://localhost:8000/metrics
