"""Generate API reference pages automatically from source code.

This script creates detailed API documentation for each module while preserving
manual overview pages for better organization.

Configuration is read from project.toml:
  [documentation]
  auto_generate_api_docs = true
  api_source_dirs = ["apps/shared", "apps/demo_app"]
"""

from pathlib import Path
import mkdocs_gen_files
import sys

# Try to load configuration
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Warning: tomllib/tomli not available, using default configuration")
        tomllib = None

# Load configuration from project.toml
def load_config():
    """Load API documentation configuration from project.toml."""
    config_path = Path("project.toml")
    
    if not config_path.exists():
        print("Warning: project.toml not found, using default configuration")
        return {
            "auto_generate_api_docs": True,
            "api_source_dirs": ["apps/shared", "apps/demo_app"]
        }
    
    if tomllib is None:
        print("Warning: Cannot read project.toml, using default configuration")
        return {
            "auto_generate_api_docs": True,
            "api_source_dirs": ["apps/shared", "apps/demo_app"]
        }
    
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        
        doc_config = config.get("documentation", {})
        return {
            "auto_generate_api_docs": doc_config.get("auto_generate_api_docs", True),
            "api_source_dirs": doc_config.get("api_source_dirs", ["apps/shared", "apps/demo_app"])
        }
    except Exception as e:
        print(f"Warning: Error loading project.toml: {e}")
        return {
            "auto_generate_api_docs": True,
            "api_source_dirs": ["apps/shared", "apps/demo_app"]
        }

# Load configuration
config = load_config()

# Check if API docs generation is enabled
if not config["auto_generate_api_docs"]:
    print("API documentation generation is disabled in project.toml")
    sys.exit(0)

# Get source directories
source_dirs = config["api_source_dirs"]
print(f"Generating API docs for: {source_dirs}")

api_nav = []

# Generate documentation for each configured source directory
for src_dir_str in source_dirs:
    src_dir = Path(src_dir_str)
    
    if not src_dir.exists():
        print(f"Warning: Source directory '{src_dir}' does not exist, skipping")
        continue
    
    print(f"Processing directory: {src_dir}")
    
    # Generate documentation for each Python package/module
    for path in sorted(src_dir.rglob("*.py")):
        # Skip __pycache__, __init__.py and other non-source files
        if "__pycache__" in str(path) or path.name.startswith("__"):
            continue
        
        # Convert file path to module path relative to project root
        module_path = path.with_suffix("")
        doc_path = path.relative_to(Path(".")).with_suffix(".md")
        full_doc_path = Path("api", "reference") / doc_path
        
        # Convert path separators to dots for Python module names
        module_name = str(module_path).replace("/", ".")
        
        # Create the markdown content with mkdocstrings reference
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            # Get the module/package name for the title
            title = path.stem.replace('_', ' ').title()
            
            print(f"# {title}", file=fd)
            print(f"", file=fd)
            print(f"Auto-generated API documentation for `{module_name}`.", file=fd)
            print(f"", file=fd)
            print(f"::: {module_name}", file=fd)
            print(f"    options:", file=fd)
            print(f"      show_source: true", file=fd)
            print(f"      show_root_heading: false", file=fd)
            print(f"      show_signature_annotations: true", file=fd)
            print(f"      separate_signature: true", file=fd)
        
        # Set up navigation
        mkdocs_gen_files.set_edit_path(full_doc_path, path)
        
        # Build navigation structure
        api_nav.append((str(full_doc_path), str(src_dir), str(path.relative_to(src_dir))))

# Create an index page for auto-generated API docs
with mkdocs_gen_files.open("api/reference/index.md", "w") as fd:
    print("# Auto-Generated API Reference", file=fd)
    print("", file=fd)
    print("This section contains automatically generated documentation for all modules.", file=fd)
    print("", file=fd)
    print("## Configuration", file=fd)
    print("", file=fd)
    print("Documentation is generated from the following source directories:", file=fd)
    print("", file=fd)
    for src_dir in source_dirs:
        print(f"- `{src_dir}`", file=fd)
    print("", file=fd)
    print("Configure in `project.toml` under `[documentation]` section.", file=fd)
    print("", file=fd)
    print("## Available Modules", file=fd)
    print("", file=fd)
    
    # Group modules by source directory
    modules_by_source = {}
    for nav_path, src_dir, rel_path in sorted(api_nav):
        if src_dir not in modules_by_source:
            modules_by_source[src_dir] = []
        modules_by_source[src_dir].append((rel_path, nav_path))
    
    for src_dir, modules in modules_by_source.items():
        print(f"### {src_dir}", file=fd)
        print("", file=fd)
        
        for rel_path, nav_path in modules:
            module_name = Path(rel_path).stem.replace("_", " ").title()
            link_path = nav_path.replace("api/reference/", "")
            print(f"- **[{module_name}]({link_path})** - `{src_dir}/{rel_path}`", file=fd)
        print("", file=fd)