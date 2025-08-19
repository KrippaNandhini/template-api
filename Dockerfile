# ===== Build stage =====
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
# copy metadata and code
COPY pyproject.toml README.md ./
COPY app ./app
# build a wheel for our package
RUN python -m pip install --upgrade pip && pip wheel --no-deps -w dist .

# ===== Runtime stage =====
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
# non-root user
RUN addgroup --system app && adduser --system --ingroup app app
# install the wheel
COPY --from=builder /app/dist/*.whl /tmp/
RUN python -m pip install --no-cache-dir /tmp/*.whl && rm -rf /root/.cache
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
