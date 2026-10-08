FROM python:3.12-slim

# curl: Coolify runs its health check with curl inside the container
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY entrypoint.py /app/entrypoint.py

RUN useradd --create-home --uid 1000 mcp
USER mcp

# Coolify "Ports Exposes" must match (8080)
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD curl -fsS http://127.0.0.1:8080/status || exit 1

CMD ["python", "/app/entrypoint.py"]
