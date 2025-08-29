from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional
import time
from datetime import datetime, timedelta
from modules.auth import (
    authenticate_user, create_access_token, decode_access_token,
    get_user, get_user_by_email, create_user, update_user,
    generate_two_factor_token, save_two_factor_token, verify_two_factor_token,
    send_two_factor_email, reset_failed_login_attempts, increment_failed_login_attempts,
    is_account_locked, lock_user_account
)
from modules.auth_models import (
    UserCreate, UserUpdate, User, Token, TwoFactorRequest, 
    TwoFactorVerify, UserRole, UserStatus
)
from modules.db import get_db_connection

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

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

# Costanti per la sicurezza
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint per il login e ottenere il token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        # Incrementa i tentativi falliti
        increment_failed_login_attempts(form_data.username)
        
        # Blocca l'account se necessario
        user_obj = get_user(form_data.username)
        if user_obj and user_obj.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
            lock_user_account(form_data.username, LOCKOUT_DURATION_MINUTES)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o password non corretti",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se l'account è bloccato
    if is_account_locked(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account temporaneamente bloccato. Riprova più tardi.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Se il 2FA è abilitato, richiedi il token
    if user.is_two_factor_enabled:
        # Genera e invia il token 2FA
        two_factor_token = generate_two_factor_token()
        save_two_factor_token(user.id, two_factor_token)
        send_two_factor_email(user.email, two_factor_token)
        
        # Ritorna una risposta speciale per indicare che è necessario il 2FA
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="2FA_REQUIRED"
        )
    
    # Resetta i tentativi falliti
    reset_failed_login_attempts(form_data.username)
    
    # Crea il token di accesso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/two-factor/request")
async def request_two_factor_token(two_factor_request: TwoFactorRequest):
    """Endpoint per richiedere il token 2FA"""
    user = authenticate_user(two_factor_request.username, two_factor_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o password non corretti"
        )
    
    if not user.is_two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA non è abilitato per questo utente"
        )
    
    # Genera e invia il token 2FA
    two_factor_token = generate_two_factor_token()
    save_two_factor_token(user.id, two_factor_token)
    send_two_factor_email(user.email, two_factor_token)
    
    return {"message": "Codice 2FA inviato all'email"}

@router.post("/two-factor/verify", response_model=Token)
async def verify_two_factor_token_endpoint(two_factor_verify: TwoFactorVerify):
    """Endpoint per verificare il token 2FA e ottenere il token di accesso"""
    user = get_user(two_factor_verify.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utente non trovato"
        )
    
    if not user.is_two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA non è abilitato per questo utente"
        )
    
    # Verifica il token
    if not verify_two_factor_token(user.id, two_factor_verify.token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 2FA non valido o scaduto"
        )
    
    # Resetta i tentativi falliti
    reset_failed_login_attempts(two_factor_verify.username)
    
    # Crea il token di accesso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=User)
async def create_new_user(user: UserCreate):
    """Endpoint per creare un nuovo utente"""
    # Verifica che l'username o l'email non esistano già
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username già esistente"
        )
    
    existing_email = get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email già registrata"
        )
    
    # Crea l'utente
    user_id = create_user(user.dict())
    
    # Recupera l'utente creato
    created_user = get_user(user.username)
    return created_user

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Endpoint per ottenere le informazioni dell'utente corrente"""
    return current_user

@router.put("/users/me/", response_model=User)
async def update_user_me(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    """Endpoint per aggiornare le informazioni dell'utente corrente"""
    # Aggiorna l'utente
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        success = update_user(current_user.id, update_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Errore nell'aggiornamento dell'utente"
            )
    
    # Recupera l'utente aggiornato
    updated_user = get_user(current_user.username)
    return updated_user

@router.post("/users/{user_id}/enable-2fa")
async def enable_two_factor(user_id: int):
    """Endpoint per abilitare il 2FA per un utente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET is_two_factor_enabled = TRUE WHERE id = %s", (user_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    return {"message": "2FA abilitato con successo"}

@router.post("/users/{user_id}/disable-2fa")
async def disable_two_factor(user_id: int):
    """Endpoint per disabilitare il 2FA per un utente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET is_two_factor_enabled = FALSE WHERE id = %s", (user_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    return {"message": "2FA disabilitato con successo"}