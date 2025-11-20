# Automatic API Documentation

Toybox 2.0 supports automatic generation of API documentation from Python source code using MkDocs with mkdocstrings.

## Overview

The API documentation system automatically:

- Scans configured source directories for Python files
- Generates markdown documentation from docstrings
- Creates cross-referenced API pages
- Integrates with your existing documentation

## Configuration

###Enable API Documentation Generation

Edit `project.toml`:

```toml
[documentation]
# Enable automatic API documentation generation
auto_generate_api_docs = true

# Specify source directories to document
api_source_dirs = [
    "apps/shared",
    "apps/demo_app",
    "apps/utilities",
]
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `auto_generate_api_docs` | boolean | Enable/disable API docs generation |
| `api_source_dirs` | list | List of directories to scan for Python files |

## Adding New Source Directories

### Step 1: Update Configuration

Add your new app directory to `project.toml`:

```toml
[documentation]
api_source_dirs = [
    "apps/shared",
    "apps/demo_app",
    "apps/my_new_app",  # Add your new app
]
```

### Step 2: Rebuild Documentation

```bash
# Clean previous build
rm -rf site/

# Rebuild with new API docs
uv run mkdocs build

# Or serve locally
uv run mkdocs serve
```

The API documentation will automatically be generated for all Python files in the specified directories.

## Writing Documentation-Friendly Code

### Use Google-Style Docstrings

```python
def calculate_metrics(data: pd.DataFrame, threshold: float = 0.5) -> dict:
    """Calculate performance metrics from data.
    
    Args:
        data: Input dataframe containing performance data
        threshold: Minimum threshold for metric calculation
    
    Returns:
        Dictionary containing calculated metrics
    
    Raises:
        ValueError: If data is empty or threshold is invalid
    
    Example:
        >>> df = pd.DataFrame({'score': [0.8, 0.6, 0.3]})
        >>> metrics = calculate_metrics(df, threshold=0.5)
        >>> print(metrics['accuracy'])
        0.75
    """
    pass
```

## Best Practices

- Write docstrings for all public functions and classes
- Use Google-style docstrings consistently
- Include examples in docstrings
- Document parameters with type hints

## Related Documentation

- **[Documentation Testing](documentation-testing.md)** - Test documentation locally
- **[Production Server](documentation-production-server.md)** - Deploy documentation
