# Sub-App Development Guide for Toybox 2.0

This guide explains how to develop standalone Streamlit applications that can be seamlessly integrated into the Toybox 2.0 multi-page framework while remaining independently executable.

## Table of Contents
- [Core Principles](#core-principles)
- [Directory Structure](#directory-structure)
- [Package Configuration](#package-configuration)
- [Import Patterns](#import-patterns)
- [Development Workflow](#development-workflow)
- [Integration Checklist](#integration-checklist)
- [Troubleshooting](#troubleshooting)

---

## Core Principles

### Design Philosophy

**Dual-Mode Execution:** Each sub-app should work in two modes:
1. **Standalone Mode:** Run directly for development (`streamlit run my_app.py`)
2. **Integrated Mode:** Run through Toybox navigation (`toybox.py` → `st.Page()`)

**Key Requirements:**
- No code changes needed between standalone and integrated modes
- Custom modules must be importable in both modes
- Proper package structure in `pyproject.toml`
- Consistent import patterns

---

## Directory Structure

### Recommended Structure

```
apps/
├── shared/                    # Shared utilities (always top-level)
│   ├── __init__.py
│   ├── auth.py
│   ├── utils.py
│   └── components.py
│
├── my_new_app/               # Your new sub-app
│   ├── __init__.py           # Required for package
│   ├── main_app.py           # Main Streamlit entry point
│   ├── helper_app.py         # Additional pages (optional)
│   └── my_modules/           # Custom modules for this app
│       ├── __init__.py
│       ├── data_processor.py
│       └── utilities.py
│
└── another_app/              # Another example
    ├── __init__.py
    ├── app.py
    └── lib/
        ├── __init__.py
        └── functions.py
```

### Structure Rules

1. **Always include `__init__.py`** in every directory that should be a package
2. **Keep app-specific modules nested** under the app directory
3. **Use descriptive names** for module directories (`my_modules`, `lib`, `utils`, etc.)
4. **Separate concerns:** Main app file + module directory for logic

---

## Package Configuration

### Understanding `pyproject.toml` Packages

The `packages` list in `[tool.hatch.build.targets.wheel]` defines **top-level packages** for installation.

#### Rule of Thumb

**What you list in `packages` = How you import it**

```toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",           # Import as: from shared.xxx import ...
    "apps/my_new_app",       # Import as: from my_new_app.xxx import ...
]
```

### Configuration Examples

#### Example 1: Simple App with Custom Modules

**Directory:**
```
apps/my_app/
├── __init__.py
├── app.py
└── helpers/
    ├── __init__.py
    └── functions.py
```

**Configuration:**
```toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",        # Always include shared
    "apps/my_app",        # Include the entire app package
]
```

**Import in `app.py`:**
```python
# Import from shared (top-level)
from shared.components import create_page_header

# Import from own modules (relative to my_app)
from my_app.helpers.functions import process_data
```

#### Example 2: App with Multiple Sub-packages

**Directory:**
```
apps/data_processor/
├── __init__.py
├── main.py
├── analysis/
│   ├── __init__.py
│   └── analyzer.py
└── visualization/
    ├── __init__.py
    └── plotter.py
```

**Configuration:**
```toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",
    "apps/data_processor",  # One entry for the entire app
]
```

**Import in `main.py`:**
```python
from shared.utils import load_config
from data_processor.analysis.analyzer import analyze_data
from data_processor.visualization.plotter import create_plot
```

#### Example 3: Legacy App Requiring Path Manipulation

For apps with non-standard structure or that can't be easily packaged:

**In your app file (`apps/legacy_app/app.py`):**
```python
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Now can import from same directory
from my_module import my_function
```

**Configuration:**
```toml
# Don't add to packages if using sys.path method
packages = [
    "apps/shared",
    # "apps/legacy_app",  # Omit this
]
```

---

## Import Patterns

### Pattern 1: Import from Shared Utilities (Recommended)

**Always works because `shared` is a top-level package:**

```python
# In any app file
from shared.auth import ToyboxAuth
from shared.utils import load_config, get_user_role
from shared.components import create_page_header, display_info_message
```

### Pattern 2: Import from Own App Modules (Preferred)

**When your app is in `packages`:**

```python
# In apps/my_app/main.py
import streamlit as st
from my_app.modules.processor import process_data
from my_app.modules.validator import validate_input
```

**Testing standalone:**
```bash
cd apps/my_app
uv run streamlit run main.py  # Works!
```

**Running through Toybox:**
```python
# In toybox.py via st.Page
st.Page("apps/my_app/main.py", ...)  # Works!
```

### Pattern 3: Hybrid Approach (Maximum Compatibility)

**For maximum flexibility during development:**

```python
# In apps/my_app/main.py
import sys
from pathlib import Path

# Ensure imports work both ways
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    # Try package import first (integrated mode)
    from my_app.modules.processor import process_data
except ImportError:
    # Fall back to direct import (standalone mode)
    from modules.processor import process_data
```

### Pattern 4: Relative Imports (Not Recommended)

**Avoid relative imports for Streamlit apps:**

```python
# ❌ Don't do this - breaks in Streamlit navigation
from .modules.processor import process_data
from ..shared.utils import load_config
```

**Why it fails:** Streamlit executes pages without proper package context, causing `ImportError: attempted relative import with no known parent package`.

---

## Development Workflow

### Step 1: Create Your App Structure

```bash
cd /opt/projects/toybox2/apps

# Create your app directory
mkdir -p my_new_app/modules

# Create necessary files
touch my_new_app/__init__.py
touch my_new_app/main_app.py
touch my_new_app/modules/__init__.py
touch my_new_app/modules/functions.py
```

### Step 2: Develop Standalone

```python
# apps/my_new_app/main_app.py
import streamlit as st
from my_new_app.modules.functions import my_function

st.title("My New App")
result = my_function()
st.write(result)
```

**Test standalone:**
```bash
cd apps/my_new_app
uv run streamlit run main_app.py --server.port 8501
```

### Step 3: Update Configuration Files

#### A. Add to `pyproject.toml`

```toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",
    "apps/my_new_app",  # Add your app here
]
```

#### B. Add to `config/projects.yaml`

```yaml
projects:
  my_new_app:
    name: "My New Application"
    description: "Description of what your app does"
    icon: "🚀"
    apps:
      main:
        title: "My New App"
        description: "Main application interface"
        icon: "🚀"
        path: "apps/my_new_app/main_app.py"
```

#### C. Add to `config/navigation.yaml`

```yaml
sections:
  utilities:  # Or create a new section
    title: "🛠️ Utilities"
    pages:
      - my_new_app  # Add your app key here

roles:
  admin:
    sections:
      - utilities  # Ensure admin has access
```

### Step 4: Install and Test Integrated

```bash
# Reinstall with your new app
cd /opt/projects/toybox2
uv sync --all-extras

# Test through Toybox
uv run streamlit run toybox.py
```

### Step 5: Verify Dual-Mode Operation

```bash
# Test 1: Standalone mode
cd apps/my_new_app
uv run streamlit run main_app.py
# ✅ Should work

# Test 2: Integrated mode
cd /opt/projects/toybox2
uv run streamlit run toybox.py
# ✅ Navigate to your app, should work
```

---

## Integration Checklist

### Before Integration

- [ ] App has `__init__.py` in all package directories
- [ ] Custom modules are under the app directory
- [ ] Imports use package-based paths (`from my_app.modules import ...`)
- [ ] App runs successfully standalone
- [ ] No relative imports (`from .module import ...`)

### Configuration Updates

- [ ] Added app to `pyproject.toml` packages list
- [ ] Added project definition to `config/projects.yaml`
- [ ] Added app to appropriate section in `config/navigation.yaml`
- [ ] Assigned to appropriate user roles in `config/navigation.yaml`
- [ ] Ran `uv sync --all-extras` after changes

### Testing Validation

- [ ] Standalone execution works: `cd apps/my_app && streamlit run app.py`
- [ ] Toybox execution works: Navigate to app through Toybox UI
- [ ] No import errors in either mode
- [ ] Shared utilities import correctly
- [ ] Custom modules import correctly
- [ ] All functionality works in both modes

---

## Troubleshooting

### Issue 1: `ModuleNotFoundError: No module named 'my_app'`

**Cause:** App not in `packages` list or not installed.

**Solution:**
```toml
# Add to pyproject.toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/my_app",  # Add this
]
```

```bash
# Reinstall
uv sync --all-extras
```

### Issue 2: `ImportError: attempted relative import with no known parent package`

**Cause:** Using relative imports.

**Solution:** Change to absolute imports:
```python
# ❌ Don't do this
from .modules.functions import my_function

# ✅ Do this instead
from my_app.modules.functions import my_function
```

### Issue 3: Works Standalone but Fails in Toybox

**Cause:** Import paths assume current directory context.

**Solution:** Use package-based imports matching your `pyproject.toml`:
```python
# If packages = ["apps/my_app"]
from my_app.modules.functions import my_function
```

### Issue 4: Works in Toybox but Fails Standalone

**Cause:** Missing `sys.path` setup or wrong import structure.

**Solution:** Add path setup for standalone execution:
```python
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))
```

### Issue 5: Import Works Sometimes but Not Always

**Cause:** Module name conflicts between installed package and filesystem.

**Solution:** Ensure consistent import paths. If `packages = ["apps/my_app"]`:
```python
# Always use full path from package root
from my_app.modules.functions import my_function

# Not just:
from modules.functions import my_function  # Ambiguous!
```

---

## Best Practices Summary

### DO ✅

1. **Use package-based imports** matching your `pyproject.toml` configuration
2. **Include `__init__.py`** in all package directories
3. **Keep modules under app directory** (e.g., `apps/my_app/modules/`)
4. **Test both standalone and integrated** before marking complete
5. **Use absolute imports** from package root
6. **Add your app to `packages` list** in `pyproject.toml`
7. **Update all three config files** (pyproject.toml, projects.yaml, navigation.yaml)

### DON'T ❌

1. **Don't use relative imports** (`from .module import ...`)
2. **Don't put modules outside app directory** without proper packaging
3. **Don't forget `__init__.py`** files
4. **Don't skip `uv sync`** after configuration changes
5. **Don't assume imports work without testing both modes**
6. **Don't install sub-packages separately** (install parent package instead)
7. **Don't mix import styles** within the same app

---

## Quick Reference

### Command Cheat Sheet

```bash
# Create new app structure
mkdir -p apps/my_app/modules
touch apps/my_app/{__init__.py,app.py}
touch apps/my_app/modules/__init__.py

# Test standalone
cd apps/my_app && uv run streamlit run app.py

# Install after config changes
cd /opt/projects/toybox2 && uv sync --all-extras

# Test integrated
cd /opt/projects/toybox2 && uv run streamlit run toybox.py

# Check installed packages
uv pip list | grep toybox
```

### Import Template

```python
# Standard template for new apps
import streamlit as st
import sys
from pathlib import Path

# Import from shared utilities
from shared.components import create_page_header
from shared.utils import load_config

# Import from your app modules (package-based)
from my_app.modules.processor import process_data
from my_app.modules.validator import validate_input

# Your app code here
st.title("My App")
```

### Configuration Template

```toml
# In pyproject.toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",
    "apps/my_app",  # Your app
]
```

```yaml
# In config/projects.yaml
projects:
  my_app:
    name: "My Application"
    description: "What it does"
    icon: "🚀"
    apps:
      main:
        title: "My App"
        description: "Main interface"
        icon: "🚀"
        path: "apps/my_app/app.py"
```

```yaml
# In config/navigation.yaml
sections:
  my_section:
    title: "My Section"
    pages:
      - my_app

roles:
  admin:
    sections:
      - my_section
```

---

## Example: Complete New App

See `apps/demo_app/` for a complete working example demonstrating:
- Proper package structure
- Dual-mode execution
- Package-based imports
- Integration with Toybox navigation

**Study these files:**
- `apps/demo_app/demo_app1.py` - Main application
- `apps/demo_app/demo_package/` - Module structure
- Configuration in `config/projects.yaml` and `config/navigation.yaml`

---

## Getting Help

If you encounter issues:

1. **Check this guide** - Most common issues are covered
2. **Review demo apps** - Working examples in `apps/demo_app/`
3. **Verify configuration** - Ensure all three config files are updated
4. **Test incrementally** - Standalone first, then integrated
5. **Check imports** - Match your `packages` configuration

**Remember:** The goal is **zero code changes** between development and integration!
