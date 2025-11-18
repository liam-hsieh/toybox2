#!/usr/bin/env bash

# Documentation server script for new-python-repo template
# This script starts the MkDocs development server

set -e  # Exit on any error

echo "New Python Repo - Documentation Server"
echo "========================================="
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   # or"
    echo "   pip install uv"
    exit 1
fi

echo "uv is installed"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Please run this script from the project root directory (where pyproject.toml is located)"
    exit 1
fi

if [ ! -f "mkdocs.yml" ]; then
    echo "mkdocs.yml not found. Make sure documentation is set up."
    exit 1
fi

echo "Project structure verified"

# Install docs dependencies if needed
echo "Installing documentation dependencies..."
uv sync --extra docs

echo "Documentation dependencies installed"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Something went wrong with 'uv sync'"
    exit 1
fi

echo "Virtual environment ready"
echo

echo

# Display information
echo "Documentation Server Information:"
echo "   • Framework: MkDocs with Material theme"
echo "   • Auto-reload: Enabled"
echo "   • API docs: Auto-generated from docstrings"
echo "   • URL: http://127.0.0.1:8000"
echo

# Run MkDocs
echo "Starting documentation server..."
echo "   Documentation will open at: http://127.0.0.1:8000"
echo "   Use Ctrl+C to stop the server"
echo "   Changes to .md files and docstrings will auto-reload"
echo

# Give user a moment to read
sleep 2

# Start MkDocs development server
echo "Launching documentation server..."
uv run mkdocs serve -a 0.0.0.0:8008