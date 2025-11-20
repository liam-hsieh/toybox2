#!/usr/bin/env bash

# Demo script for new-python-repo template
# This script demonstrates how to run the Streamlit app
#
# Usage:
#   ./run_demo.sh           # Interactive selection with detailed explanations
#   ./run_demo.sh 1         # Run demo1 (package-based imports)
#   ./run_demo.sh demo1     # Run demo1 (package-based imports)
#   ./run_demo.sh 2         # Run demo2 (direct module imports)
#   ./run_demo.sh demo2     # Run demo2 (direct module imports)

set -e  # Exit on any error

echo "New Python Repo - Demo Application"
echo "===================================="
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

echo "Project structure verified"

# Install dependencies if needed
echo "Installing dependencies..."
uv sync --all-extras

echo "Dependencies installed"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Something went wrong with 'uv sync'"
    exit 1
fi

echo "Virtual environment ready"

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

echo "Project structure verified"

# Install dependencies if needed
echo "Installing dependencies..."
uv sync --all-extras

echo "Dependencies installed"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Something went wrong with 'uv sync'"
    exit 1
fi

echo "Virtual environment ready"
echo

# Display some useful information
echo "Demo Information:"
echo "   • App Type: Streamlit Web Application"
echo "   • Custom Modules: Shared utility functions"
echo

# Demo selection
echo "Available Demos:"
echo "   1) demo1 - Package-based import demo (src/demo_app.py)"
echo "      Uses: 'from libs.example_module1 import import_checking1'"
echo "      Demonstrates: Proper package structure with libs/ as a Python package"
echo "      Requires: Package declared in pyproject.toml [tool.hatch.build.targets.wheel]"
echo
echo "   2) demo2 - Direct module import demo (src/demo_sub_app/sub_demo_app.py)"
echo "      Uses: 'from example_module2 import import_checking2'"
echo "      Demonstrates: Direct module import from same directory"
echo "      Requires: Module file listed individually in pyproject.toml packages"
echo

echo "Key Differences:"
echo "   • Demo1: Shows how to structure reusable packages (recommended for libraries)"
echo "   • Demo2: Shows how to import individual modules (good for simple utilities)"
echo "   • pyproject.toml configuration differs for each approach"
echo

# Get user selection
if [ $# -eq 0 ]; then
    read -p "Select demo (1 or 2) [default: 1]: " demo_choice
    demo_choice=${demo_choice:-1}
else
    demo_choice=$1
fi

# Set demo file path based on selection
case $demo_choice in
    1|demo1)
        demo_file="src/demo_app.py"
        demo_name="Main Demo App"
        ;;
    2|demo2)
        demo_file="src/demo_sub_app/sub_demo_app.py"
        demo_name="Sub Demo App"
        ;;
    *)
        echo "Invalid selection. Please choose 1 or 2."
        exit 1
        ;;
esac

# Check if demo file exists
if [ ! -f "$demo_file" ]; then
    echo "Demo file not found: $demo_file"
    exit 1
fi

echo "Selected: $demo_name ($demo_file)"

# Run the Streamlit app
echo "Starting Streamlit application..."
echo "   App will open at: http://localhost:8521"
echo "   Use Ctrl+C to stop the application"
echo

# Give user a moment to read
sleep 2

# Run the app
echo "Launching $demo_name..."
uv run streamlit run "$demo_file" --server.port 8521