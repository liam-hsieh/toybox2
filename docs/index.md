# New Python Repo Template

Welcome to the **New Python Repo Template** documentation! This template provides a modern foundation for Python projects using [uv](https://github.com/astral-sh/uv) for fast dependency management.

## Quick Overview

This template demonstrates:

- **Modern Python packaging** with `pyproject.toml`
- **Fast dependency management** with `uv`
- **Two import patterns** for different project structures
- **Interactive demo applications** built with Streamlit
- **Professional documentation** with MkDocs + mkdocstrings
- **Comprehensive logging** following Python best practices

## Key Features

=== "Package Management"
    - Fast dependency resolution with `uv`
    - Optional dependency groups for different features
    - Lock file for reproducible builds
    - Cross-platform compatibility

=== "Project Structure"
    - `src/` layout for clean organization
    - Package-based and direct imports
    - Modular code architecture
    - Ready for distribution

=== "Documentation"
    - Auto-generated API docs from docstrings
    - Interactive examples and tutorials
    - Material Design theme
    - Search functionality

=== "Logging & Debugging"
    - Hierarchical logger patterns
    - Module-level and function-level logging
    - Class-based logging demonstrations
    - Production-ready configurations
    - Third-party library suppression

=== "Demo Applications"
    - Streamlit web apps
    - Data visualization examples
    - Custom module integration
    - Different import patterns
    - Comprehensive logging examples

## Navigation

- **[Getting Started](getting-started/quick-start.md)** - Set up and run your first project
- **[Import Patterns](getting-started/import-patterns.md)** - Learn different module organization approaches
- **[Demo Applications](getting-started/demos.md)** - Explore the included examples with logging
- **[Logging Guide](tutorials/logging-guide.md)** - Comprehensive logging implementation guide
- **[API Reference](api/libs.md)** - Auto-generated documentation from code
- **[Tutorials](tutorials/docs-setup.md)** - Step-by-step guides

## Quick Start

```bash
# Clone the template
git clone https://github.com/your-username/new-python-repo.git my-project
cd my-project

# Install dependencies
uv sync --all-extras

# Run demos
./run_demo.sh

# Build documentation
uv run mkdocs serve
```

!!! tip "Pro Tip"
    Use `uv sync --extra docs` to install only documentation dependencies when you just want to work on docs.

