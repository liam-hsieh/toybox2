# Testing Documentation Locally

This guide shows you how to build, test, and preview Toybox 2.0 documentation on your local machine or network.

## Quick Start

### Basic Local Preview

```bash
# Install documentation dependencies
uv sync --extra docs

# Start documentation server
uv run mkdocs serve

# Access at http://127.0.0.1:8000
```

The documentation server will automatically reload when you make changes to markdown files.

## Network Access

### Serve on All Network Interfaces

To access documentation from other machines on your network:

```bash
# Serve on all interfaces with custom port
uv run mkdocs serve -a 0.0.0.0:8011
```

**Access from:**
- Local machine: `http://localhost:8011`
- Same network: `http://<your-ip>:8011`
- Container/VM: `http://<container-ip>:8011`

### Find Your IP Address

=== "Linux"
    ```bash
    # Show all IP addresses
    ip addr show | grep "inet " | grep -v 127.0.0.1
    
    # Or use hostname command
    hostname -I
    
    # Or specific interface
    ip addr show eth0
    ```

=== "macOS"
    ```bash
    # Show all network interfaces
    ifconfig | grep "inet " | grep -v 127.0.0.1
    
    # Or use hostname
    hostname -I
    
    # Or check Network preferences
    ipconfig getifaddr en0
    ```

=== "Windows"
    ```powershell
    # Show IP configuration
    ipconfig
    
    # Or use hostname
    hostname -I
    ```

## Build Options

### Development Server

**Default (localhost only):**
```bash
uv run mkdocs serve
# → http://127.0.0.1:8000
```

**Custom host and port:**
```bash
uv run mkdocs serve -a 0.0.0.0:8011
# → http://0.0.0.0:8011
```

**Specific interface:**
```bash
uv run mkdocs serve -a 192.168.1.100:8000
# → http://192.168.1.100:8000
```

### Static Build

Generate static HTML files for deployment:

```bash
# Build documentation
uv run mkdocs build

# Output directory: site/
ls -la site/
```

**Preview static build:**
```bash
# Build first
uv run mkdocs build

# Serve with Python HTTP server
cd site
python -m http.server 8000

# Access at http://localhost:8000
```

## Testing Workflow

### 1. Edit Documentation

Make changes to markdown files in `docs/` directory:

```bash
# Edit a file
nano docs/getting-started/quick-start.md

# Or use your preferred editor
code docs/architecture/overview.md
```

### 2. Preview Changes

Start the development server if not already running:

```bash
uv run mkdocs serve -a 0.0.0.0:8011
```

**Live reload features:**
- Automatic page refresh on file changes
- Instant updates (no rebuild needed)
- Preserves scroll position
- Works with all markdown files

### 3. Verify Changes

Open your browser and check:

- [ ] Content displays correctly
- [ ] Links work properly
- [ ] Code blocks render with syntax highlighting
- [ ] Images and diagrams appear
- [ ] Navigation structure is correct
- [ ] Search functionality works

### 4. Check for Errors

Monitor the terminal for build errors:

```bash
INFO     -  Building documentation...
INFO     -  Cleaning site directory
INFO     -  Documentation built in 0.52 seconds
INFO     -  [12:34:56] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO     -  [12:34:56] Serving on http://0.0.0.0:8011/
```

**Common errors:**
- Missing files referenced in `mkdocs.yml`
- Broken internal links
- Invalid markdown syntax
- Missing dependencies

## Advanced Testing

### Test with Docker

Create a container for isolated testing:

```dockerfile
# Dockerfile.docs
FROM python:3.12-slim

WORKDIR /docs

# Install UV
RUN pip install uv

# Copy documentation
COPY . .

# Install dependencies
RUN uv sync --extra docs

# Expose port
EXPOSE 8011

# Serve documentation
CMD ["uv", "run", "mkdocs", "serve", "-a", "0.0.0.0:8011"]
```

**Build and run:**
```bash
# Build container
docker build -f Dockerfile.docs -t toybox-docs .

# Run container
docker run -p 8011:8011 toybox-docs

# Access at http://localhost:8011
```

### Test Navigation

Verify navigation structure:

```bash
# Check mkdocs.yml navigation section
cat mkdocs.yml | grep -A 20 "^nav:"

# List all documentation files
find docs -name "*.md" | sort

# Check for broken links (requires linkchecker)
uv run mkdocs build
linkchecker site/
```

### Test Search

1. Start documentation server
2. Open browser to documentation
3. Use search box (top right)
4. Verify search results are relevant
5. Check search suggestions

### Test Different Browsers

Test documentation in multiple browsers:

- Chrome/Chromium
- Firefox
- Safari (macOS)
- Edge (Windows)
- Mobile browsers

**Check for:**
- Responsive design
- Navigation menu on mobile
- Code block scrolling
- Dark/light theme switching

## Performance Testing

### Build Time

Check documentation build performance:

```bash
# Time the build
time uv run mkdocs build

# Typical output:
# real    0m1.234s
# user    0m2.345s
# sys     0m0.456s
```

### Page Load Time

Monitor page load performance:

1. Open browser developer tools (F12)
2. Go to Network tab
3. Navigate to documentation page
4. Check load time and resource sizes

**Optimization tips:**
- Compress images
- Minimize external dependencies
- Use lazy loading for images
- Optimize code examples

## Continuous Testing

### Watch Mode

MkDocs serve runs in watch mode by default:

```bash
uv run mkdocs serve -a 0.0.0.0:8011

# Watches these paths:
# - docs/
# - mkdocs.yml
```

**What triggers rebuild:**
- Creating/modifying markdown files
- Changing `mkdocs.yml`
- Adding/removing files in `docs/`

**What doesn't trigger rebuild:**
- Changes to Python plugins
- Updates to dependencies
- Modifications to theme files

### Pre-commit Testing

Add documentation testing to pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: mkdocs-build
        name: MkDocs Build Test
        entry: uv run mkdocs build --strict
        language: system
        pass_filenames: false
```

Install and use:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Troubleshooting

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill process
kill <PID>

# Or use different port
uv run mkdocs serve -a 0.0.0.0:8001
```

### Build Errors

**Problem:** Build fails with errors

**Solutions:**

1. **Check file references:**
   ```bash
   # Verify all files in nav exist
   grep -E "\.md$" mkdocs.yml | while read line; do
       file=$(echo $line | sed 's/.*: //' | tr -d ' ')
       if [ ! -f "docs/$file" ]; then
           echo "Missing: docs/$file"
       fi
   done
   ```

2. **Validate markdown:**
   ```bash
   # Install markdownlint
   npm install -g markdownlint-cli
   
   # Check all markdown files
   markdownlint docs/**/*.md
   ```

3. **Check dependencies:**
   ```bash
   # Reinstall docs dependencies
   uv sync --extra docs --upgrade
   ```

### Slow Build

**Problem:** Documentation builds slowly

**Solutions:**

1. **Disable plugins temporarily:**
   ```yaml
   # mkdocs.yml
   plugins:
     - search
     # - mkdocstrings  # Disable for testing
     # - gen-files
   ```

2. **Reduce content:**
   - Comment out large sections in `nav`
   - Test individual pages

3. **Clear cache:**
   ```bash
   rm -rf site/
   uv run mkdocs build
   ```

### Cannot Access from Network

**Problem:** Documentation not accessible from other machines

**Checklist:**

1. Server bound to 0.0.0.0? ✓
   ```bash
   uv run mkdocs serve -a 0.0.0.0:8011
   ```

2. Firewall allows port? ✓
   ```bash
   # Linux - allow port
   sudo ufw allow 8011
   
   # macOS - check firewall
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
   ```

3. Correct IP address? ✓
   ```bash
   ip addr show | grep "inet "
   ```

4. Same network/VLAN? ✓

## Best Practices

### Before Committing

1. **Build without errors:**
   ```bash
   uv run mkdocs build --strict
   ```

2. **Check all links:**
   ```bash
   # Internal links
   grep -r "\[.*\](.*\.md)" docs/
   
   # Verify they exist
   ```

3. **Test navigation:**
   - Click through all sections
   - Verify breadcrumbs
   - Check cross-references

4. **Review changes:**
   ```bash
   git diff docs/
   ```

### During Development

1. **Keep server running** - instant feedback
2. **Test on target browsers** - avoid surprises
3. **Check mobile view** - responsive design
4. **Verify search** - proper indexing
5. **Review generated HTML** - inspect `site/` directory

### For Deployment

1. **Clean build:**
   ```bash
   rm -rf site/
   uv run mkdocs build --strict
   ```

2. **Test static build locally:**
   ```bash
   cd site
   python -m http.server 8000
   ```

3. **Verify GitHub Pages config:**
   ```bash
   ./manage_github_pages.sh status
   ```

4. **Check deployment workflow:**
   ```bash
   cat .github/workflows/docs.yml
   ```

## Quick Reference

| Command | Purpose | Access URL |
|---------|---------|------------|
| `uv run mkdocs serve` | Local only | http://127.0.0.1:8000 |
| `uv run mkdocs serve -a 0.0.0.0:8011` | Network access | http://\<your-ip\>:8011 |
| `uv run mkdocs build` | Static build | N/A (creates `site/`) |
| `uv run mkdocs build --strict` | Strict build (fails on warnings) | N/A |
| `uv run mkdocs gh-deploy` | Deploy to GitHub Pages | N/A (deploys) |

## Related Documentation

- **[Production Documentation Server](documentation-production-server.md)** - Serve documentation in production with auto-updates
- **[GitHub Pages Setup](../github-pages-setup.md)** - Deploy documentation online
- **[MkDocs Documentation](https://www.mkdocs.org/)** - Official MkDocs guide
- **[Material Theme](https://squidfunk.github.io/mkdocs-material/)** - Theme documentation

---

!!! tip "Development Tip"
    Keep the documentation server running in a separate terminal while editing. Changes appear instantly, making documentation development much faster!

!!! info "Network Testing"
    Use `uv run mkdocs serve -a 0.0.0.0:8011` to test documentation from mobile devices or other computers on your network.
