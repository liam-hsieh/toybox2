# Demo Sub App Overview

The demo sub app demonstrates direct module imports and advanced logging patterns.

## Module Structure

```
src/demo_sub_app/
├── __init__.py
├── sub_demo_app.py       # Streamlit demo application
└── example_module2.py    # Direct import module with advanced features
```

## Key Features

### Advanced Logging Demonstrations

- **Hierarchical logger names** with `set_logger_w_obj_name()`
- **Class-based logging** with multiple approaches
- **Input validation** with comprehensive error context
- **Text analysis** with performance metrics

### Example Usage

```python
# Direct imports (when in same directory)
from example_module2 import import_checking2, process_text, validate_input

# Test direct import
result = import_checking2("Direct import test")
print(result)

# Text analysis with logging
text = "Sample text for analysis"
analysis = process_text(text)
print(f"Words: {analysis['word_count']}, Chars: {analysis['char_count']}")

# Input validation
is_valid = validate_input("test input", min_length=5)
print(f"Valid: {is_valid}")
```

### Class-Based Logging Example

```python
from example_module2 import ExampleClass

# Demonstrates two logging approaches
obj = ExampleClass()
result = obj.example_method("test data")
# Shows both instance-level and method-level logging
```

## Detailed API Documentation

For complete API documentation:

- **[Sub Demo App](reference/demo_sub_app/sub_demo_app.md)** - Streamlit application details
- **[Example Module 2](reference/demo_sub_app/example_module2.md)** - Complete API for direct imports and logging

## When to Use This Pattern

- **Simple utilities** in the same directory
- **Quick prototyping** without complex package structure
- **Single-file modules** with specific functionality
- **Advanced logging** requirements with hierarchical names

## Running the Demo

```bash
# Install dependencies
uv sync --all-extras

# Run the Streamlit demo
uv run streamlit run src/demo_sub_app/sub_demo_app.py --server.port 8521

# Test module directly
uv run python src/demo_sub_app/example_module2.py
```