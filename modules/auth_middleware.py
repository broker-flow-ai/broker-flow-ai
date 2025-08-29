from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import jwt
from modules.auth import decode_access_token, get_user
from modules.auth_models import TokenData, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Permessi richiesti per ogni endpoint
ENDPOINT_PERMISSIONS = {
    # Clienti
    "/api/v1/clients": ["view_clients", "manage_clients"],
    "/api/v1/clients/{client_id}": ["view_clients", "manage_clients"],
    
    # Polizze
    "/api/v1/policies": ["view_policies", "manage_policies"],
    "/api/v1/policies/{policy_id}": ["view_policies", "manage_policies"],
    
    # Sinistri
    "/api/v1/claims": ["view_claims", "manage_claims"],
    "/api/v1/claims/{claim_id}": ["view_claims", "manage_claims"],
    
    # Rischi
    "/api/v1/risks": ["view_risks", "manage_risks"],
    "/api/v1/risks/{risk_id}": ["view_risks", "manage_risks"],
    
    # Report di compliance
    "/api/v1/insurance/compliance-report": ["generate_reports"],
    "/api/v1/insurance/compliance-reports": ["view_reports"],
    
    # Dashboard analytics
    "/api/v1/insurance/portfolio-analytics": ["view_analytics"],
    "/api/v1/insurance/company-performance": ["view_analytics"],
    "/api/v1/insurance/broker-metrics": ["view_analytics"],
    
    # Sconti
    "/api/v1/insurance/discounts": ["manage_discounts"],
    
    # Metriche di sistema
    "/api/v1/metrics": ["view_system"],
    
    # Altri endpoint che richiedono autenticazione
    "/api/v1/health": ["view_system"]
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Ottiene l'utente corrente dal token JWT"""
    token_data = decode_access_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user(token_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utente non trovato",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def require_permission(permission: str):
    """Decorator per richiedere un permesso specifico"""
    def permission_checker(current_user = Depends(get_current_user)):
        from modules.auth import has_permission
        if not has_permission(UserRole(current_user.role), permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permesso '{permission}' richiesto"
            )
        return current_user
    return permission_checker

def require_role(required_role: UserRole):
    """Decorator per richiedere un ruolo specifico"""
    def role_checker(current_user = Depends(get_current_user)):
        if UserRole(current_user.role) != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Ruolo '{required_role.value}' richiesto"
            )
        return current_user
    return role_checker

def check_endpoint_permission(endpoint: str, method: str, current_user):
    """Verifica i permessi per un endpoint specifico"""
    from modules.auth import has_permission
    
    # Trova i permessi richiesti per l'endpoint
    required_permissions = ENDPOINT_PERMISSIONS.get(endpoint, [])
    
    # Se non ci sono permessi specifici, permetti l'accesso
    if not required_permissions:
        return True
    
    # Verifica se l'utente ha almeno uno dei permessi richiesti
    user_role = UserRole(current_user.role)
    for permission in required_permissions:
        if has_permission(user_role, permission):
            return True
    
    return False