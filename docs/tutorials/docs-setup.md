# Documentation Setup Tutorial

Learn how to set up and customize MkDocs documentation with hybrid API documentation.

## Overview

This template uses **MkDocs** with **Material theme** and **mkdocstrings** for automatic API documentation generation from Python docstrings. It implements a **hybrid documentation approach** combining manual curation with automatic generation.

## Documentation Architecture

### Hybrid Approach
- **Manual Overview Pages**: Curated introductions with examples (`docs/api/*.md`)
- **Auto-Generated Reference**: Detailed API docs from source code (`docs/api/reference/*`)
- **Best of Both Worlds**: Context + completeness

### Generated Structure
```
docs/
├── api/
│   ├── index.md              # Manual API overview
│   ├── libs.md               # Manual package overview  
│   ├── demo-sub-app.md       # Manual module overview
│   └── reference/            # Auto-generated detailed docs
│       ├── index.md          # Auto-generated index
│       ├── libs/
│       │   ├── example_module1.md
│       │   └── logging_utils.md
│       └── demo_sub_app/
│           ├── sub_demo_app.md
│           └── example_module2.md
└── gen_ref_pages.py          # Auto-generation script
```

## Installation

Documentation dependencies are included in the optional `docs` group:

```bash
# Install documentation dependencies
uv sync --extra docs
```

## Configuration Files

### mkdocs.yml

The main configuration file controls:

- Site metadata (name, description, URL)
- Theme and styling
- Navigation structure
- Plugins and extensions
- Markdown processing

Key sections:

```yaml title="mkdocs.yml"
# Site information
site_name: Your Project Name
site_description: Project description
theme:
  name: material
  palette:
    - scheme: default      # Light mode
    - scheme: slate        # Dark mode

# Navigation structure
nav:
  - Home: index.md
  - Getting Started:
    - Quick Start: getting-started/quick-start.md
  - API Reference:
    - Your Module: api/your-module.md

# Plugins for automatic documentation
plugins:
  - search
  - mkdocstrings:         # Auto-generates API docs
      handlers:
        python:
          options:
            docstring_style: google
```

## Writing Documentation

### Markdown Files

Create `.md` files in the `docs/` directory:

```bash
docs/
├── index.md              # Homepage
├── getting-started/
│   └── quick-start.md    # Tutorial pages
├── api/                  # API documentation
└── tutorials/            # Step-by-step guides
```

### Docstrings in Code

mkdocstrings automatically generates API docs from your Python docstrings:

```python title="Example with Google-style docstrings"
def calculate_total(items: list[float], tax_rate: float = 0.1) -> float:
    """Calculate the total cost including tax.
    
    This function takes a list of item costs and applies a tax rate
    to calculate the final total.
    
    Args:
        items: List of individual item costs
        tax_rate: Tax rate as a decimal (default: 0.1 for 10%)
        
    Returns:
        Total cost including tax
        
    Raises:
        ValueError: If tax_rate is negative
        
    Example:
        >>> calculate_total([10.0, 20.0], 0.05)
        31.5
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

## Building Documentation

### Local Development

```bash
# Start development server with auto-reload
uv run mkdocs serve

# Custom host and port
uv run mkdocs serve --dev-addr=127.0.0.1:8001
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to preview your docs.

### Building for Production

```bash
# Build static site
uv run mkdocs build

# Output goes to site/ directory
ls site/
```

## Customization

### Themes and Colors

Material theme offers many customization options:

```yaml title="mkdocs.yml - Theme customization"
theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: indigo        # Header color
      accent: indigo         # Link color
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode  
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs        # Top-level tabs
    - navigation.sections    # Expandable sections
    - navigation.top         # Back-to-top button
    - search.highlight       # Highlight search terms
    - content.code.copy      # Copy code button
```

### Adding Custom CSS

1. Create a custom CSS file:
   ```css title="docs/stylesheets/extra.css"
   .md-header {
     background-color: #2c5282 !important;
   }
   
   .md-tabs {
     background-color: #3182ce !important;
   }
   ```

2. Reference it in `mkdocs.yml`:
   ```yaml
   extra_css:
     - stylesheets/extra.css
   ```

### Navigation Structure

Organize your navigation in `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
    - Configuration: getting-started/configuration.md
  - User Guide:
    - Basic Usage: guide/basic-usage.md
    - Advanced Features: guide/advanced.md
  - API Reference:
    - Core Module: api/core.md
    - Utilities: api/utils.md
  - Development:
    - Contributing: development/contributing.md
    - Changelog: development/changelog.md
```

## Auto-generating API Docs

The `gen_ref_pages.py` script automatically creates API documentation:

```python title="docs/gen_ref_pages.py"
"""Generate API reference pages from source code."""

from pathlib import Path
import mkdocs_gen_files

src_dir = Path("src")

for path in sorted(src_dir.rglob("*.py")):
    if "__pycache__" in str(path):
        continue
    
    module_path = path.relative_to(src_dir).with_suffix("")
    doc_path = Path("api") / module_path.with_suffix(".md")
    module_name = str(module_path).replace("/", ".")
    
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        print(f"# {module_path.name}", file=fd)
        print(f"::: src.{module_name}", file=fd)
```

## Deployment

### GitHub Pages

**Automated deployment is already configured!** The template includes a GitHub Actions workflow that automatically builds and deploys your documentation.

#### Quick Setup

1. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select "**GitHub Actions**"
   - Click **Save**

2. **Push your documentation:**
   ```bash
   git add .
   git commit -m "Add documentation setup"
   git push origin main
   ```

3. **Access your live docs:**
   - URL: `https://your-username.github.io/your-repo-name`
   - Usually available within 2-3 minutes after push

#### How It Works

The included `.github/workflows/docs.yml` workflow:

- **Triggers on:** pushes to main branch affecting docs, source code, or config
- **Installs:** Python 3.12 and uv package manager
- **Builds:** documentation with `mkdocs build`
- **Deploys:** to GitHub Pages automatically

#### Workflow Features

```yaml title=".github/workflows/docs.yml"
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'           # Documentation files
      - 'src/**'            # Source code (for API docs)
      - 'mkdocs.yml'        # Configuration
      - 'pyproject.toml'    # Dependencies

permissions:
  contents: read
  pages: write              # Required for Pages deployment
  id-token: write
```

#### Customizing the Workflow

To modify deployment behavior, edit `.github/workflows/docs.yml`:

**Change trigger branches:**
```yaml
on:
  push:
    branches: [ main, develop ]  # Add more branches
```

**Add manual trigger:**
```yaml
on:
  push:
    branches: [ main ]
  workflow_dispatch:             # Enables manual run
```

**Different Python version:**
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'      # Change version
```

#### Troubleshooting

**Build fails?**
- Check the Actions tab in your GitHub repository
- Common issues: missing dependencies, broken links, invalid markdown

**Pages not updating?**
- Ensure GitHub Pages source is set to "GitHub Actions"
- Check if the workflow is enabled in Actions tab
- Verify the workflow file is in `.github/workflows/`

**Custom domain?**
- Add a `CNAME` file to your `docs/` directory with your domain
- Configure DNS to point to GitHub Pages

#### Monitoring Deployments

- **Actions tab**: See build logs and status
- **Environments**: View deployment history under repository settings
- **Commit status**: Green checkmark indicates successful deployment

### Other Platforms

MkDocs generates static HTML that can be deployed anywhere:

- **Netlify**: Connect repository and set build command to `uv run mkdocs build`
- **Vercel**: Similar setup with build command
- **Custom server**: Upload `site/` directory contents

## Tips and Best Practices

!!! tip "Documentation Structure"
    - Keep documentation close to code when possible
    - Use clear, descriptive filenames
    - Organize content logically in navigation
    - Include examples in docstrings

!!! warning "Common Issues"
    - Missing `__init__.py` files prevent mkdocstrings from finding modules
    - Incorrect module paths in `::: src.module.name` references
    - Forgetting to install docs dependencies

!!! info "Advanced Features"
    - Use admonitions for callouts (like these boxes)
    - Include diagrams with Mermaid syntax
    - Add code syntax highlighting
    - Create tabbed content for different platforms

## Example Workflow

1. **Write code with good docstrings**
2. **Create or update markdown files** for tutorials/guides
3. **Run `mkdocs serve`** to preview changes
4. **Update navigation** in `mkdocs.yml` if needed
5. **Push to repository** to trigger automatic deployment

Your documentation will be automatically updated whenever you change your code or markdown files!