"""
Administration Panel - Toybox 2.0
System administration and user management
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add shared components to path
current_dir = Path(__file__).parent
apps_dir = current_dir.parent / "apps"
sys.path.insert(0, str(apps_dir))

from shared.components import (
    create_page_header, create_action_buttons, create_data_table,
    display_warning_message, display_success_message
)

# Page header
create_page_header(
    "Administration",
    "System administration and user management",
    "⚙️"
)

# Check admin access
current_user = st.session_state.get('current_user', {})
if not current_user.get('idsid') == 'demo_user_id_12345':  # In production, check proper admin role
    display_warning_message("Administrator access required for this page.")
    st.stop()

# Admin dashboard
st.markdown("### 👥 User Management")

# Sample user data
users_data = pd.DataFrame({
    'User ID': ['user001', 'user002', 'user003', 'user004', 'user005'],
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'Role': ['Admin', 'SME', 'Analyst', 'Developer', 'Viewer'],
    'Last Login': ['2025-11-10 09:30', '2025-11-10 08:45', '2025-11-09 16:20', '2025-11-10 10:15', '2025-11-08 14:30'],
    'Status': ['Active', 'Active', 'Active', 'Active', 'Inactive']
})

# User management actions
user_actions = [
    {
        'key': 'add_user',
        'label': '➕ Add User',
        'help': 'Add a new user to the system',
        'type': 'primary'
    },
    {
        'key': 'export_users',
        'label': '📤 Export Users',
        'help': 'Export user list to CSV'
    },
    {
        'key': 'sync_directory',
        'label': '🔄 Sync Directory',
        'help': 'Synchronize with directory service'
    }
]

button_states = create_action_buttons(user_actions)

if button_states.get('add_user'):
    st.info("Add User dialog would open here")

if button_states.get('export_users'):
    display_success_message("User list exported successfully!")

if button_states.get('sync_directory'):
    display_success_message("Directory synchronization completed!")

# Display users table
create_data_table(users_data, "Current Users", searchable=True)

# System configuration
st.markdown("### ⚙️ System Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔧 Application Settings")
    
    # Configuration options
    auto_logout = st.checkbox("Auto-logout after inactivity", value=True)
    session_timeout = st.slider("Session timeout (minutes)", 60, 480, 480)
    debug_mode = st.checkbox("Enable debug mode", value=False)
    maintenance_mode = st.checkbox("Maintenance mode", value=False)
    
    if st.button("💾 Save Settings"):
        display_success_message("Settings saved successfully!")

with col2:
    st.markdown("#### 📊 System Statistics")
    
    system_stats = {
        "Total Users": 127,
        "Active Sessions": 23,
        "Applications": 9,
        "Storage Used": "1.2 TB",
        "Uptime": "45 days, 12 hours"
    }
    
    for stat, value in system_stats.items():
        st.metric(stat, value)

# Role management
st.markdown("### 🎭 Role Management")

roles_data = pd.DataFrame({
    'Role': ['Admin', 'SME', 'Analyst', 'Developer', 'Viewer'],
    'Users': [3, 15, 28, 12, 69],
    'Permissions': [
        'All access',
        'Project management, Data analysis',
        'Analytics tools, Reporting',
        'Development tools, API access', 
        'Dashboard only'
    ],
    'Created': ['2025-01-15', '2025-01-15', '2025-02-01', '2025-02-15', '2025-01-15']
})

create_data_table(roles_data, "System Roles")

# Add role button
if st.button("➕ Add New Role"):
    st.info("Add Role dialog would open here")

# Application management
st.markdown("### 📱 Application Management")

apps_data = pd.DataFrame({
    'Application': ['Snow Dumper', 'Excel Macro', 'API Explorer', 'MM Maintenance', 'System Config'],
    'Status': ['Running', 'Running', 'Running', 'Running', 'Running'],
    'Version': ['2.1.5', '1.8.2', '3.0.1', '2.0.4', '1.5.0'],
    'Last Updated': ['2025-11-05', '2025-10-28', '2025-11-02', '2025-10-15', '2025-09-20'],
    'Users Today': [45, 32, 28, 15, 8]
})

create_data_table(apps_data, "Application Status")

# Application actions
app_actions = [
    {
        'key': 'restart_apps',
        'label': '🔄 Restart All',
        'help': 'Restart all applications'
    },
    {
        'key': 'update_apps',
        'label': '⬆️ Check Updates',
        'help': 'Check for application updates'
    },
    {
        'key': 'backup_config',
        'label': '💾 Backup Config',
        'help': 'Backup system configuration'
    }
]

app_button_states = create_action_buttons(app_actions)

if app_button_states.get('restart_apps'):
    display_warning_message("Application restart initiated. This may take a few minutes.")

if app_button_states.get('update_apps'):
    display_success_message("All applications are up to date!")

if app_button_states.get('backup_config'):
    display_success_message("Configuration backup completed successfully!")

# System logs
st.markdown("### 📋 System Logs")

with st.expander("📄 View Recent Logs"):
    log_entries = [
        "2025-11-10 10:30:15 [INFO] User user001 logged in",
        "2025-11-10 10:28:42 [INFO] Snow Dumper job completed successfully", 
        "2025-11-10 10:25:33 [WARN] High memory usage detected",
        "2025-11-10 10:22:18 [INFO] Excel Macro processing started",
        "2025-11-10 10:20:05 [INFO] System backup completed",
        "2025-11-10 10:15:22 [ERROR] API rate limit exceeded for user002",
        "2025-11-10 10:12:45 [INFO] Database optimization completed",
        "2025-11-10 10:10:30 [INFO] User user003 accessed MM Maintenance"
    ]
    
    for entry in log_entries:
        st.code(entry)

# Export logs button
if st.button("📤 Export System Logs"):
    display_success_message("System logs exported successfully!")

# Maintenance section
st.markdown("### 🔧 Maintenance")

maintenance_col1, maintenance_col2 = st.columns(2)

with maintenance_col1:
    st.markdown("#### 🗄️ Database Maintenance")
    if st.button("🧹 Clean Cache"):
        display_success_message("Cache cleaned successfully!")
    
    if st.button("📊 Optimize Database"):
        display_success_message("Database optimization completed!")

with maintenance_col2:
    st.markdown("#### 🔒 Security Scan")
    if st.button("🔍 Run Security Scan"):
        display_success_message("Security scan completed - No issues found!")
    
    if st.button("📝 Generate Security Report"):
        display_success_message("Security report generated!")

# Footer
st.markdown("---")
st.caption("⚠️ Administrator Panel - Use with caution. All actions are logged and monitored.")