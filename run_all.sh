#!/usr/bin/env bash
set -euo pipefail

# Ports:
# BACKEND_PORT: internal FastAPI port (never exposed outside container)
# FRONTEND_PORT: Streamlit external port. If Cloud Run (or similar) sets $PORT, use that.
BACKEND_PORT=${BACKEND_PORT:-8000}

# Priority order for frontend port:
# 1. Explicit FRONTEND_PORT
# 2. Cloud provider PORT (e.g. Cloud Run)
# 3. Default 8501 for local/dev
if [ -n "${FRONTEND_PORT:-}" ]; then
  : # keep provided FRONTEND_PORT
elif [ -n "${PORT:-}" ]; then
  FRONTEND_PORT="$PORT"
else
  FRONTEND_PORT=8501
fi

export API_BASE_URL="http://localhost:${BACKEND_PORT}"

echo "[run_all] Starting FastAPI on :${BACKEND_PORT}"
uvicorn src.api.main:app --host 127.0.0.1 --port ${BACKEND_PORT} &
API_PID=$!

# Basic health wait
for i in {1..20}; do
  if curl -s "http://localhost:${BACKEND_PORT}/health" >/dev/null 2>&1; then
    echo "[run_all] FastAPI healthy"
    break
  fi
  sleep 0.5
done

echo "[run_all] Starting Streamlit on :${FRONTEND_PORT} (Cloud PORT=${PORT:-unset})"
streamlit run streamlit_frontend/app.py \
  --server.port ${FRONTEND_PORT} \
  --server.address 0.0.0.0

# On Streamlit exit, stop API
kill ${API_PID} 2>/dev/null || true
