"""
UI Components for Toybox 2.0
Reusable Streamlit components and styling
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def apply_custom_css():
    """Apply custom CSS styling to the application"""
    
    css = """
    <style>
    /* Custom Toybox 2.0 Styling */
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Navigation styling */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom info boxes */
    .toybox-info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    
    .toybox-warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    
    .toybox-success-box {
        background-color: #d1f2eb;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    
    /* Header styling */
    h1 {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: #34495e;
    }
    
    h3 {
        color: #7f8c8d;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 0.375rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
    }
    
    /* Metric styling */
    .metric-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    /* Navigation active state */
    .nav-link-active {
        background-color: #3498db !important;
        color: white !important;
    }
    
    /* Footer styling */
    .toybox-footer {
        margin-top: 2rem;
        padding: 1rem;
        text-align: center;
        color: #6c757d;
        font-size: 0.875rem;
        border-top: 1px solid #dee2e6;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def create_sidebar_footer():
    """Create sidebar footer with app information"""
    
    with st.sidebar:
        st.markdown("---")
        
        # App version and info
        st.markdown("**Ver:** 0.1.0")
        st.markdown("**Updated:** Nov 2025")
        
        # Quick help
        with st.expander("🆘 Quick Help"):
            st.markdown("""
            **Navigation:** Use the menu above to switch between applications.
            
            **Shortcuts:**
            - `Ctrl + R` - Refresh current page
            - `Ctrl + Shift + R` - Force reload
            
            **Support:** [liam.hsieh@intel.com](mailto:liam.hsieh@intel.com)
            """)
        
        # System status
        #st.caption(f"🟢 System Online | {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("---")


def create_page_header(title: str, subtitle: str = "", icon: str = ""):
    """Create a consistent page header"""
    
    if icon:
        title = f"{icon} {title}"
    
    st.markdown(f"# {title}")
    
    if subtitle:
        st.markdown(f"*{subtitle}*")
    
    st.markdown("---")


def create_info_card(title: str, content: str, card_type: str = "info"):
    """Create an information card"""
    
    card_classes = {
        "info": "toybox-info-box",
        "warning": "toybox-warning-box", 
        "success": "toybox-success-box"
    }
    
    card_class = card_classes.get(card_type, "toybox-info-box")
    
    st.markdown(f"""
    <div class="{card_class}">
        <strong>{title}</strong><br>
        {content}
    </div>
    """, unsafe_allow_html=True)


def create_metric_cards(metrics: List[Dict[str, Any]]):
    """Create a row of metric cards"""
    
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{metric.get('title', 'Metric')}</h3>
                <h1>{metric.get('value', '0')}</h1>
                <p style="color: #6c757d; margin: 0;">{metric.get('description', '')}</p>
            </div>
            """, unsafe_allow_html=True)


def create_status_indicator(status: str, label: str = ""):
    """Create a status indicator"""
    
    status_colors = {
        "online": "🟢",
        "offline": "🔴", 
        "warning": "🟡",
        "unknown": "⚪"
    }
    
    indicator = status_colors.get(status.lower(), "⚪")
    display_text = f"{indicator} {label}" if label else indicator
    
    st.markdown(f"**Status:** {display_text}")


def create_breadcrumb_navigation(pages: List[str]):
    """Create breadcrumb navigation"""
    
    breadcrumb = " → ".join(pages)
    st.caption(f"📍 {breadcrumb}")


def create_action_buttons(buttons: List[Dict[str, Any]]) -> Dict[str, bool]:
    """Create a row of action buttons and return their states"""
    
    button_states = {}
    
    if len(buttons) == 1:
        button = buttons[0]
        button_states[button['key']] = st.button(
            button['label'],
            key=button['key'],
            help=button.get('help', ''),
            type=button.get('type', 'secondary')
        )
    else:
        cols = st.columns(len(buttons))
        for i, button in enumerate(buttons):
            with cols[i]:
                button_states[button['key']] = st.button(
                    button['label'],
                    key=button['key'],
                    help=button.get('help', ''),
                    type=button.get('type', 'secondary')
                )
    
    return button_states


def create_data_table(data, title: str = "", searchable: bool = False):
    """Create a formatted data table"""
    
    if title:
        st.subheader(title)
    
    if searchable and len(data) > 10:
        search_term = st.text_input("🔍 Search table:", key=f"search_{title}")
        if search_term:
            # Simple search implementation
            mask = data.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            data = data[mask]
    
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


def create_file_uploader(label: str, accepted_types: List[str], help_text: str = ""):
    """Create a styled file uploader"""
    
    return st.file_uploader(
        label,
        type=accepted_types,
        help=help_text,
        accept_multiple_files=False
    )


def show_loading_spinner(message: str = "Loading..."):
    """Show a loading spinner with message"""
    
    with st.spinner(message):
        pass


def create_progress_bar(progress: float, label: str = ""):
    """Create a progress bar"""
    
    if label:
        st.markdown(f"**{label}**")
    
    st.progress(progress)


def create_expandable_section(title: str, content_func, expanded: bool = False):
    """Create an expandable section"""
    
    with st.expander(title, expanded=expanded):
        content_func()


def display_error_message(error: str, details: str = ""):
    """Display formatted error message"""
    
    st.error(f"❌ **Error:** {error}")
    
    if details:
        with st.expander("Error Details"):
            st.code(details)


def display_success_message(message: str):
    """Display formatted success message"""
    
    st.success(f"✅ {message}")


def display_warning_message(message: str):
    """Display formatted warning message"""
    
    st.warning(f"⚠️ {message}")


def display_info_message(message: str):
    """Display formatted info message"""
    
    st.info(f"ℹ️ {message}")