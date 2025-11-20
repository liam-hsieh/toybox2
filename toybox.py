"""
Toybox 2.0 - Native Streamlit Multipage Application
Modern implementation of the project portal using st.Page and st.navigation
"""
# For st.dataframe, Please replace `use_container_width` with `width`.
# `use_container_width` will be removed after 2025-12-31.
# For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.

from altair import Dict
import streamlit as st
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
from typing import Dict, Any, Optional
# Load environment variables from .env file
load_dotenv()

# Add the apps directory to Python path for imports
current_dir = Path(__file__).parent
apps_dir = current_dir / "apps"
sys.path.insert(0, str(apps_dir))

# Import shared components
from shared.auth import ToyboxAuth
from shared.utils import load_config, get_user_role, generate_dynamic_navigation
from shared.components import create_sidebar_footer, apply_custom_css

# Page configuration
st.set_page_config(
    page_title="Toybox 2.0",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "mailto:liamhsieh@ieee.org",
        "Get help": "https://toybox.xxx.com",
        'About': "Developed and maintained by [Liam Hsieh, PhD](https://liamhsieh.info/)."
    }
)

# Apply custom CSS styling
apply_custom_css()

# Load configuration (cached)
#@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_config():
    return load_config()

config = get_cached_config()

# Authentication
auth = ToyboxAuth(config)
if not auth.verify_user():
    st.error("🔐 Authentication required. Please ensure you're logged in properly.")
    st.info("💡 Tip: Use Google Chrome for the best authentication experience.")
    st.stop()
else:
    # Welcome message
    # # # Get current user details
    current_user = auth.get_current_user()
    with st.sidebar:
        st.markdown(f"Welcome, {current_user.get('name')} ({current_user.get('role')})!")


#pages = get_authorized_pages(current_user.get('role'), config)
pages = generate_dynamic_navigation(current_user.get('role'), config)


# Create navigation
if pages:
    pg = st.navigation(pages,position="top")
    
    
    # Run the selected page
    pg.run()
else:
    st.error("❌ No authorized applications available for your role.")
    st.info("📞 Contact your administrator if you believe this is an error.")
