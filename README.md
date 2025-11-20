# Toybox 2.0 - Multi-Page Streamlit Application Framework

**A modern, production-ready framework for building scalable multi-page Streamlit applications with role-based access control, dynamic navigation, and modular architecture.**

Built with [UV](https://github.com/astral-sh/uv) for blazing-fast dependency management and [Streamlit](https://streamlit.io/) native multipage navigation.

## Features

**Dynamic YAML-Based Navigation**
- Fully configuration-driven page routing
- No hardcoded navigation logic
- Automatic page generation from YAML files

**Role-Based Access Control**
- Multi-role support (admin, developer, analyst, viewer)
- Section-based permission system
- Configuration-driven authorization

**Modular Sub-App Architecture**
- Independent sub-applications with dual-mode execution
- Standalone and integrated operation modes
- Clean separation of concerns

**Modern Python Stack**
- UV package manager for 10-100x faster dependency resolution
- Python 3.12+ with modern `pyproject.toml` configuration
- Optional dependency groups for flexible installation

**Professional Documentation**
- MkDocs with Material theme
- Auto-generated API documentation
- Comprehensive development guides

## Quick Start

### 1. Install UV

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Install Dependencies

```bash
# Clone the repository
cd toybox2

# Install core dependencies
uv sync

# Or install with all optional features
uv sync --all-extras
```

### 3. Configure Authentication

Create `config/auth.yaml`:

```yaml
credentials:
  usernames:
    admin:
      email: admin@example.com
      name: Admin User
      password: $2b$12$...  # bcrypt hash
      role: admin
    developer:
      email: dev@example.com
      name: Developer User
      password: $2b$12$...
      role: developer

cookie:
  expiry_days: 30
  key: your_secret_key_here
  name: toybox_auth_cookie

preauthorized:
  emails:
    - admin@example.com
```

### 4. Configure Environment Variables (Optional)

For applications that need secrets (API keys, database credentials):

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env
```

Example `.env` content:

```bash
# Demo Application Variables
DEMO_API_KEY=your_api_key_here
DEMO_DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Email Configuration
SENDER=noreply@example.com
PSW=your_smtp_password
```

See the [Environment Variables Tutorial](https://liam-hsieh.github.io/toybox2/tutorials/environment-variables/) for details.

### 5. Run Toybox

```bash
# Run the main application
uv run --python 3.12 toybox.py

# Access at http://localhost:8501
```

## Architecture

### Directory Structure

```
toybox2/
├── config/
│   ├── projects.yaml         # Project and app definitions
│   ├── navigation.yaml       # Navigation structure and permissions
│   └── auth.yaml            # User credentials and roles
├── apps/
│   ├── shared/
│   │   ├── utils.py         # Dynamic navigation generator
│   │   └── constants.py     # Shared constants
│   ├── demo_app/            # Example sub-application
│   │   ├── main.py         # App entry point
│   │   └── utils.py        # App-specific utilities
│   └── welcome/             # Welcome page application
├── docs/                    # MkDocs documentation
├── toybox.py               # Main application entry point
├── pyproject.toml          # Project configuration
└── logging.ini             # Logging configuration
```

### Configuration System

#### 1. Projects Configuration (`config/projects.yaml`)

Defines available applications and their metadata:

```yaml
projects:
  welcome:
    name: "Welcome"
    apps:
      welcome_page:
        name: "Welcome"
        path: "apps/welcome/welcome.py"
        icon: "🏠"
        description: "Welcome to Toybox 2.0"

  demo_apps:
    name: "Demo Applications"
    apps:
      demo_app:
        name: "Demo App"
        path: "apps/demo_app/main.py"
        icon: "🎯"
        description: "Example Streamlit application"
```

#### 2. Navigation Configuration (`config/navigation.yaml`)

Defines role-based navigation structure:

```yaml
roles:
  admin:
    sections:
      - welcome
      - demo_apps
      - utilities
      - system
  developer:
    sections:
      - welcome
      - demo_apps
      - utilities
  analyst:
    sections:
      - welcome
      - demo_apps

sections:
  welcome:
    title: "🏠 Welcome"
    pages:
      - welcome.welcome_page
  demo_apps:
    title: "🎯 Demo Applications"
    pages:
      - demo_apps.demo_app
```

#### 3. Authentication Configuration (`config/auth.yaml`)

Manages user credentials and roles (see Quick Start section for format).

### Dynamic Navigation System

Navigation is completely configuration-driven:

```python
# apps/shared/utils.py
def generate_dynamic_navigation(role: str) -> list:
    """Generate navigation based on user role and YAML configuration."""
    
    # Load configuration files
    projects = yaml.safe_load(open('config/projects.yaml'))
    navigation = yaml.safe_load(open('config/navigation.yaml'))
    
    # Get authorized sections for role
    sections = navigation['roles'][role]['sections']
    
    # Build page list from configuration
    pages = []
    for section_key in sections:
        section = navigation['sections'][section_key]
        for page_key in section['pages']:
            project, app = page_key.split('.')
            app_config = projects['projects'][project]['apps'][app]
            
            pages.append(st.Page(
                page=app_config['path'],
                title=app_config['name'],
                icon=app_config['icon']
            ))
    
    return pages
```

**Key Benefits:**
- Zero hardcoded navigation logic
- Easy to add/remove pages via YAML edits
- Role-based access control without code changes
- Automatic icon and title management

## Sub-App Development

### Creating a New Sub-App

1. **Create app directory:**
   ```bash
   mkdir -p apps/my_new_app
   ```

2. **Create main application file (`apps/my_new_app/main.py`):**
   ```python
   import streamlit as st
   import sys
   from pathlib import Path
   
   # Add apps directory to sys.path for dual-mode execution
   if __name__ == "__main__":
       apps_dir = str(Path(__file__).parent.parent)
       if apps_dir not in sys.path:
           sys.path.insert(0, apps_dir)
   
   from shared.constants import APP_TITLE
   
   def main():
       st.title("My New App")
       st.write("Application content here")
   
   if __name__ == "__main__":
       # Standalone mode
       main()
   else:
       # Integrated mode (called by Streamlit navigation)
       main()
   ```

3. **Add to `config/projects.yaml`:**
   ```yaml
   projects:
     utilities:  # Or create new section
       name: "Utilities"
       apps:
         my_new_app:
           name: "My New App"
           path: "apps/my_new_app/main.py"
           icon: "🔧"
           description: "Description of my app"
   ```

4. **Add to `config/navigation.yaml`:**
   ```yaml
   sections:
     utilities:
       title: "🔧 Utilities"
       pages:
         - utilities.my_new_app
   
   roles:
     admin:
       sections:
         - utilities  # Ensure section is in role list
   ```

5. **Update `pyproject.toml` (if creating a package):**
   ```toml
   [tool.hatch.build.targets.wheel]
   packages = [
       "apps/shared",
       "apps/my_new_app"  # Add your app
   ]
   ```

### Dual-Mode Execution Pattern

All sub-apps support two execution modes:

**Standalone Mode:**
```bash
# Run directly for development/testing
python apps/my_new_app/main.py
streamlit run apps/my_new_app/main.py
```

**Integrated Mode:**
```bash
# Run through Toybox navigation
uv run --python 3.12 toybox.py
```

**Implementation Pattern:**
```python
import sys
from pathlib import Path

# Ensure apps directory in sys.path for imports
if __name__ == "__main__":
    apps_dir = str(Path(__file__).parent.parent)
    if apps_dir not in sys.path:
        sys.path.insert(0, apps_dir)

# Now imports work in both modes
from shared.utils import some_utility
from shared.constants import CONSTANTS

def main():
    # Your app logic
    pass

if __name__ == "__main__":
    main()  # Standalone execution
else:
    main()  # Called by Streamlit navigation
```

### Import Patterns

**Recommended Pattern:**
```python
# Use absolute imports from apps directory
from shared.utils import generate_dynamic_navigation
from shared.constants import APP_TITLE
from demo_app.utils import process_data
```

**Avoid:**
```python
# Avoid relative imports - Streamlit navigation doesn't preserve package context
from ..shared.utils import something  # ❌ Will fail in integrated mode
from .utils import local_function      # ❌ May fail depending on execution mode
```

## Dependency Management

### Core Commands

```bash
# Install core dependencies
uv sync

# Install with optional groups
uv sync --extra demo_app
uv sync --extra docs

# Install everything
uv sync --all-extras

# Add new dependencies
uv add pandas
uv add --optional-group demo_app plotly
```

### Dependency Groups

**Core Dependencies (always installed):**
- `streamlit` - Web application framework
- `streamlit-authenticator` - Authentication system
- `pyyaml` - Configuration file parsing
- `pandas` - Data manipulation
- `numpy` - Numerical computing

**Optional Groups:**
- `demo_app` - Demo application dependencies
- `docs` - Documentation generation (MkDocs, mkdocstrings)

## Configuration Management

### Adding New Roles

Edit `config/auth.yaml`:

```yaml
credentials:
  usernames:
    new_user:
      email: user@example.com
      name: New User
      password: $2b$12$...  # Generate with bcrypt
      role: analyst  # admin, developer, analyst, viewer
```

Then ensure role exists in `config/navigation.yaml`:

```yaml
roles:
  analyst:
    sections:
      - welcome
      - demo_apps
```

### Adding New Sections

1. **Define section in `config/navigation.yaml`:**
   ```yaml
   sections:
     analytics:
       title: "📊 Analytics"
       pages:
         - analytics.dashboard
         - analytics.reports
   ```

2. **Add to role permissions:**
   ```yaml
   roles:
     admin:
       sections:
         - analytics
   ```

3. **Define projects in `config/projects.yaml`:**
   ```yaml
   projects:
     analytics:
       name: "Analytics Tools"
       apps:
         dashboard:
           name: "Dashboard"
           path: "apps/analytics/dashboard.py"
           icon: "📊"
         reports:
           name: "Reports"
           path: "apps/analytics/reports.py"
           icon: "📈"
   ```

## Documentation

### Viewing Documentation

```bash
# Install documentation dependencies
uv sync --extra docs

# Start documentation server (localhost only)
uv run mkdocs serve

# Access at http://127.0.0.1:8000
```

### Automatic API Documentation

Toybox 2.0 can automatically generate API documentation from your Python source code.

**Configuration in `project.toml`:**

```toml
[documentation]
auto_generate_api_docs = true

api_source_dirs = [
    "apps/shared",
    "apps/demo_app",
    # Add your apps here
]
```

**Features:**
- Automatic generation from docstrings
- Supports multiple source directories
- Google-style docstring format
- Cross-referenced API pages
- Integrated with main documentation

See the [API Documentation Tutorial](docs/tutorials/api-documentation.md) for complete setup instructions.

### Testing Documentation Locally

To test documentation on your local network or from remote machines:

```bash
# Serve on all network interfaces with custom port
uv run mkdocs serve -a 0.0.0.0:8011

# Access from:
# - Local machine: http://localhost:8011
# - Same network: http://<your-ip>:8011
```

**Find your IP address:**
```bash
# Linux/macOS
ip addr show | grep "inet " | grep -v 127.0.0.1

# Or use hostname
hostname -I
```

### Building Documentation

```bash
# Build static HTML
uv run mkdocs build

# Output in site/ directory
```

### Documentation Structure

```
docs/
├── index.md                          # Documentation homepage
├── getting-started/
│   └── quick-start.md               # Installation guide
├── architecture/
│   ├── overview.md                  # System architecture
│   ├── configuration.md             # Configuration system
│   └── navigation.md                # Navigation system
├── tutorials/
│   ├── adding-sub-app.md            # Sub-app creation
│   ├── role-management.md           # User and role management
│   └── configuration.md             # Configuration patterns
├── SUB_APP_DEVELOPMENT_GUIDE.md     # Comprehensive sub-app guide
└── cmake_installation_guide.md      # CMake setup (for dependencies)
```

### Deployment

**GitHub Pages (configurable):**

```bash
# Enable GitHub Pages deployment
./manage_github_pages.sh enable

# Disable deployment
./manage_github_pages.sh disable

# Check status
./manage_github_pages.sh status
```

## Logging System

Toybox uses a hierarchical logging system following Python best practices.

### Architecture

- **Modules define loggers** but never configure handlers
- **Entry points configure logging** (toybox.py, sub-apps in standalone mode)
- **Hierarchical naming** for granular control

### Module Pattern

```python
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def my_function():
    logger.info("Function executed")
    logger.debug("Debug information")
```

### Configuration

**Main application (`toybox.py`):**
```python
import logging.config

logging.config.fileConfig('logging.ini')
```

**Standalone sub-apps:**
```python
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

**Configuration file (`logging.ini`):**
```ini
[loggers]
keys=root,toybox

[logger_toybox]
level=INFO
handlers=console
qualname=toybox
propagate=0

[handlers]
keys=console

[handler_console]
class=StreamHandler
level=INFO
formatter=detailed
args=(sys.stdout,)
```

## Testing

### Running Sub-Apps in Standalone Mode

```bash
# Test individual apps
python apps/demo_app/main.py
streamlit run apps/demo_app/main.py

# Test with UV
uv run python apps/demo_app/main.py
uv run streamlit run apps/demo_app/main.py
```

### Validation

```bash
# Check configuration validity
python check_config.py

# Verbose mode for detailed checks
python check_config.py --verbose
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'shared'`

**Solution:** Ensure `sys.path` includes apps directory:
```python
import sys
from pathlib import Path

if __name__ == "__main__":
    apps_dir = str(Path(__file__).parent.parent)
    if apps_dir not in sys.path:
        sys.path.insert(0, apps_dir)
```

### Navigation Not Showing Pages

**Problem:** Added page to configuration but it doesn't appear

**Checklist:**
1. Page defined in `config/projects.yaml`?
2. Page listed in `config/navigation.yaml` section?
3. Section included in user's role?
4. File path correct in `projects.yaml`?

### Authentication Issues

**Problem:** Cannot login with credentials

**Solutions:**
1. Verify password hash generated with bcrypt
2. Check role exists in `navigation.yaml`
3. Validate `auth.yaml` YAML syntax
4. Ensure cookie key is set correctly

## Best Practices

### Configuration Management

✅ **DO:**
- Use YAML for all configuration
- Keep credentials in `auth.yaml` (not in code)
- Document role permissions
- Use descriptive app keys and names

❌ **DON'T:**
- Hardcode navigation in Python
- Store passwords in plain text
- Mix configuration with application logic
- Use relative imports in sub-apps

### Sub-App Development

✅ **DO:**
- Implement dual-mode execution pattern
- Use absolute imports from `apps/` directory
- Add comprehensive docstrings
- Test standalone before integration

❌ **DON'T:**
- Rely on package context (use sys.path)
- Use relative imports
- Assume execution directory
- Skip standalone testing

### Code Organization

✅ **DO:**
- Keep shared utilities in `apps/shared/`
- One main.py per sub-app
- Separate business logic from UI
- Use type hints

❌ **DON'T:**
- Duplicate utility functions
- Mix concerns in single file
- Skip error handling
- Ignore logging best practices


## Contributing

See the [Sub-App Development Guide](docs/SUB_APP_DEVELOPMENT_GUIDE.md) for comprehensive development guidelines.

## Resources

- **UV Documentation:** https://github.com/astral-sh/uv
- **Streamlit Documentation:** https://docs.streamlit.io/
- **MkDocs Documentation:** https://www.mkdocs.org/
- **Python Packaging Guide:** https://packaging.python.org/

## License

MIT License - see LICENSE file for details

---

**Built with Streamlit and UV**
