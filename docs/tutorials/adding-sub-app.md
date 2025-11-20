# Adding a New Sub-Application

This tutorial walks you through creating and integrating a new sub-application into Toybox 2.0.

## Overview

Adding a new sub-app involves:

1. Creating the application directory and files
2. Implementing the dual-mode execution pattern
3. Configuring the app in `projects.yaml`
4. Adding navigation in `navigation.yaml`
5. Assigning role permissions
6. Testing standalone and integrated modes

**Time Required:** 15-30 minutes

## Prerequisites

- Toybox 2.0 installed and running
- Basic Python and Streamlit knowledge
- Understanding of YAML configuration
- Admin access to configuration files

## Step 1: Create Application Directory

```bash
cd /opt/projects/toybox2
mkdir -p apps/data_analyzer
```

Create the following structure:

```
apps/data_analyzer/
├── main.py          # Entry point
├── utils.py         # App-specific utilities (optional)
└── README.md        # App documentation (optional)
```

## Step 2: Implement Main Application

Create `apps/data_analyzer/main.py`:

```python
"""
Data Analyzer - A sub-application for Toybox 2.0

This app demonstrates data analysis capabilities with Pandas and visualization.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# ============================================================================
# Dual-Mode Execution Setup
# ============================================================================
# This pattern enables the app to run standalone OR integrated in Toybox

if __name__ == "__main__":
    # Standalone mode: add apps directory to sys.path for imports
    apps_dir = str(Path(__file__).parent.parent)
    if apps_dir not in sys.path:
        sys.path.insert(0, apps_dir)

# ============================================================================
# Imports
# ============================================================================
# Use absolute imports from apps/ directory - works in both modes

from shared.constants import APP_TITLE
from shared.utils import some_shared_function  # Example

# Optional: Import app-specific utilities
# from data_analyzer.utils import process_data

# ============================================================================
# Configuration
# ============================================================================

APP_NAME = "Data Analyzer"
VERSION = "1.0.0"

# ============================================================================
# Helper Functions
# ============================================================================

def load_sample_data():
    """Load sample dataset for demonstration."""
    return pd.DataFrame({
        'Product': ['A', 'B', 'C', 'D', 'E'],
        'Sales': [100, 150, 200, 175, 225],
        'Profit': [20, 30, 50, 35, 55]
    })

def analyze_data(df: pd.DataFrame) -> dict:
    """Perform basic analysis on dataframe."""
    return {
        'total_sales': df['Sales'].sum(),
        'avg_profit': df['Profit'].mean(),
        'top_product': df.loc[df['Sales'].idxmax(), 'Product']
    }

# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application logic."""
    
    # Page configuration
    st.title(f"📊 {APP_NAME}")
    st.write(f"Version: {VERSION}")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        show_raw_data = st.checkbox("Show Raw Data", value=False)
    
    # Main content
    st.header("Sample Data Analysis")
    
    # Load data
    df = load_sample_data()
    
    # Show raw data if requested
    if show_raw_data:
        st.subheader("Raw Data")
        st.dataframe(df)
    
    # Perform analysis
    results = analyze_data(df)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${results['total_sales']}")
    with col2:
        st.metric("Avg Profit", f"${results['avg_profit']:.2f}")
    with col3:
        st.metric("Top Product", results['top_product'])
    
    # Visualization
    st.subheader("Sales by Product")
    st.bar_chart(df.set_index('Product')['Sales'])
    
    st.subheader("Profit by Product")
    st.bar_chart(df.set_index('Product')['Profit'])

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Standalone mode: run directly
    # Usage: python apps/data_analyzer/main.py
    #        streamlit run apps/data_analyzer/main.py
    main()
else:
    # Integrated mode: called by Streamlit navigation in Toybox
    main()
```

## Step 3: Add Optional Utilities (Optional)

If your app needs utilities, create `apps/data_analyzer/utils.py`:

```python
"""Utility functions for Data Analyzer."""

import pandas as pd

def process_data(df: pd.DataFrame, operation: str) -> pd.DataFrame:
    """Process dataframe based on operation type."""
    if operation == "normalize":
        return (df - df.min()) / (df.max() - df.min())
    elif operation == "standardize":
        return (df - df.mean()) / df.std()
    return df

def validate_data(df: pd.DataFrame) -> dict:
    """Validate dataframe and return issues."""
    issues = {}
    
    if df.isnull().any().any():
        issues['null_values'] = True
    
    if len(df) == 0:
        issues['empty_dataframe'] = True
    
    return issues
```

## Step 4: Test Standalone Execution

Before integrating, test the app standalone:

```bash
# Direct Python execution
python apps/data_analyzer/main.py

# Or with Streamlit
streamlit run apps/data_analyzer/main.py

# Or with UV
uv run streamlit run apps/data_analyzer/main.py
```

**Verify:**
- App loads without errors
- UI renders correctly
- All functionality works
- Imports resolve properly

## Step 5: Configure in projects.yaml

Add your app to `config/projects.yaml`:

```yaml
projects:
  # ... existing projects ...
  
  utilities:  # Group name (or create new group)
    name: "Utility Tools"
    apps:
      data_analyzer:  # App key (must be unique)
        name: "Data Analyzer"  # Display name in navigation
        path: "apps/data_analyzer/main.py"  # Relative path
        icon: "📊"  # Emoji for navigation
        description: "Analyze data with Pandas and visualizations"
```

**Configuration Guidelines:**

- **App Key:** Use lowercase with underscores (`data_analyzer`)
- **Name:** User-friendly display name (`Data Analyzer`)
- **Path:** Relative from project root (`apps/data_analyzer/main.py`)
- **Icon:** Single emoji (`📊`, `🔧`, `📈`, etc.)
- **Description:** Brief explanation for documentation

## Step 6: Add to Navigation

Update `config/navigation.yaml` to include your app:

```yaml
sections:
  # ... existing sections ...
  
  utilities:  # Section key (matches project group)
    title: "🔧 Utilities"  # Section header in sidebar
    pages:
      - utilities.data_analyzer  # Format: project_key.app_key
      # Add more pages as needed

roles:
  admin:
    sections:
      - welcome
      - demo_apps
      - utilities  # Add utilities section to admin role
      - system
  
  developer:
    sections:
      - welcome
      - demo_apps
      - utilities  # Add utilities section to developer role
  
  analyst:
    sections:
      - welcome
      - utilities  # Analysts can access utilities too
```

**Navigation Guidelines:**

- **Section Key:** Must match project key in `projects.yaml`
- **Page References:** Format is always `project_key.app_key`
- **Role Assignment:** Add section to appropriate roles
- **Ordering:** Sections appear in the order listed in role configuration

## Step 7: Test Integrated Mode

Restart Toybox and test the integrated app:

```bash
# Stop current Toybox instance (Ctrl+C)

# Restart Toybox
uv run --python 3.12 toybox.py
```

**Test Checklist:**

- [ ] Login with appropriate role
- [ ] App appears in navigation sidebar
- [ ] App loads when selected
- [ ] All features work as expected
- [ ] No import errors
- [ ] Navigation between pages works
- [ ] Logout functionality works

## Step 8: Update Package Configuration (Optional)

If you want to make your app importable as a package, update `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel]
packages = [
    "apps/shared",
    "apps/demo_app",
    "apps/data_analyzer"  # Add your app
]
```

Then reinstall:

```bash
uv sync
```

This allows other apps to import from your app:

```python
from data_analyzer.utils import process_data
```

## Complete Example Structure

After following all steps, your structure should look like:

```
toybox2/
├── config/
│   ├── projects.yaml     # ✅ Updated with data_analyzer config
│   ├── navigation.yaml   # ✅ Updated with utilities section
│   └── auth.yaml        # No changes needed
├── apps/
│   ├── shared/
│   │   ├── utils.py
│   │   └── constants.py
│   ├── data_analyzer/   # ✅ New app directory
│   │   ├── main.py      # ✅ Application code
│   │   ├── utils.py     # ✅ Optional utilities
│   │   └── README.md    # ✅ Optional documentation
│   └── ...
└── pyproject.toml       # ✅ Optionally updated
```

## Advanced Patterns

### App with Multiple Pages

Create a multi-page structure within your app:

```
apps/data_analyzer/
├── main.py           # Main dashboard
├── upload.py         # Data upload page
├── analysis.py       # Analysis page
├── reports.py        # Reports page
├── utils.py          # Shared utilities
└── components/       # Reusable UI components
    ├── charts.py
    └── tables.py
```

Configure each page separately:

```yaml
projects:
  utilities:
    name: "Utility Tools"
    apps:
      data_analyzer_main:
        name: "Data Analyzer - Dashboard"
        path: "apps/data_analyzer/main.py"
        icon: "📊"
      data_analyzer_upload:
        name: "Data Analyzer - Upload"
        path: "apps/data_analyzer/upload.py"
        icon: "📤"
```

### App with Dependencies

If your app needs special packages:

```bash
# Add dependencies
uv add plotly scikit-learn

# Or create optional group
```

Update `pyproject.toml`:

```toml
[project.optional-dependencies]
data_analyzer = [
    "plotly>=5.0.0",
    "scikit-learn>=1.0.0",
]
```

Install with:

```bash
uv sync --extra data_analyzer
```

### App with State Management

Use Streamlit session state for complex workflows:

```python
def main():
    # Initialize state
    if 'data' not in st.session_state:
        st.session_state.data = None
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Use state throughout app
    if st.button("Load Data"):
        st.session_state.data = load_sample_data()
    
    if st.session_state.data is not None:
        st.dataframe(st.session_state.data)
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'shared'`

**Solution:**
```python
# Ensure this is in your main.py:
if __name__ == "__main__":
    apps_dir = str(Path(__file__).parent.parent)
    if apps_dir not in sys.path:
        sys.path.insert(0, apps_dir)
```

### App Not Appearing in Navigation

**Problem:** App is configured but doesn't show up

**Checklist:**
1. App defined in `projects.yaml`? ✓
2. App listed in `navigation.yaml` section? ✓
3. Section included in user's role? ✓
4. Toybox restarted after configuration changes? ✓

### Page Path Errors

**Problem:** `FileNotFoundError` when navigating to app

**Solution:**
- Verify path in `projects.yaml` is correct
- Path should be relative from project root
- Use forward slashes even on Windows
- File must have `.py` extension

Example:
```yaml
# ❌ Wrong
path: "data_analyzer/main.py"
path: "/apps/data_analyzer/main.py"
path: "apps\\data_analyzer\\main.py"

# ✅ Correct
path: "apps/data_analyzer/main.py"
```

## Best Practices

### Code Organization

✅ **DO:**
- Use dual-mode execution pattern
- Implement clear function separation
- Add docstrings to functions
- Handle errors gracefully
- Use type hints

❌ **DON'T:**
- Use relative imports
- Hardcode configuration values
- Mix UI and business logic
- Forget error handling

### Configuration

✅ **DO:**
- Use descriptive app keys
- Choose appropriate emojis
- Write clear descriptions
- Group related apps together

❌ **DON'T:**
- Use spaces in app keys
- Duplicate app keys
- Use non-standard characters
- Leave descriptions empty

### Testing

✅ **DO:**
- Test standalone before integrating
- Verify all imports work
- Test with different roles
- Check error handling

❌ **DON'T:**
- Skip standalone testing
- Assume imports will work
- Only test with admin role
- Ignore edge cases

## Next Steps

<div class="grid cards" markdown>

-   :material-shield-account:{ .lg .middle } **Configure Roles**

    ---

    Control who can access your new app
    
    [:octicons-arrow-right-24: Role Management](role-management.md)

-   :material-file-cog:{ .lg .middle } **Advanced Configuration**

    ---

    Learn advanced YAML patterns
    
    [:octicons-arrow-right-24: Configuration Guide](../architecture/configuration.md)

-   :material-code-braces:{ .lg .middle } **Sub-App Development Guide**

    ---

    Deep dive into development patterns
    
    [:octicons-arrow-right-24: Development Guide](../SUB_APP_DEVELOPMENT_GUIDE.md)

</div>

## Summary

You've learned to:

- ✅ Create a new sub-application directory
- ✅ Implement dual-mode execution pattern
- ✅ Configure app in `projects.yaml`
- ✅ Add navigation in `navigation.yaml`
- ✅ Assign role permissions
- ✅ Test standalone and integrated modes
- ✅ Handle common issues

Your app is now fully integrated into Toybox 2.0!
