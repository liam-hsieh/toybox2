"""
Authentication module for Toybox 2.0
Handles user authentication and authorization
"""

import streamlit as st
import configparser
import os
from pathlib import Path
from typing import Dict, Optional, Any
from streamlit.components.v1 import html


class ToyboxAuth:
    """Handle authentication and user management for Toybox 2.0"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth_by_cookie = self.config.get('auth',{}).get('auth_methods', {}).get('cookie_based', True)

    def _verify_user_by_SSO(self) -> bool:
        # Placeholder for SSO verification logic
        return False

    @staticmethod
    def get_idsid():
        cookies = st.context.cookies.to_dict()
        return cookies.get("IDSID")

    def verify_user(self) -> bool:
        """Verify if the current user is authenticated"""
        if self.auth_by_cookie is False:
            idsid = self._verify_user_by_SSO()
        else:
            idsid = self.get_idsid()

        if idsid:
            role = self._get_user_role(idsid)
            st.session_state.current_user = {
                'idsid': idsid,
                'name': idsid,
                'authenticated': True,
                'role': role
            }
            return True
            
        return False
    
    def _get_user_name(self, idsid: str) -> str:
        """Get user display name from IDSID"""
        # In production, this would query user database
        # For now, return a formatted version of IDSID

        return idsid.title()
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        return st.session_state.get('current_user', {})

    def _get_user_role(self, idsid=None) -> str:
        """Determine user role based on configuration"""
        if not self.auth_by_cookie:
            return self._get_role_from_database(idsid)
        
        # Check role assignments in navigation config
        nav_config = self.config.get('navigation', {})
        user_assignments = nav_config.get('user_assignments', {})
        
        # Try to determine role from database configuration
        try:
            role = user_assignments.get(idsid, None)
            if role is not None:
                return role
            
        except Exception as e:
            st.warning(f"Could not determine role from configuration: {e}")
            return 'Visitor'
        
        # Default role
        return 'Visitor'

    def _get_role_from_database(self, idsid, db_ini_path=None):
        pass
        return None
    
    def check_project_authorization(self, user_idsid: str, project_name: str) -> bool:
        """Check if user is authorized for specific project"""
        try:
            # Load authorization from database configuration
            config = configparser.ConfigParser()
            config.read(self.config.get('auth', {}).get('database', {}).get('ini_path', ''))
            
            # Look for Toybox sections
            toybox_sections = [section for section in config.sections() if section.startswith('Toybox-')]
            
            for section_name in toybox_sections:
                section = config[section_name]
                
                # Parse users, orgs, and projects
                users = [user.strip() for user in section.get("user", "").split(',') if user.strip()]
                orgs = [org.strip() for org in section.get("org", "").split(',') if org.strip()]  
                projects = [proj.strip() for proj in section.get("project", "").split(',') if proj.strip()]
                
                # Check authorization
                if (user_idsid in users) and (project_name in projects):
                    return True
                    
            return False
            
        except Exception as e:
            st.error(f"Authorization check failed: {e}")
            return False
    
    def logout(self):
        """Clear user session"""
        for key in list(st.session_state.keys()):
            if key.startswith(('current_user', 'cookies', 'user_')):
                del st.session_state[key]