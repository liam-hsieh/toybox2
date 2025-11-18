# GitHub Pages Configuration

Learn how to easily control GitHub Pages deployment for your documentation.

## Overview

This template includes a flexible configuration system that allows you to enable or disable GitHub Pages deployment without modifying workflow files or repository settings.

## Configuration File

The `project.toml` file controls various aspects of your project, including documentation deployment:

```toml title="project.toml"
[documentation]
# Enable/disable automatic GitHub Pages deployment
github_pages_enabled = true  # Set to false to disable deployment

# Documentation build settings
build_on_push = true
build_strict = true  # Fail build on warnings

[project]
# General project settings
auto_generate_api_docs = true
include_demo_apps = true
```

## Management Script

Use the included management script for easy control:

### Enable GitHub Pages

```bash
./manage_github_pages.sh enable
```

**What it does:**
- Sets `github_pages_enabled = true` in `project.toml`
- Creates the config file if it doesn't exist
- Shows next steps for deployment

### Disable GitHub Pages

```bash
./manage_github_pages.sh disable
```

**What it does:**
- Sets `github_pages_enabled = false` in `project.toml`
- Future pushes will skip deployment
- Existing deployed site remains until manually removed

### Check Status

```bash
./manage_github_pages.sh status
```

**Output example:**
```
GitHub Pages Status
=====================

Status: ENABLED
Config file: project.toml
Deployment: Will deploy on next push to main branch

Management commands:
   Enable:  ./manage_github_pages.sh enable
   Disable: ./manage_github_pages.sh disable
```

## How It Works

### GitHub Actions Workflow

The workflow includes a configuration check job:

```yaml title=".github/workflows/docs.yml"
jobs:
  check-config:
    runs-on: ubuntu-latest
    outputs:
      github-pages-enabled: ${{ steps.config-check.outputs.enabled }}
    
    steps:
    - name: Check configuration
      id: config-check
      run: |
        enabled=$(python3 check_config.py github_pages 2>/dev/null || echo "true")
        echo "enabled=$enabled" >> $GITHUB_OUTPUT

  build:
    needs: check-config
    if: needs.check-config.outputs.github-pages-enabled == 'true'
    # ... build steps only run if enabled
```

### Conditional Deployment

- **When enabled** (`github_pages_enabled = true`):
  - Workflow builds and deploys documentation
  - Site updates automatically on push
  - GitHub Pages serves the latest docs

- **When disabled** (`github_pages_enabled = false`):
  - Workflow skips build and deployment
  - Logs show "deployment disabled" message
  - Existing site remains unchanged

## Use Cases

### Temporary Disable

When working on major documentation restructuring:

```bash
# Disable deployment while working
./manage_github_pages.sh disable

# Make your changes
git add docs/
git commit -m "WIP: Restructuring documentation"
git push  # No deployment triggered

# Re-enable when ready
./manage_github_pages.sh enable
git commit -m "Enable docs deployment"
git push  # Deployment resumes
```

### Development Branches

For feature branches that shouldn't deploy:

1. **Create feature branch** with deployment disabled
2. **Work on documentation** without triggering deployments
3. **Enable deployment** before merging to main

### Multiple Environments

Different deployment settings for different branches:

- **Main branch**: `github_pages_enabled = true` (production docs)
- **Dev branch**: `github_pages_enabled = false` (no deployment)
- **Staging branch**: Custom deployment to staging environment

## Manual Configuration

You can also edit `project.toml` directly:

```toml
[documentation]
github_pages_enabled = false  # Disable deployment
build_on_push = true          # Still check builds
build_strict = false          # Allow warnings
```

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `github_pages_enabled` | Enable/disable GitHub Pages deployment | `true` |
| `build_on_push` | Build docs on push (even if not deploying) | `true` |
| `build_strict` | Fail build on warnings | `true` |

## Troubleshooting

### Configuration Not Working?

1. **Check file exists**: Ensure `project.toml` is in repository root
2. **Verify syntax**: TOML syntax must be correct
3. **Check permissions**: Ensure workflow has read access to file
4. **Review logs**: Check Actions tab for configuration check output

### Script Issues?

```bash
# Check if script is executable
ls -la manage_github_pages.sh

# Make executable if needed
chmod +x manage_github_pages.sh

# Run with verbose output
bash -x manage_github_pages.sh status
```

### Python Issues?

The configuration checker requires Python 3.11+ or the `tomli` package:

```bash
# For Python < 3.11, install tomli
pip install tomli

# Check configuration manually
python3 check_config.py show
```

## Best Practices

### Version Control

Always commit configuration changes:

```bash
# After enabling/disabling
git add project.toml
git commit -m "Update GitHub Pages configuration"
git push
```

### Team Workflow

1. **Document decisions**: Comment why deployment is enabled/disabled
2. **Coordinate changes**: Discuss with team before changing deployment settings
3. **Test locally**: Use `mkdocs serve` to test before enabling deployment

### Automation

You can script deployment control:

```bash
#!/bin/bash
# deploy-docs.sh

echo "Building documentation locally..."
mkdocs build

echo "Enabling GitHub Pages deployment..."
./manage_github_pages.sh enable

echo "Committing and pushing..."
git add .
git commit -m "Deploy documentation updates"
git push

echo "Documentation deployment initiated!"
```

## Advanced Usage

### Environment-Based Configuration

Use different settings for different environments:

```bash
# Production
export GITHUB_PAGES_ENABLED=true
./manage_github_pages.sh enable

# Development
export GITHUB_PAGES_ENABLED=false
./manage_github_pages.sh disable
```

### Conditional Deployment

Only deploy when specific conditions are met:

```bash
# Deploy only if tests pass
if ./run_tests.sh; then
    ./manage_github_pages.sh enable
else
    ./manage_github_pages.sh disable
fi
```

This flexible configuration system gives you complete control over when and how your documentation is deployed!