# Quick Start Guide

Get up and running with the New Python Repo Template in minutes!

## Prerequisites

- **Python 3.12+**
- **Git** (for cloning)
- **uv** (Python package manager)

## Step 1: Install uv

If you don't have `uv` installed:

=== "macOS/Linux"
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "Via pip"
    ```bash
    pip install uv
    ```

## Step 2: Create Your Project

### Option A: Use GitHub Template

1. Click "Use this template" on GitHub
2. Create your new repository
3. Clone it locally:

```bash
git clone https://github.com/your-username/your-project-name.git
cd your-project-name
```

### Option B: Clone Directly

```bash
git clone https://github.com/your-username/new-python-repo.git my-project
cd my-project
rm -rf .git  # Remove template git history
git init     # Start fresh
```

## Step 3: Install Dependencies

```bash
# Install core dependencies only
uv sync

# Or install everything (recommended for exploring)
uv sync --all-extras

# Or install specific groups
uv sync --extra docs --extra dev
```

## Step 4: Try the Demos

```bash
# Interactive demo selection
./run_demo.sh

# Or run specific demos
./run_demo.sh 1  # Package-based imports
./run_demo.sh 2  # Direct module imports
```

## Step 5: Customize for Your Project

### Update Project Metadata

Edit `pyproject.toml`:

```toml
[project]
name = "your-project-name"           # ← Change this
version = "0.1.0"
description = "Your project description"  # ← Change this
authors = [
    {name = "Your Name", email = "your.email@example.com"}  # ← Change this
]
```

### Add Your Code

Choose your preferred structure:

=== "Package Approach"
    ```bash
    mkdir -p src/mypackage
    echo "# Your package" > src/mypackage/__init__.py
    echo "def hello(): return 'Hello World!'" > src/mypackage/utils.py
    ```

=== "Direct Module Approach"
    ```bash
    mkdir -p src/myapp
    echo "# Your app" > src/myapp/__init__.py
    echo "def hello(): return 'Hello World!'" > src/myapp/utils.py
    ```

## Step 6: Build Documentation

```bash
# Install docs dependencies
uv sync --extra docs

# Serve docs locally
uv run mkdocs serve
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see your docs!

## Next Steps

- **[Learn Import Patterns](import-patterns.md)** - Understand module organization
- **[Explore Demos](demos.md)** - See practical examples
- **[Set Up Documentation](../tutorials/docs-setup.md)** - Customize your docs

!!! success "You're Ready!"
    Your modern Python project is now set up with fast dependency management, documentation, and demo applications!