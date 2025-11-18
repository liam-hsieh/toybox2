# Import Patterns Guide

Understanding the two import approaches in this template.

## Overview

This template demonstrates two different approaches to organizing and importing Python modules, each with comprehensive logging implementations:

1. **Package-based imports** - Best for reusable libraries with module-level logging
2. **Direct module imports** - Best for simple utilities with hierarchical logging

Both patterns include production-ready logging configurations following Python best practices.

## Package-Based Imports (Demo 1)

### Structure
```
src/
├── libs/
│   ├── __init__.py           # Makes it a package
│   └── example_module1.py    # Your module
└── demo_app.py               # Uses package import
```

### Import Statement
```python
from libs.example_module1 import import_checking1
```

### Configuration in pyproject.toml
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/libs"]  # Include entire package
```

### When to Use

**Good for:**

- Multiple related modules
- Reusable library code
- Complex project structures
- Code you plan to distribute as a package
- Clear namespace separation

**Avoid when:**

- You have only one simple module
- Quick prototyping
- Simple scripts

### Example Implementation

```python title="src/libs/math_utils.py"
"""Math utility functions for the project."""

def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers to average
        
    Returns:
        Average of the numbers
    """
    return sum(numbers) / len(numbers)
```

```python title="src/libs/__init__.py"
"""Math utilities package."""

from .math_utils import add_numbers, calculate_average

__all__ = ["add_numbers", "calculate_average"]
```

```python title="src/my_app.py"
"""Example app using package imports."""

from libs import add_numbers, calculate_average
# or
from libs.math_utils import add_numbers

result = add_numbers(5, 3)
print(f"Result: {result}")
```

## Direct Module Imports (Demo 2)

### Structure
```
src/
└── demo_sub_app/
    ├── __init__.py
    ├── sub_demo_app.py       # Your main app
    └── example_module2.py    # Module in same directory
```

### Import Statement
```python
from example_module2 import import_checking2
```

### Configuration in pyproject.toml
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/demo_sub_app/example_module2.py"]  # Specific file
```

### When to Use

**Good for:**

- Single utility modules
- Simple helper functions
- Quick prototypes
- App-specific utilities
- Small projects

**Avoid when:**

- You have many related modules
- Building a reusable library
- Need clear namespace separation
- Complex project structure

### Example Implementation

```python title="src/myapp/helpers.py"
"""Helper functions for the app."""

def format_name(first: str, last: str) -> str:
    """Format a person's name.
    
    Args:
        first: First name
        last: Last name
        
    Returns:
        Formatted full name
    """
    return f"{first.title()} {last.title()}"

def validate_email(email: str) -> bool:
    """Simple email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email appears valid
    """
    return "@" in email and "." in email
```

```python title="src/myapp/main.py"
"""Main application file."""

from helpers import format_name, validate_email

# Use the helper functions
name = format_name("john", "doe")
is_valid = validate_email("john@example.com")

print(f"Name: {name}")
print(f"Email valid: {is_valid}")
```

## Comparison Table

| Feature | Package-Based | Direct Module |
|---------|---------------|---------------|
| **Complexity** | Higher | Lower |
| **Scalability** | Better | Limited |
| **Namespace** | Clear separation | Same directory |
| **Reusability** | High | Medium |
| **Setup effort** | More | Less |
| **Best for** | Libraries | Utilities |

## Migration Between Approaches

### From Direct to Package

1. Create a package directory:
   ```bash
   mkdir -p src/mypackage
   ```

2. Add `__init__.py`:
   ```python
   from .my_module import my_function
   ```

3. Move your module:
   ```bash
   mv src/myapp/helpers.py src/mypackage/helpers.py
   ```

4. Update imports:
   ```python
   # Before
   from helpers import my_function
   
   # After  
   from mypackage.helpers import my_function
   ```

5. Update `pyproject.toml`:
   ```toml
   packages = ["src/mypackage"]
   ```

### From Package to Direct

1. Move module to app directory:
   ```bash
   mv src/mypackage/helpers.py src/myapp/helpers.py
   ```

2. Update imports:
   ```python
   # Before
   from mypackage.helpers import my_function
   
   # After
   from helpers import my_function
   ```

3. Update `pyproject.toml`:
   ```toml
   packages = ["src/myapp/helpers.py"]
   ```

## Best Practices

!!! tip "Choose Based on Project Goals"
    - **Starting small?** Use direct imports
    - **Building a library?** Use package-based imports
    - **Not sure?** Start with direct, refactor to packages later

!!! warning "Common Pitfalls"
    - Forgetting `__init__.py` files for packages
    - Incorrect `pyproject.toml` configuration
    - Mixing both approaches inconsistently

!!! info "Pro Tip"
    You can use both approaches in the same project for different purposes!