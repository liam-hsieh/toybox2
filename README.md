# New Python Project Template

This is a template repository for creating new Python projects with modern tooling and best practices, using [uv](https://github.com/astral-sh/uv) for fast dependency management.

## Features

- **Fast dependency management** with `uv` instead of pip/conda
- **Modern Python packaging** with `pyproject.toml` 
- **Flexible dependency groups** for development, testing, and optional features
- **Pre-configured project structure** with src layout
- **Professional documentation** with MkDocs + mkdocstrings
- **Two demo applications** showcasing different import patterns
- **Git integration** with comprehensive `.gitignore`
- **Ready for CI/CD** with standardized configuration

## Quick Start

### 1. Install uv

If you don't have `uv` installed yet:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Create Your New Project

1. **Use this template**: Click "Use this template" button or clone this repository
   ```bash
   git clone https://github.com/liam-hsieh/new-python-repo.git <your-new-project-name>
   ```
2. **Navigate to your project directory**:
   ```bash
   cd your-new-project-name
   ```
3. **Update project metadata** in `pyproject.toml`:
   - Change `name` from "new-python-repo" to your project name
   - Update `description`, `authors`, and other metadata
   - Modify `dependencies` and `optional-dependencies` as needed

### 3. Try the Demo Applications

**Run the included demo apps to understand different import patterns:**

```bash
# Run the demo selection script
./run_demo.sh

# Or run specific demos directly
./run_demo.sh 1    # Package-based imports
./run_demo.sh 2    # Direct module imports
```

## Demo Applications & Import Patterns

This template includes two demo applications that showcase different approaches to organizing and importing custom Python modules:

### Demo 1: Package-Based Imports (`src/demo_app.py`)
```python
from libs.example_module1 import import_checking1
```

**Best for:**
- Reusable libraries and packages
- Complex projects with multiple modules
- When you want to distribute your code as a package

**Structure:**
```
src/
├── libs/
│   ├── __init__.py           # Makes it a Python package
│   └── example_module1.py    # Your module code
└── demo_app.py               # Uses package import
```

**Configuration in pyproject.toml:**
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/libs"]  # Include entire libs package
```

### Demo 2: Direct Module Imports (`src/demo_sub_app/sub_demo_app.py`)
```python
from example_module2 import import_checking2
```

**Best for:**
- Simple utilities and standalone modules
- Single-file modules in the same directory
- Quick prototyping and simple scripts

**Structure:**
```
src/
└── demo_sub_app/
    ├── __init__.py
    ├── sub_demo_app.py       # Your main app
    └── example_module2.py    # Module in same directory
```

**pyproject.toml Configuration:**
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/demo_sub_app/example_module2.py"]  # Include specific file
```

###Choosing the Right Approach

| Scenario | Use Demo 1 (Package) | Use Demo 2 (Direct) |
|----------|---------------------|----------------------|
| **Multiple related modules** | Yes | No |
| **Single utility module** | No | Yes |
| **Plan to distribute as package** | Yes | No |
| **Quick prototype/script** | No | Yes |
| **Complex project structure** | Yes | No |
| **Simple directory structure** | No | Yes |

## Setting Up Your Project

### For Package-Based Approach (Recommended)

1. **Create your package structure:**
   ```bash
   mkdir -p src/mypackage
   touch src/mypackage/__init__.py
   ```

2. **Add your modules:**
   ```python
   # src/mypackage/utils.py
   def my_function():
       return "Hello from package!"
   ```

3. **Update pyproject.toml:**
   ```toml
   [tool.hatch.build.targets.wheel]
   packages = ["src/mypackage"]
   ```

4. **Import in your apps:**
   ```python
   from mypackage.utils import my_function
   ```

### For Direct Module Approach

1. **Create your app directory:**
   ```bash
   mkdir -p src/myapp
   touch src/myapp/__init__.py
   ```

2. **Add module in same directory:**
   ```python
   # src/myapp/helper.py
   def helper_function():
       return "Hello from helper!"
   ```

3. **Update pyproject.toml:**
   ```toml
   [tool.hatch.build.targets.wheel]
   packages = ["src/myapp/helper.py"]
   ```

4. **Import in your app:**
   ```python
   # src/myapp/main.py
   from helper import helper_function
   ```

### Converting Between Approaches

**From Direct to Package:**
1. Create a package directory with `__init__.py`
2. Move your module files into the package
3. Update imports to use package notation
4. Update pyproject.toml packages list

**From Package to Direct:**
1. Move module files to your app directory
2. Update imports to direct module names
3. Update pyproject.toml to list individual files

## Documentation with MkDocs

This template includes professional documentation setup using **MkDocs** with **Material theme** and **mkdocstrings** for automatic API documentation.

### Quick Documentation Setup

```bash
# Install documentation dependencies
uv sync --extra docs

# Start documentation server
uv run mkdocs serve

# Visit http://127.0.0.1:8000 to see your docs
```

### Features Included

- **Auto-generated API docs** from Python docstrings
- **Beautiful Material Design** theme with dark/light mode
- **Full-text search** functionality
- **Mobile-responsive** design
- **Live reload** during development
- **Code syntax highlighting**

### Documentation Structure

```
docs/
├── index.md                    # Homepage
├── getting-started/
│   ├── quick-start.md         # Installation & setup
│   ├── import-patterns.md     # Module organization guide
│   └── demos.md               # Demo applications guide
├── api/                       # Auto-generated API docs
│   ├── libs.md               # Package-based modules
│   └── demo-sub-app.md       # Direct import modules  
├── tutorials/
│   ├── docs-setup.md         # Documentation tutorial
│   └── adding-modules.md     # Development guides
└── gen_ref_pages.py          # Auto-generation script
```

### Writing Documentation

**Add Google-style docstrings to your code:**

```python
def calculate_total(items: list[float], tax_rate: float = 0.1) -> float:
    """Calculate total cost including tax.
    
    Args:
        items: List of item costs
        tax_rate: Tax rate as decimal (default: 0.1)
        
    Returns:
        Total cost including tax
        
    Example:
        >>> calculate_total([10.0, 20.0], 0.05)
        31.5
    """
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

**mkdocstrings automatically generates beautiful API documentation from these docstrings!**

### Customization

- **Theme colors** and styling in `mkdocs.yml`
- **Navigation structure** for your content
- **Plugin configuration** for advanced features
- **Custom CSS** for branded appearance

### Deployment Options

#### GitHub Pages (Automated if enables)

**Configurable deployment!** You can easily enable/disable GitHub Pages deployment:

**Quick Toggle Commands:**
```bash
# Enable GitHub Pages deployment
./manage_github_pages.sh enable

# Disable GitHub Pages deployment  
./manage_github_pages.sh disable

# Check current status
./manage_github_pages.sh status
```

**Manual Configuration:**
Edit `project.toml` to control deployment:
```toml
[documentation]
github_pages_enabled = true  # Set to false to disable
```

**Setup Steps:**
1. **Enable GitHub Pages in your repository:**
   - Go to repository Settings → Pages  
   - Source: "GitHub Actions"
   - Save settings

2. **Configure deployment (optional):**
   ```bash
   ./manage_github_pages.sh enable  # Enable automatic deployment
   ```

3. **Push your changes:**
   ```bash
   git add .
   git commit -m "Setup documentation with configurable GitHub Pages"
   git push origin main
   ```

4. **Access your docs:**
   - URL: `https://your-username.github.io/your-repo-name`
   - Auto-updates when `github_pages_enabled = true`
   - Deployment skipped when `github_pages_enabled = false`

**Features:**
- Easy on/off toggle via management script
- Configuration file (`project.toml`) controls deployment
- Workflow respects settings and skips deployment when disabled
- Status checking to see current configuration

**GitHub Actions workflow included:** `.github/workflows/docs.yml`

#### Other Platforms
- **Netlify** or **Vercel** (connect repository)
- **Custom server** (static HTML output with `mkdocs build`)

See the [Documentation Setup Tutorial](docs/tutorials/docs-setup.md) for complete configuration details.

### 4. Initialize the Environment

```bash
# Create virtual environment and install dependencies
uv sync

# Or install with development tools
uv sync --extra dev

# Install everything (all optional dependencies)
uv sync --all-extras
```

### 4. Activate the Environment

```bash
# Activate the virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Or run commands directly with uv
uv run python your_script.py
# when the project is built on top of those frameworks such like streamlit, run it similarly as usual but in uv
uv run streamlit run app.py
```

## Dependency Management with uv

### Core Commands

```bash
# Install core dependencies only
uv sync

# Install with specific optional dependency groups
uv sync --extra dev
uv sync --extra enhanced
uv sync --extra name-of-subproject

# Install multiple groups
uv sync --extra dev --extra enhanced

# Install everything
uv sync --all-extras
```

### Adding Dependencies

uv automatically updates the dependency sections in `pyproject.toml` when you add packages, while you maintain the project metadata and configuration manually.

```bash
# Add a new core dependency
uv add pandas

# Add to development dependencies
uv add --optional-group dev pytest

# Add to a custom group
uv add --optional-group enhanced streamlit-authenticator

# Add with version constraints
uv add "numpy>=1.21.0,<2.0"
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv sync --upgrade-package pandas
```

## Project Structure

```
your-project/
├── .git/                   # Git repository
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── pyproject.toml         # Project configuration and dependencies
├── .venv/                 # Virtual environment (created by uv sync)
└── src/                   # Source code directory
    ├── __init__.py
    ├── main.py           # Your main application
    ├── shared/           # Shared modules
    └── ...
```

## Dependency Groups

The template includes several pre-configured dependency groups:

### Core Dependencies
Always installed with `uv sync`:
- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `pyyaml` - YAML parsing
- `requests` - HTTP client
- And more...

### Optional Groups

**Development (`dev`)**: Uncomment in `pyproject.toml` to enable
- `pytest` - Testing framework
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking
- `pre-commit` - Git hooks

**Enhanced (`enhanced`)**: Uncomment in `pyproject.toml` to enable
- `streamlit-authenticator` - Authentication
- `streamlit-option-menu` - Enhanced UI
- `duckdb` - In-memory analytics

**Custom groups**: Define your own based on project needs

## Common Workflows

### Starting Development

```bash
# 1. Clone/create your project
git clone <your-repo-url>
cd your-project

# 2. Install dependencies
uv sync --extra dev

# 3. Start coding in src/
```

### Running Your Application

```bash
# Run with uv (recommended)
uv run python src/main.py
uv run streamlit run app.py

# Or activate environment first
source .venv/bin/activate
python src/main.py
streamlit run app.py
```

### Testing

```bash
# Install test dependencies
uv sync --extra dev

# Run tests
uv run pytest
```

## Why uv?

- **Speed**: 10-100x faster than pip for dependency resolution
- **Reliability**: Deterministic, reproducible installations
- **Modern**: Built with Rust, designed for Python 3.12+
- **Compatible**: Drop-in replacement for pip/pip-tools
- **All-in-one**: Manages Python versions, virtual environments, and dependencies

## Configuration Details

### pyproject.toml Structure

The `pyproject.toml` file contains:
- **Project metadata**: name, version, description, authors
- **Core dependencies**: Required packages
- **Optional dependencies**: Grouped by feature/purpose
- **Build configuration**: For packaging and distribution
- **Tool configuration**: Settings for linters, formatters, etc.

### Environment Management

uv automatically:
- Creates `.venv/` directory for virtual environment
- Manages Python version compatibility
- Handles dependency resolution and conflict detection
- Creates lock files for reproducible builds

## Customization

1. **Update project metadata** in `pyproject.toml`
2. **Modify dependencies** for your specific needs
3. **Uncomment tool configurations** (black, mypy, pytest) as needed
4. **Add your source code** in the `src/` directory
5. **Update this README** with project-specific information

## Migration from pip/conda

If you're coming from pip or conda:

```bash
# From requirements.txt
uv add $(cat requirements.txt)

# From conda environment
conda list --export > conda-deps.txt
# Then manually add relevant packages with uv add
```

## Getting Help

- [uv documentation](https://github.com/astral-sh/uv)
- [Python packaging guide](https://packaging.python.org/)
- [pyproject.toml reference](https://pep.python.org/pep-0621/)

## Logging Setup

This template implements a comprehensive logging system following Python logging best practices with a **hierarchical logger pattern**. 

### Architecture Overview

```
new_python_repo                    # Root package logger
├── new_python_repo.libs          # Package modules
├── new_python_repo.demo_app       # Demo applications
└── new_python_repo.logging_utils  # Logging utilities
```

**Key Principle**: Modules define loggers but never configure handlers/levels - configuration happens at entry points only.

### Module-Level Logging Pattern

All `.py` files follow this standard setup:

```python
import logging

# Configure module-level logger - NO handlers, NO setLevel
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def my_function():
    logger.info("Function executed successfully")
    logger.debug("Detailed debug information")
```

### Entry Point Configuration

**For Streamlit apps** (already configured in demo apps):
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

**For module testing** (included in all modules):
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
```

### Advanced Logging Utilities

The template includes `src/libs/logging_utils.py` with enhanced functionality:

```python
from libs.logging_utils import set_logger_w_obj_name, setup_development_logging

# Function-level hierarchical logging
def process_data(data):
    logger = set_logger_w_obj_name()  # Creates: 'module.function_name'
    logger.info("Processing data")

# Class method hierarchical logging  
class AnalyticsEngine:
    def run_query(self, query):
        logger = set_logger_w_obj_name()  # Creates: 'module.ClassName.method_name'
        logger.info("Running query")

# Quick development setup
setup_development_logging(level=logging.DEBUG)
```

### Testing the Logging System

Test individual modules with built-in logging:
```bash
# Test package module with hierarchical logging
python src/libs/example_module1.py

# Test direct import module with validation logging  
python src/demo_sub_app/example_module2.py

# Test logging utilities
python src/libs/logging_utils.py

# Test configuration script with verbose logging
python check_config.py --verbose
```

### When to Use Each Approach

| Context | Use Module Logger | Use Hierarchical Logger |
|---------|------------------|------------------------|
| **General operations** | `logger = logging.getLogger(__name__)` | No |
| **Granular debugging** | No | `logger = set_logger_w_obj_name()` |
| **Complex workflows** | No | Yes |
| **Function-level tracing** | No | Yes |
| **Performance monitoring** | Yes | Yes |

### Benefits of This Approach

- **Clean separation**: Modules stay configuration-agnostic
- **Flexible control**: Entry points control logging behavior  
- **Hierarchical tracking**: Detailed function/method-level tracing
- **Production ready**: Proper log levels and third-party suppression
- **Development friendly**: Easy debugging with detailed output

---

**Happy coding!** 
