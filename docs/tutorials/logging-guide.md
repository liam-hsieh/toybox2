# Logging Guide

Comprehensive logging implementation following Python best practices with hierarchical logger patterns.

## Overview

This template implements a **hierarchical logger pattern** that provides:

- **Module-level logging** for general operations
- **Function-level logging** for granular debugging
- **Class-based logging** with multiple approaches
- **Entry point configuration** for different environments
- **Third-party library suppression** for clean output

## Architecture

```
new_python_repo                        # Root package logger
├── new_python_repo.libs               # Package modules
│   ├── new_python_repo.libs.example_module1
│   └── new_python_repo.libs.logging_utils
├── new_python_repo.demo_app           # Demo applications
└── new_python_repo.demo_sub_app       # Sub demo applications
    ├── new_python_repo.demo_sub_app.example_module2
    └── new_python_repo.demo_sub_app.sub_demo_app
```

**Key Principle**: Modules define loggers but never configure handlers/levels - configuration happens at entry points only.

## Implementation Patterns

### 1. Module-Level Logger Setup

All `.py` files follow this standard setup:

```python
import logging

# Configure module-level logger - NO handlers, NO setLevel
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
```

**Usage in functions:**
```python
def my_function(data):
    logger.info(f"Processing {len(data)} items")
    logger.debug(f"Data details: {data[:100]}...")
    return processed_data
```

### 2. Hierarchical Function-Level Logging

For detailed function-level tracing, use the `set_logger_w_obj_name()` utility:

```python
from libs.logging_utils import set_logger_w_obj_name

def process_data(input_file):
    logger = set_logger_w_obj_name()
    logger.info(f"Processing file: {input_file}")
    # Logger name: 'module_name.process_data'
```

**In class methods:**
```python
class AnalyticsEngine:
    def run_query(self, query: str):
        logger = set_logger_w_obj_name()
        logger.debug(f"Executing query: {query[:100]}...")
        # Logger name: 'module_name.AnalyticsEngine.run_query'
```

### 3. Class-Based Logging Approaches

The template demonstrates two class logging patterns:

#### Instance-Level Logger
```python
class ExampleClass:
    def __init__(self):
        self.logger = set_logger_w_obj_name(eliminate_init=True)
        # Logger name: 'module_name.ExampleClass'
    
    def method(self):
        self.logger.info("Using instance logger")
```

#### Method-Level Logger
```python
class ExampleClass:
    def method(self):
        logger = set_logger_w_obj_name()
        logger.info("Using method-specific logger")
        # Logger name: 'module_name.ExampleClass.method'
```

## Entry Point Configuration

### Streamlit Applications

Both demo apps include proper logging setup:

```python
# Configure logging for Streamlit app (only if not already configured)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Set levels for different components
    logging.getLogger('new_python_repo').setLevel(logging.INFO)
    logging.getLogger('streamlit').setLevel(logging.WARNING)
```

### Module Testing

All modules include `if __name__ == "__main__"` sections with configurable logging:

```python
if __name__ == "__main__":
    import sys
    import logging
    
    # Test-specific logging (terminal only, configurable level)
    logging.basicConfig(
        level=logging.DEBUG,  # Change to INFO/WARNING as needed
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )
    
    # Fine-tune specific loggers for debugging
    logging.getLogger('new_python_repo').setLevel(logging.DEBUG)
```

### Configuration Scripts

The `check_config.py` script demonstrates configuration-aware logging:

```python
# Configure logging for script execution
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors for CLI usage
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()],
    force=True
)

# Verbose mode for debugging
if sys.argv[1] == "--verbose":
    logging.getLogger().setLevel(logging.DEBUG)
    logger.info("Verbose mode enabled")
```

## Logging Utilities

### Advanced Setup Functions

The `libs.logging_utils` module provides convenience functions:

```python
from libs.logging_utils import setup_development_logging, setup_production_logging

# Quick development setup
setup_development_logging(level=logging.DEBUG)

# Production logging to file and console
setup_production_logging("/var/log/app/service.log")
```

### Hierarchical Logger Generation

```python
from libs.logging_utils import set_logger_w_obj_name

# In any function or method
logger = set_logger_w_obj_name()
# Automatically generates appropriate hierarchical name
```

## Testing the Logging System

### Individual Module Testing

Test modules with built-in logging support:

```bash
# Test package module with hierarchical logging
python src/libs/example_module1.py

# Test direct import module with class logging
python src/demo_sub_app/example_module2.py

# Test logging utilities
python src/libs/logging_utils.py

# Test configuration with verbose logging
python check_config.py --verbose
```

### Expected Output

When testing `example_module1.py`:
```
2025-11-17 17:32:25,589 - __main__ - INFO - Processing import check with input: Hello from module test!...
2025-11-17 17:32:25,590 - __main__ - DEBUG - Calculating sum for 5 items
2025-11-17 17:32:25,590 - __main__ - INFO - Sum calculation completed: 5 numbers, result=15.0
```

When testing `example_module2.py`:
```
2025-11-17 17:32:45,642 - __main__.ExampleClass.example_method - INFO - Example logging by method logger...
2025-11-17 17:32:45,642 - __main__.ExampleClass - INFO - Example logging by instance logger...
```

## Log Level Guidelines

| Level | Usage | Examples |
|-------|--------|----------|
| `DEBUG` | Detailed diagnostic information | Variable values, SQL queries, detailed flow |
| `INFO` | General operational information | Process started, completed, milestones |
| `WARNING` | Recoverable issues | Retrying connections, missing optional data |
| `ERROR` | Serious problems | Query failures, file not found |
| `CRITICAL` | System failures | Database unreachable, out of memory |

## Best Practices

### ✅ Do

- Use module-level loggers for general operations
- Use hierarchical loggers for granular debugging
- Configure logging at entry points only
- Include context in log messages
- Suppress noisy third-party libraries
- Use appropriate log levels

### ❌ Don't

- Configure handlers/levels in modules
- Use print statements instead of logging
- Log sensitive information
- Create overly verbose debug messages
- Forget to handle exceptions in logging code

## Integration Examples

### ETL Pipeline
```python
# etl_main.py
from libs.logging_utils import setup_production_logging
setup_production_logging("/var/log/etl/pipeline.log")

pipeline = ETLPipeline()
# All module logging automatically configured
```

### Data Analysis Script
```python
# analysis.py
from libs.logging_utils import setup_development_logging
setup_development_logging(level=logging.INFO)

# All imports will use properly configured logging
from libs.data_processor import analyze_data
```

### Web Service
```python
# api_service.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/api/service.log"),
        logging.StreamHandler()
    ]
)
```

This architecture ensures clean separation: modules stay configuration-agnostic, entry points control logging behavior, and developers get consistent, actionable log output across the entire application stack.