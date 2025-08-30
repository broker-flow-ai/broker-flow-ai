import streamlit as st
from functools import wraps
from typing import List, Optional

def require_authentication(func):
    """Decorator per richiedere l'autenticazione"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica che l'utente sia autenticato
        if not st.session_state.get('authenticated', False) or not st.session_state.get('user', None):
            st.warning("⚠️ Devi effettuare il login per accedere a questa sezione")
            from pages.login import login_page
            login_page()
            return None
        return func(*args, **kwargs)
    return wrapper

def require_role(allowed_roles: List[str]):
    """Decorator per richiedere uno specifico ruolo"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verifica che l'utente sia autenticato
            if not st.session_state.get('authenticated', False) or not st.session_state.get('user', None):
                st.warning("⚠️ Devi effettuare il login per accedere a questa sezione")
                from pages.login import login_page
                login_page()
                return None
            
            # Verifica il ruolo dell'utente
            user_role = st.session_state.user.get('role', 'viewer') if isinstance(st.session_state.user, dict) else 'viewer'
            if user_role not in allowed_roles:
                st.error(f"❌ Accesso negato. Solo i seguenti ruoli possono accedere: {', '.join(allowed_roles)}")
                st.info(f"Il tuo ruolo è: {user_role}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_permission(required_permission: str) -> bool:
    """Verifica se l'utente ha un permesso specifico"""
    # Verifica che l'utente sia autenticato
    if not st.session_state.get('authenticated', False) or not st.session_state.get('user', None):
        return False
    
    # Per ora implementiamo un controllo semplice basato sui ruoli
    # In futuro si potrebbe estendere con permessi specifici
    user_role = st.session_state.user.get('role', 'viewer') if isinstance(st.session_state.user, dict) else 'viewer'
    
    # Mappa dei permessi per ruolo
    role_permissions = {
        'admin': ['view_all', 'manage_all', 'create', 'delete', 'modify'],
        'broker': ['view_clients', 'manage_clients', 'view_policies', 'manage_policies', 
                  'view_claims', 'manage_claims', 'view_risks', 'manage_risks', 'create', 'delete'],
        'underwriter': ['view_risks', 'analyze_risks', 'view_policies'],
        'claims_adjuster': ['view_claims', 'manage_claims', 'view_policies'],
        'customer_service': ['view_clients', 'view_policies', 'view_claims'],
        'viewer': ['view_only']
    }
    
    permissions = role_permissions.get(user_role, [])
    return required_permission in permissions or required_permission == 'view_all' or 'manage_all' in permissions

def has_create_permission() -> bool:
    """Verifica se l'utente ha il permesso di creare"""
    return check_permission('create')

def has_delete_permission() -> bool:
    """Verifica se l'utente ha il permesso di eliminare"""
    return check_permission('delete')

def has_modify_permission() -> bool:
    """Verifica se l'utente ha il permesso di modificare"""
    return check_permission('modify')