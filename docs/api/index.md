# API Reference

Welcome to the API reference documentation for the New Python Repo Template.

## Documentation Structure

This API documentation is organized in two levels:

### 📋 **Overview Pages** (This Section)
- **Curated introductions** with examples and usage patterns
- **Quick start guides** for each package/module
- **Best practices** and common use cases
- **High-level explanations** of functionality

### 🔍 **Detailed Reference** (Auto-Generated)
- **Complete API documentation** extracted from source code
- **All functions, classes, and methods** with full signatures
- **Parameter details** and return type information
- **Source code links** for implementation details

## Available Packages

### [Libs Package](libs.md)
**Package-based imports for reusable utilities**

- `example_module1` - Basic package functions with logging
- `logging_utils` - Advanced logging utilities and setup functions

**Quick Example:**
```python
from libs.example_module1 import import_checking1, calculate_sum
from libs.logging_utils import setup_development_logging
```

### [Demo Sub App](demo-sub-app.md)
**Direct imports for simple utilities**

- `example_module2` - Advanced features with hierarchical logging
- `sub_demo_app` - Streamlit demo application
- `ExampleClass` - Class-based logging demonstrations

**Quick Example:**
```python
from example_module2 import import_checking2, process_text, ExampleClass
```

## Getting Started

1. **Choose your import pattern**:
   - Use **package imports** (`libs.*`) for reusable libraries
   - Use **direct imports** for simple utilities in the same directory

2. **Set up logging** (recommended):
   ```python
   from libs.logging_utils import setup_development_logging
   setup_development_logging(level=logging.INFO)
   ```

3. **Explore the examples**:
   - Run the demo apps: `./run_demo.sh`
   - Test modules directly: `python src/libs/example_module1.py`

## Navigation Tips

- **Start with overview pages** for context and examples
- **Use detailed reference** for complete API information
- **Follow the links** between overview and detailed docs
- **Run the demos** to see everything in action

## For Developers

This documentation is automatically generated from source code using MkDocs + mkdocstrings. To rebuild:

```bash
uv sync --extra docs
uv run mkdocs build
```

The hybrid approach combines:
- Manual curation (overview pages)
- Automatic generation (detailed reference)
- Best of both worlds for different use cases