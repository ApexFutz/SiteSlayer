#!/bin/bash
# Script to start the SiteSlayer web server.

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT" || exit 1

# Start the server using uv
uv run uvicorn website_server.main:app --host 0.0.0.0 --port 8000 --reload

