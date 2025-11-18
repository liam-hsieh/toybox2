# Libs Package Overview

The `libs` package contains reusable utility modules organized as a proper Python package structure.

## Package Structure

```
src/libs/
├── __init__.py           # Package initialization
├── example_module1.py    # Example utilities with logging
└── logging_utils.py      # Advanced logging utilities
```

## Quick Examples

### Example Module 1 - Basic Package Functions

```python
from libs.example_module1 import import_checking1, calculate_sum

# Test package import
result = import_checking1("Hello World!")
print(result)
# Output: Import import_checking1 successful, and here is your input: Hello World!

# Calculate sum with logging
numbers = [1, 2, 3, 4, 5]
total = calculate_sum(numbers)
print(f"Sum: {total}")  # Output: Sum: 15.0
```

### Logging Utilities - Advanced Logging Features

```python
from libs.logging_utils import set_logger_w_obj_name, setup_development_logging

# Quick development logging setup
setup_development_logging(level=logging.DEBUG)

# Hierarchical function logging
def my_function():
    logger = set_logger_w_obj_name()
    logger.info("Function executing with hierarchical name")
    # Logger name: module.my_function
```

## Detailed API Documentation

For complete API documentation with all methods, parameters, and examples:

- **[Example Module 1](reference/libs/example_module1.md)** - Detailed API for package imports and utilities
- **[Logging Utils](reference/libs/logging_utils.md)** - Complete logging utilities API reference

## Usage Patterns

### When to Use This Package

- **Reusable utilities** across multiple applications
- **Library development** for distribution
- **Complex projects** requiring organized code structure
- **Professional logging** implementations

### Import Examples

```python
# Individual function imports
from libs.example_module1 import import_checking1

# Multiple imports
from libs.example_module1 import import_checking1, calculate_sum

# Module import
import libs.example_module1 as example

# Logging utilities
from libs.logging_utils import setup_development_logging
```