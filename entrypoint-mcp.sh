#!/usr/bin/env bash
set -e

# Start Memegen in the background
poetry run gunicorn \
    --bind "0.0.0.0:5000" \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout=20 \
    --daemon \
    app.main:app

# Wait for Memegen to be ready
echo "Waiting for Memegen to start..." >&2
for i in {1..30}; do
    if curl -s http://localhost:5000/templates/ > /dev/null 2>&1; then
        echo "Memegen is ready!" >&2
        break
    fi
    sleep 1
done

# Start MCP server on stdio
exec poetry run python -u mcp_server.py

