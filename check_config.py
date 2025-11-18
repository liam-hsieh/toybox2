#!/usr/bin/env python3
"""Configuration reader for project settings.

This module provides utilities for reading and validating project
configuration from project.toml files. It implements proper logging
for configuration operations and error handling.

Features:
    - TOML configuration file parsing
    - GitHub Pages configuration validation
    - Verbose logging mode for debugging
    - Cross-platform Python version compatibility

Usage:
    python check_config.py [github_pages|show|--verbose]

Examples:
    python check_config.py github_pages    # Check GitHub Pages status
    python check_config.py show           # Display full configuration
    python check_config.py --verbose      # Show detailed logging
"""

import sys
import logging
from pathlib import Path

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

try:
    import tomllib
except ImportError:
    # Python < 3.11
    try:
        import toml as tomllib
    except ImportError:
        logger.critical("tomllib/tomli not available. Please install tomli for Python < 3.11")
        sys.exit(1)

def read_config():
    """Read project configuration from project.toml."""
    config_path = Path("project.toml")
    
    if not config_path.exists():
        logger.warning("project.toml not found, using defaults")
        return {
            "documentation": {
                "github_pages_enabled": True,
                "build_on_push": True,
                "build_strict": True
            },
            "project": {
                "auto_generate_api_docs": True,
                "include_demo_apps": True
            }
        }
    
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        logger.info(f"Successfully loaded configuration from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error reading project.toml: {e}")
        sys.exit(1)

def check_github_pages_enabled():
    """Check if GitHub Pages deployment is enabled."""
    config = read_config()
    return config.get("documentation", {}).get("github_pages_enabled", True)

if __name__ == "__main__":
    # Configure logging for script execution
    logging.basicConfig(
        level=logging.WARNING,  # Only show warnings and errors for CLI usage
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler()],
        force=True
    )
    
    config = read_config()
    
    # Check what user wants to know
    if len(sys.argv) > 1:
        if sys.argv[1] == "github_pages":
            enabled = check_github_pages_enabled()
            print("true" if enabled else "false")  # Keep print for CLI output
        elif sys.argv[1] == "show":
            import json
            print(json.dumps(config, indent=2))  # Keep print for CLI output
        elif sys.argv[1] == "--verbose":
            # Enable verbose logging for debugging
            logging.getLogger().setLevel(logging.DEBUG)
            logger.info("Verbose mode enabled")
            config = read_config()
            import json
            print(json.dumps(config, indent=2))
    else:
        print("Usage: python check_config.py [github_pages|show|--verbose]")
        print("  github_pages: Check if GitHub Pages is enabled")
        print("  show: Display full configuration")
        print("  --verbose: Show detailed logging and configuration")