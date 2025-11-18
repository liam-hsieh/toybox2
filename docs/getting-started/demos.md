# Demo Applications

Explore the interactive demo applications included in this template.

## Overview

This template includes two Streamlit demo applications that showcase different Python module import patterns and comprehensive logging implementations. The demos provide hands-on examples of how to structure your code with proper logging practices.

### Logging Architecture

Both demos implement:

- **Module-level logging** configuration
- **Streamlit-specific** logging setup
- **Third-party library** log suppression
- **Function-level tracing** with detailed context
- **Error handling** with comprehensive logging

See the [Logging Guide](../tutorials/logging-guide.md) for detailed implementation patterns.

## Logging Benefits

Both demos demonstrate production-ready logging that provides:

- **Debugging capabilities** - Trace execution flow and identify issues
- **Performance monitoring** - Track function execution times and data processing
- **Error tracking** - Comprehensive error context and stack traces
- **Operational visibility** - Monitor application behavior in production
- **Development efficiency** - Quick problem identification and resolution

### Testing Logging

Each module can be run independently to demonstrate logging:

```bash
# Test package-based module logging
python src/libs/example_module1.py

# Test direct import module with hierarchical logging
python src/demo_sub_app/example_module2.py

# Test logging utilities
python src/libs/logging_utils.py
```

## Quick Start

### Using the Demo Script

The easiest way to run demos is using the provided script:

```bash
# Interactive selection with detailed explanations
./run_demo.sh

# Run specific demo directly
./run_demo.sh 1    # Package-based imports demo
./run_demo.sh 2    # Direct module imports demo
```

### Manual Execution

You can also run demos manually:

```bash
# Install dependencies
uv sync --all-extras

# Run demo 1 (package-based)
uv run streamlit run src/demo_app.py --server.port 8521

# Run demo 2 (direct imports)  
uv run streamlit run src/demo_sub_app/sub_demo_app.py --server.port 8521
```

## Demo 1: Package-Based Imports

**File**: `src/demo_app.py`  
**Port**: 8521  
**Import pattern**: `from libs.example_module1 import import_checking1`

### Features Demonstrated

- **Package structure** with `libs/` directory
- **Proper `__init__.py`** files for Python packages  
- **Reusable modules** organized as packages
- **Clean namespace** separation
- **Scalable architecture** for larger projects

### Code Structure

```
src/
├── libs/
│   ├── __init__.py           # Package initialization
│   └── example_module1.py    # Module with utilities
└── demo_app.py               # Streamlit app
```

### Key Functions

The demo showcases these functions from `libs.example_module1`:

- `import_checking1()` - Import verification with detailed logging
- `calculate_sum()` - Mathematical operations with error handling and logging

### Logging Features

- **Module-level logging** with proper logger configuration
- **Function-level logging** with input/output tracing
- **Error handling** with detailed logging context
- **Configurable log levels** for debugging

**View logging output:**
```bash
# Run module directly to see logging in action
python src/libs/example_module1.py
```

### When to Use This Pattern

Perfect for:

- Building reusable libraries
- Complex projects with multiple modules
- Code you plan to distribute as packages
- Clear separation of concerns

## Demo 2: Direct Module Imports

**File**: `src/demo_sub_app/sub_demo_app.py`  
**Port**: 8521  
**Import pattern**: `from example_module2 import import_checking2`

### Features Demonstrated

- **Direct imports** from same directory
- **Simple module structure** 
- **Quick prototyping** approach
- **Minimal configuration** needed
- **Hierarchical logging** with `set_logger_w_obj_name()`
- **Class-based logging** demonstrations
- **Advanced text analysis** with logging metrics

### Key Functions

The demo showcases these functions from `example_module2`:

- `import_checking2()` - Direct import verification
- `process_text()` - Text analysis with detailed logging
- `validate_input()` - Input validation with warning logs
- `ExampleClass.example_method()` - Class method logging patterns

### Logging Features

- **Hierarchical logger names** for function and class tracking
- **Multiple logging approaches** within classes
- **Input validation logging** with detailed context
- **Performance metrics** in text processing

**View advanced logging:**
```bash
# Run module directly to see hierarchical logging
python src/demo_sub_app/example_module2.py
```

### Code Structure

```
src/
└── demo_sub_app/
    ├── __init__.py
    ├── sub_demo_app.py       # Streamlit app
    └── example_module2.py    # Direct import module
```

### Key Functions

The demo showcases these functions from `example_module2`:

- `import_checking2()` - Import verification
- `process_text()` - Text analysis utilities
- `validate_input()` - Input validation helpers

### When to Use This Pattern

Perfect for:

- Simple utility modules
- Single-purpose applications
- Quick prototypes and scripts
- Small projects with minimal complexity

## Interactive Features

Both demos include:

### Import Testing
- Verify that module imports work correctly
- See the difference between import patterns
- Test function calls and responses

### Function Examples
- Real working examples of each function
- Input/output demonstrations
- Error handling showcase

### Learning Opportunities
- Compare code organization approaches
- Understand pyproject.toml configuration
- See practical Python packaging patterns

## Comparing the Approaches

| Aspect | Demo 1 (Package) | Demo 2 (Direct) |
|--------|------------------|------------------|
| **Import syntax** | `from libs.module import func` | `from module import func` |
| **File structure** | Package directories | Same directory |
| **Scalability** | High | Limited |
| **Setup complexity** | Medium | Low |
| **Best for** | Libraries | Utilities |

## Learning Paths

### For Beginners
1. Start with **Demo 2** (direct imports)
2. Understand basic module structure
3. Learn function organization
4. Practice with simple imports

### For Intermediate Users
1. Explore **Demo 1** (package-based)
2. Study package organization
3. Understand `__init__.py` files
4. Learn namespace management

### For Advanced Users
1. Compare both approaches
2. Understand pyproject.toml configuration
3. Study deployment differences
4. Choose the right pattern for your projects

## Next Steps

After exploring the demos:

1. **[Learn Import Patterns](import-patterns.md)** - Deep dive into module organization
2. **[API Reference](../api/libs.md)** - See auto-generated documentation
3. **[Documentation Setup](../tutorials/docs-setup.md)** - Learn to document your code

!!! tip "Experiment!"
    Try modifying the demo code to add your own functions and see how the import patterns work in practice.

!!! info "Real-world Usage"
    These patterns are used in production Python projects worldwide. Choose the one that fits your project's needs and complexity level.