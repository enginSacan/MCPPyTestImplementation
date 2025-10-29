#!/bin/bash

# Wrapper script to run the MCP server with proper environment
# This ensures the server runs with the correct Python environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to project directory
cd "$SCRIPT_DIR" || exit 1

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!" >&2
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -e ." >&2
    exit 1
fi

# Activate virtual environment and run server
source venv/bin/activate
exec python server.py
