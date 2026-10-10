# File service image. Runs as non-root; mount nothing writable.
# docker run --read-only --network <internal> -e EEFILE_API_TOKEN=... -p 8080:8080 eeganizer-files
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md THIRD_PARTY_NOTICES.md ./
COPY src ./src
RUN pip install --no-cache-dir ".[service]" && useradd --system --no-create-home eefile

USER eefile
EXPOSE 8080
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
CMD ["uvicorn", "--factory", "eeganizer_files.service:create_app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
