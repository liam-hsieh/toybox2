# Copilot Instructions for New Python Repo Template

## Project Architecture

This is a **modern Python project template** using `uv` for fast dependency management with two distinct import patterns:

### Import Patterns
- **Package-based imports** (`src/libs/`) - For reusable libraries with `__init__.py` files
- **Direct module imports** (`src/demo_sub_app/`) - For utilities in same directory

Key files demonstrating patterns:
- `src/demo_app.py` - Streamlit app using package imports (`from libs.example_module1 import`)
- `src/demo_sub_app/sub_demo_app.py` - App using direct imports (`from example_module2 import`)

## Logging Architecture (Critical)

**NEVER configure logging handlers/levels in modules** - only at entry points. Follow this pattern:

### Module Setup Pattern
```python
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Required in every module
```

### Function-Level Debugging
```python
from libs.logging_utils import set_logger_w_obj_name

def my_function():
    logger = set_logger_w_obj_name()  # Creates hierarchical name
    logger.info("Processing...")
    # Logger name becomes: module.ClassName.method_name
```

### Entry Point Configuration
- Streamlit apps: Check `if not logging.getLogger().handlers:` before setup
- Development: `setup_development_logging(level=logging.DEBUG)`
- Production: `setup_production_logging("/path/to/file.log")`

## Development Workflow

### Essential Commands
```bash
# Install dependencies (replaces pip install -r requirements.txt)
uv sync --all-extras

# Run demos to understand patterns
./run_demo.sh              # Interactive selection
./run_demo.sh 1            # Package-based demo
./run_demo.sh 2            # Direct import demo

# Test modules individually (they have built-in logging)
python src/libs/example_module1.py
python src/libs/logging_utils.py

# Documentation development
uv run mkdocs serve         # Live preview at http://127.0.0.1:8000
```

### Configuration Management
- `pyproject.toml` - Main project config with optional dependencies
- `project.toml` - Template-specific settings (GitHub Pages toggle)
- Use `uv sync --extra docs` for documentation development
- Run `./manage_github_pages.sh enable/disable` to toggle deployment

## Key Conventions

### File Organization
- `src/libs/` - Package modules with `__init__.py` (use package imports)
- `src/demo_sub_app/` - Direct modules in same directory (use direct imports)
- All modules include comprehensive `if __name__ == "__main__"` testing sections

### Documentation Pattern
- Auto-generated API docs via `mkdocstrings` from docstrings
- Use Google-style docstrings with proper type hints
- Manual pages in `docs/` directory with MkDocs Material theme

### Error Handling
Always include logging context in error handling:
```python
try:
    result = process_data(data)
    logger.info(f"Processed {len(data)} items successfully")
except Exception as e:
    logger.error(f"Processing failed: {e}")
    raise
```

## Integration Points

### Streamlit Integration
- Logging configured for Streamlit apps (suppress noisy libraries)
- Demo apps show proper setup patterns for web applications

### MkDocs Integration
- Automatic API documentation generation from docstrings
- GitHub Actions deployment (configurable via `project.toml`)
- Live development server with hot reload

## Testing Strategy

Run individual modules directly - they include comprehensive test suites:
- Test imports, logging, error handling, and performance metrics
- Use built-in `if __name__ == "__main__"` sections for validation
- Check `LOGGING_SUMMARY.md` for implementation examples

This template prioritizes **clean separation of concerns** where modules define loggers but never configure them, enabling flexible deployment across different environments.