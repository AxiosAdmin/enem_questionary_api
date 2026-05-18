#!/bin/bash
set -e

echo "🚀 Starting API..."

exec uvicorn src.__main__:app --host 0.0.0.0 --port 8000