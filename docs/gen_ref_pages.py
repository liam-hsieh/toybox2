"""Generate API reference pages automatically from source code.

This script creates detailed API documentation for each module while preserving
manual overview pages for better organization.
"""

from pathlib import Path
import mkdocs_gen_files

# Define the source directory
src_dir = Path("src")
api_nav = []

# Generate documentation for each Python package/module
for path in sorted(src_dir.rglob("*.py")):
    # Skip __pycache__, __init__.py and other non-source files
    if "__pycache__" in str(path) or path.name.startswith("__"):
        continue
    
    # Convert file path to module path
    module_path = path.relative_to(src_dir).with_suffix("")
    doc_path = path.relative_to(src_dir).with_suffix(".md")
    full_doc_path = Path("api", "reference") / doc_path
    
    # Convert path separators to dots for Python module names
    module_name = str(module_path).replace("/", ".")
    
    # Create the markdown content with mkdocstrings reference
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        # Get the module/package name for the title
        title = module_path.name or str(module_path)
        
        print(f"# {title.replace('_', ' ').title()}", file=fd)
        print(f"", file=fd)
        print(f"Auto-generated API documentation for `{module_name}`.", file=fd)
        print(f"", file=fd)
        print(f"::: src.{module_name}", file=fd)
        print(f"    options:", file=fd)
        print(f"      show_source: true", file=fd)
        print(f"      show_root_heading: false", file=fd)
        print(f"      show_signature_annotations: true", file=fd)
        print(f"      separate_signature: true", file=fd)
    
    # Set up navigation
    mkdocs_gen_files.set_edit_path(full_doc_path, path)
    
    # Build navigation structure
    api_nav.append(str(full_doc_path))

# Create an index page for auto-generated API docs
with mkdocs_gen_files.open("api/reference/index.md", "w") as fd:
    print("# Auto-Generated API Reference", file=fd)
    print("", file=fd)
    print("This section contains automatically generated documentation for all modules.", file=fd)
    print("For curated overviews and examples, see the main API Reference section.", file=fd)
    print("", file=fd)
    print("## Available Modules", file=fd)
    print("", file=fd)
    
    # Group modules by package
    modules_by_package = {}
    for nav_path in sorted(api_nav):
        parts = Path(nav_path).parts[2:]  # Remove 'api/reference'
        if len(parts) > 1:
            package = parts[0]
            module = parts[1]
            if package not in modules_by_package:
                modules_by_package[package] = []
            modules_by_package[package].append((module, nav_path))
        else:
            # Root level modules
            module = parts[0]
            if "root" not in modules_by_package:
                modules_by_package["root"] = []
            modules_by_package["root"].append((module, nav_path))
    
    for package, modules in modules_by_package.items():
        if package == "root":
            print("### Root Modules", file=fd)
        else:
            print(f"### {package.title()} Package", file=fd)
        print("", file=fd)
        
        for module_file, nav_path in modules:
            module_name = module_file.replace(".md", "").replace("_", " ").title()
            link_path = nav_path.replace("api/reference/", "")
            print(f"- **[{module_name}]({link_path})** - Detailed API documentation", file=fd)
        print("", file=fd)