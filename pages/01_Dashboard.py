"""
Dashboard Page - Toybox 2.0 Home
Main landing page with overview and quick access
"""

import streamlit as st
import sys
from pathlib import Path

# Add shared components to path
current_dir = Path(__file__).parent
apps_dir = current_dir.parent / "apps"
sys.path.insert(0, str(apps_dir))

from shared.components import (
    create_page_header, create_metric_cards, create_info_card,
    create_action_buttons, display_info_message
)
from shared.utils import get_app_version, load_config

# Page header
create_page_header(
    "Dashboard",
    "Welcome to E2E Solutions Toybox 2.0",
    "🏠"
)

# Load configuration
config = load_config()

# Welcome section
st.markdown("### 👋 Welcome to Toybox 2.0!")

display_info_message(
    "This is the new native Streamlit multipage implementation of the Toybox platform. "
    "Navigate using the sidebar to access different applications and tools."
)

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🧰 Available Apps",
        value="9",
        delta="3 new",
        help="Total number of applications in Toybox"
    )

with col2:
    st.metric(
        "👥 Active Users",
        value="25",
        delta="5 this week",
        help="Users who have accessed Toybox recently"
    )

with col3:
    st.metric(
        "📊 Projects",
        value="3",
        help="Number of project categories"
    )

with col4:
    st.metric(
        "🚀 Version",
        value=get_app_version(),
        help="Current Toybox version"
    )

# Quick access section
st.markdown("### 🚀 Quick Access")

# Create action buttons for popular apps
popular_apps = [
    {
        'key': 'snow_dumper',
        'label': '❄️ Snow Dumper',
        'help': 'Access the main Snow Dumper application',
        'type': 'primary'
    },
    {
        'key': 'data_quality',
        'label': '📝 Excel Macro',
        'help': 'Open Excel Macro data processing tool'
    },
    {
        'key': 'api_explorer',
        'label': '🌐 API Explorer',
        'help': 'Explore and test APIs'
    }
]

button_states = create_action_buttons(popular_apps)

# Handle button clicks (placeholder - would navigate in real implementation)
for button_key, clicked in button_states.items():
    if clicked:
        st.info(f"Redirecting to {button_key}... (Feature coming soon)")

# System overview
st.markdown("### 📋 System Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔧 Available Projects")
    
    projects_config = config.get('projects', {}).get('projects', {})
    
    for project_key, project_info in projects_config.items():
        with st.expander(f"{project_info.get('icon', '📱')} {project_info.get('name', project_key)}"):
            st.markdown(f"**Description:** {project_info.get('description', 'No description')}")
            
            apps = project_info.get('apps', {})
            if apps:
                st.markdown("**Applications:**")
                for app_key, app_info in apps.items():
                    st.markdown(f"- {app_info.get('icon', '📱')} {app_info.get('title', app_key)}")

with col2:
    st.markdown("#### 📊 Recent Activity")
    
    # Placeholder activity log
    activity_data = [
        {"Time": "10:30", "User": "Demo User", "Action": "Accessed Snow Dumper"},
        {"Time": "10:25", "User": "Demo User", "Action": "Viewed Dashboard"},
        {"Time": "10:20", "User": "Demo User", "Action": "Logged in"},
    ]
    
    for activity in activity_data:
        st.markdown(f"**{activity['Time']}** - {activity['User']}: {activity['Action']}")

# Information cards
st.markdown("### ℹ️ Important Information")

col1, col2 = st.columns(2)

with col1:
    create_info_card(
        "🆕 What's New in 2.0",
        """
        • Native Streamlit multipage navigation<br>
        • Improved URL routing and deep linking<br>
        • Role-based access control<br>
        • Better performance and user experience<br>
        • Modern responsive design
        """,
        "info"
    )

with col2:
    create_info_card(
        "🔗 Quick Links",
        """
        • <a href="https://e2esol.intel.com:4002/" target="_blank">Original Toybox</a><br>
        • <a href="mailto:liam.hsieh@intel.com">Support Contact</a><br>
        • <a href="https://liamhsieh.intel.com/" target="_blank">Developer Website</a><br>
        • <a href="#" onclick="window.location.reload()">Refresh Page</a>
        """,
        "success"
    )

# Footer
st.markdown("---")
st.markdown("### 🛠️ System Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("🟢 **Toybox Core:** Online")

with col2:
    st.markdown("🟢 **Database:** Connected")

with col3:
    st.markdown("🟢 **Authentication:** Active")

st.caption("Last updated: November 10, 2025 | Toybox 2.0 Native Multipage Implementation")