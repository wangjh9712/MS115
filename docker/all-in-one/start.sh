#!/usr/bin/env bash
set -Eeuo pipefail

shutdown() {
  if [[ -n "${uvicorn_pid:-}" ]]; then
    kill -TERM "${uvicorn_pid}" 2>/dev/null || true
  fi
  if [[ -n "${nginx_pid:-}" ]]; then
    kill -TERM "${nginx_pid}" 2>/dev/null || true
  fi
}

trap shutdown SIGINT SIGTERM

nginx -t

uvicorn main:app --host 127.0.0.1 --port 8000 &
uvicorn_pid=$!

echo "Waiting for backend to become ready..."
max_wait=300
elapsed=0
while [ $elapsed -lt $max_wait ]; do
  if curl -sf http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "Backend is ready (${elapsed}s), starting nginx..."
    break
  fi
  # check uvicorn hasn't crashed
  if ! kill -0 "${uvicorn_pid}" 2>/dev/null; then
    echo "Backend process exited unexpectedly"
    exit 1
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

if [ $elapsed -ge $max_wait ]; then
  echo "Backend did not become ready within ${max_wait}s, starting nginx anyway..."
fi

nginx -g 'daemon off;' &
nginx_pid=$!

wait -n "${uvicorn_pid}" "${nginx_pid}"
exit_code=$?

shutdown

wait "${uvicorn_pid}" 2>/dev/null || true
wait "${nginx_pid}" 2>/dev/null || true

exit "${exit_code}"
