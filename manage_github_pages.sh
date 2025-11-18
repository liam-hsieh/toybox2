#!/usr/bin/env bash

# GitHub Pages Management Script
# Easy way to enable/disable GitHub Pages deployment

set -e

CONFIG_FILE="project.toml"

show_help() {
    echo "GitHub Pages Management"
    echo "======================"
    echo
    echo "Usage:"
    echo "  ./manage_github_pages.sh [enable|disable|status|help]"
    echo
    echo "Commands:"
    echo "  enable   - Enable GitHub Pages deployment"
    echo "  disable  - Disable GitHub Pages deployment"
    echo "  status   - Show current GitHub Pages status"
    echo "  help     - Show this help message"
    echo
    echo "Examples:"
    echo "  ./manage_github_pages.sh enable"
    echo "  ./manage_github_pages.sh status"
}

check_config_file() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Warning: $CONFIG_FILE not found, creating default configuration..."
        cat > "$CONFIG_FILE" << 'EOF'
# Project Configuration
# This file controls various features of your Python project template

[documentation]
# Enable/disable automatic GitHub Pages deployment
github_pages_enabled = true

# Documentation build settings
build_on_push = true
build_strict = true

[project]
# General project settings
auto_generate_api_docs = true
include_demo_apps = true
EOF
        echo "Created default $CONFIG_FILE"
    fi
}

get_status() {
    if [ -f "$CONFIG_FILE" ]; then
        if python3 check_config.py github_pages 2>/dev/null | grep -q "true"; then
            echo "enabled"
        else
            echo "disabled"
        fi
    else
        echo "unknown"
    fi
}

enable_github_pages() {
    check_config_file
    
    # Update the configuration file
    if command -v sed >/dev/null 2>&1; then
        # Use sed to update the configuration
        sed -i 's/github_pages_enabled = false/github_pages_enabled = true/' "$CONFIG_FILE"
        sed -i 's/github_pages_enabled=false/github_pages_enabled = true/' "$CONFIG_FILE"
        
        # If the line doesn't exist, we need to ensure it's set to true
        if ! grep -q "github_pages_enabled" "$CONFIG_FILE"; then
            # Add the setting if it doesn't exist
            sed -i '/\[documentation\]/a github_pages_enabled = true' "$CONFIG_FILE"
        fi
    else
        echo "sed command not found. Please manually edit $CONFIG_FILE"
        echo "   Set: github_pages_enabled = true"
        return 1
    fi
    
    echo "GitHub Pages deployment enabled"
    echo "Next steps:"
    echo "   1. Commit and push changes: git add . && git commit -m 'Enable GitHub Pages' && git push"
    echo "   2. Check Actions tab for deployment status"
}

disable_github_pages() {
    check_config_file
    
    # Update the configuration file
    if command -v sed >/dev/null 2>&1; then
        sed -i 's/github_pages_enabled = true/github_pages_enabled = false/' "$CONFIG_FILE"
        sed -i 's/github_pages_enabled=true/github_pages_enabled = false/' "$CONFIG_FILE"
        
        # If the line doesn't exist, add it as disabled
        if ! grep -q "github_pages_enabled" "$CONFIG_FILE"; then
            sed -i '/\[documentation\]/a github_pages_enabled = false' "$CONFIG_FILE"
        fi
    else
        echo "sed command not found. Please manually edit $CONFIG_FILE"
        echo "   Set: github_pages_enabled = false"
        return 1
    fi
    
    echo "GitHub Pages deployment disabled"
    echo "Note: Existing deployed site will remain until manually removed"
    echo "   To re-enable: ./manage_github_pages.sh enable"
}

show_status() {
    status=$(get_status)
    echo "GitHub Pages Status"
    echo "====================="
    echo
    
    case $status in
        "enabled")
            echo "Status: ENABLED"
            echo "Config file: $CONFIG_FILE"
            echo "Deployment: Will deploy on next push to main branch"
            ;;
        "disabled")
            echo "Status: DISABLED"
            echo "Config file: $CONFIG_FILE"
            echo "Deployment: Will skip deployment on push"
            ;;
        "unknown")
            echo "Status: UNKNOWN"
            echo "Config file: $CONFIG_FILE (not found)"
            echo "Run './manage_github_pages.sh enable' to create configuration"
            ;;
    esac
    
    echo
    echo "Management commands:"
    echo "   Enable:  ./manage_github_pages.sh enable"
    echo "   Disable: ./manage_github_pages.sh disable"
}

# Main command handling
case "${1:-help}" in
    "enable")
        enable_github_pages
        ;;
    "disable")
        disable_github_pages
        ;;
    "status")
        show_status
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac