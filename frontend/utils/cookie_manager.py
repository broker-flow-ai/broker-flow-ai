import streamlit as st
import json
import base64
import time
from typing import Optional, Dict, Any

class CookieManager:
    def __init__(self):
        # Simple in-memory storage for Docker environment
        # This will work as long as the container is running
        if 'auth_storage' not in st.session_state:
            st.session_state.auth_storage = {}
    
    def save_auth_cookie(self, token: str, user_info: Dict[str, Any]) -> bool:
        """Save authentication data to session state (works in Docker)"""
        try:
            # Create a dictionary with all auth data
            auth_data = {
                "access_token": token,
                "user": user_info,
                "timestamp": time.time()
            }
            
            # Store in session state
            st.session_state.auth_storage = auth_data
            return True
        except Exception as e:
            st.error(f"Error saving auth data: {str(e)}")
            return False
    
    def load_auth_cookie(self) -> Optional[Dict[str, Any]]:
        """Load authentication data from session state"""
        try:
            auth_data = st.session_state.get("auth_storage", {})
            
            if auth_data:
                # Check if token is still valid (less than 24 hours old)
                timestamp = auth_data.get("timestamp", 0)
                if time.time() - timestamp < 24 * 60 * 60:  # 24 hours
                    # Validate that we have the necessary fields
                    if "access_token" in auth_data and "user" in auth_data:
                        return auth_data
                else:
                    # Token expired, clear it
                    self.clear_auth_cookie()
        except Exception as e:
            st.error(f"Error loading auth data: {str(e)}")
        
        return None
    
    def clear_auth_cookie(self) -> bool:
        """Clear authentication data from session state"""
        try:
            st.session_state.auth_storage = {}
            return True
        except Exception as e:
            st.error(f"Error clearing auth data: {str(e)}")
            return False