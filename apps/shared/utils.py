"""
Utility functions for Toybox 2.0
Common helper functions and configuration management
"""
import yaml
import os
import streamlit as st
from pathlib import Path
from typing import Dict, Any, Optional
import configparser
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())



def load_config() -> Dict[str, Any]:
    """Load all configuration files"""
    config_dir = Path(__file__).parent.parent.parent / "config"
    
    config = {}
    
    # Load each configuration file
    config_files = {
        'auth': 'auth.yaml',
        'projects': 'projects.yaml', 
        'navigation': 'navigation.yaml'
    }
    
    for key, filename in config_files.items():
        file_path = config_dir / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                config[key] = yaml.safe_load(f)
        else:
            st.warning(f"Configuration file not found: {filename}")
            config[key] = {}
    
    return config


def get_user_role(user_info: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Determine user role based on configuration"""
    # if not user_info or not user_info.get('idsid'):
    #     return 'viewer'
    
    idsid = user_info['idsid']
    
    # Check role assignments in navigation config
    nav_config = config.get('navigation', {})
    user_assignments = nav_config.get('user_assignments', {})

    
    # Try to determine role from database configuration
    # try:
    #     # Use environment variable DB_INI_PATH if set, otherwise fall back to config
    #     db_ini_path = os.getenv('DB_INI_PATH') or config.get('auth', {}).get('database', {}).get('ini_path', '/opt/ssl/db.ini')
    #     role = _get_role_from_database(idsid, db_ini_path)
    #     if role:
    #         return role
    # except Exception as e:
    #     st.warning(f"Could not determine role from database: {e}")
    
    # Default role
    return user_assignments.get(idsid, 'viewer')


def _get_role_from_database(idsid: str, db_ini_path: str) -> Optional[str]:
    """Get user role from database configuration"""
    try:
        config = configparser.ConfigParser()
        config.read(db_ini_path)
        
        # Check different Toybox sections to determine role
        toybox_sections = [section for section in config.sections() if section.startswith('Toybox-')]
        
        for section_name in toybox_sections:
            section = config[section_name]
            users = [user.strip() for user in section.get("user", "").split(',') if user.strip()]
            
            if idsid in users:
                # Determine role based on section name
                if 'admin' in section_name.lower():
                    return 'admin'
                elif 'sme' in section_name.lower():
                    return 'sme'
                elif 'developer' in section_name.lower():
                    return 'developer'
                elif 'analyst' in section_name.lower():
                    return 'analyst'
                else:
                    return 'viewer'
    except:
        pass
    
    return None
def _find_app_in_projects(app_key: str, projects_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find app definition in projects.yaml"""
    return projects_config.get('apps', {}).get(app_key)

def generate_dynamic_navigation(user_role, config):
    """Generate navigation dynamically from configuration files"""
    # 1. Get user's authorized sections from navigation.yaml
    roles_config = config['navigation']['roles']
    authorized_sections = roles_config[user_role]['sections']
    
    # 2. For each authorized section, get page list
    sections_config = config['navigation']['sections']
    navigation_dict = {}

    for project_key in authorized_sections:
        section = sections_config[project_key]
        section_pages = []

        # 3. For each page in section, find app definition in projects.yaml
        for app_key in section['pages']:
            project_config = config['projects']["projects"].get(project_key)
            app_config = _find_app_in_projects(app_key, project_config)
            if app_config:
                # 4. Create st.Page from projects.yaml metadata
                page = st.Page(
                    page=app_config['path'],
                    title=app_config['title'],
                    icon=app_config['icon']
                )
                section_pages.append(page)
        
        if section_pages:
            navigation_dict[section['title']] = section_pages
    
    return navigation_dict

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def get_project_info(project_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Get project information from configuration"""
    projects_config = config.get('projects', {}).get('projects', {})
    return projects_config.get(project_name, {})


def validate_browser_compatibility() -> bool:
    """Check browser compatibility and show warnings if needed"""
    # This would be enhanced with actual browser detection
    # For now, just show a general recommendation
    with st.sidebar:
        st.info("💡 **Browser Tip:** For the best experience, use Google Chrome or Firefox.")
    
    return True


def create_breadcrumb(page_path: str) -> str:
    """Create breadcrumb navigation for current page"""
    parts = page_path.split('/')
    breadcrumbs = []
    
    for i, part in enumerate(parts):
        if part:
            # Format part name
            formatted = part.replace('_', ' ').replace('.py', '').title()
            breadcrumbs.append(formatted)
    
    return ' > '.join(breadcrumbs)


def log_user_action(user_id: str, action: str, details: str = ""):
    """Log user actions for analytics (placeholder)"""
    # In production, this would log to a proper logging system
    if 'user_actions' not in st.session_state:
        st.session_state.user_actions = []
    
    st.session_state.user_actions.append({
        'user_id': user_id,
        'action': action,
        'details': details,
        'timestamp': str(st.runtime.Runtime.instance().timestamp)
    })


def get_app_version() -> str:
    """Get application version"""
    return "0.1.0-beta"

def check_odbc_driver():
    from pyodbc import drivers
    # Get a list of installed ODBC drivers
    odbc_drivers = drivers()
    found_drivers=[]
    # Check for SQL Server drivers and print their names
    sql_server_drivers = [driver for driver in odbc_drivers if 'SQL Server' in driver]
    if sql_server_drivers:
        
        for driver in sql_server_drivers:
            if "ODBC" in driver:
                found_drivers.append(driver)
    else:
        raise Exception("No SQL Server ODBC drivers are found. Please set availavble driver in db.ini file for your SQL Server")

    return found_drivers

def parse_db_access(config_path: str, section_name:str)->Dict:
    """parse the configuration file to acquire required information for connecting supporting DBs

    Args:
        config_path (str): path of configuration file
        section_name (str): section name for db access in config file

    Returns:
        Dict: access information
    """

    try:
        config = configparser.ConfigParser()
        _ = config.read(config_path)

        db_access = config._sections[section_name]
        db_access["ssl"] = config._sections["SSL"]
        # db_access = {}
        # db_access["server_username"] = config.get(section_name, 'username')

        if "db_type" not in db_access.keys(): raise ValueError("db_type is mandatory for setting db.ini")
        if db_access["db_type"]=="mssql" and "driver" not in db_access.keys():
            db_access["driver"] = check_odbc_driver()[0]

        return db_access

    except Exception as e:
        print(f"function parse_db_access got exception message: {e}")
        logger.info(
            "unable to parse from configuration file:/n {config_path} for database access information"
        )

if __name__ == "__main__":
    # For testing purposes
    import pprint
    config = load_config()
    pprint.pprint(config)
    user_info = {'idsid': 'lhsieh'}
    role = get_user_role(user_info, config)
    print(f"User role: {role}")
    navigation = generate_dynamic_navigation(role, config)
    pprint.pprint(f"Navigation: {navigation}")