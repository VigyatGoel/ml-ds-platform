# Combined FastAPI + Streamlit Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    BACKEND_PORT=8000

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt /app/requirements.txt
# Add extra frontend deps (if not already present)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src
COPY streamlit_frontend /app/streamlit_frontend
COPY run_all.sh /app/run_all.sh

RUN chmod +x /app/run_all.sh && mkdir -p /app/uploads /app/src/csvfiles

# Expose default dev port; Cloud Run will override via $PORT automatically.
EXPOSE 8501

# Healthcheck now via Streamlit (backend kept private). Adjust path if you add a custom health route.
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["/app/run_all.sh"]
