from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Optional, List
import time
from datetime import datetime, timedelta
from modules.auth import (
    authenticate_user, create_access_token, decode_access_token,
    get_user, get_user_by_email, create_user, update_user,
    generate_otp_code, save_otp_token, verify_otp_token, send_otp_email,
    reset_failed_login_attempts, increment_failed_login_attempts,
    is_account_locked, lock_user_account, get_all_users, delete_user,
    ENABLE_2FA
)
from modules.auth_models import (
    UserCreate, UserUpdate, User, Token, TwoFactorRequest, 
    TwoFactorVerify, UserRole, UserStatus, UserListResponse, UserInDB
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

def require_admin(current_user: User = Depends(get_current_user)):
    """Verifica che l'utente abbia ruolo admin"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Richiesto ruolo amministratore"
        )
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint per il login e ottenere il token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        # Incrementa i tentativi falliti
        increment_failed_login_attempts(form_data.username)
        
        # Blocca l'account se necessario
        user_obj = get_user(form_data.username)
        if user_obj and user_obj.failed_login_attempts >= 5:  # 5 tentativi massimi
            lock_user_account(form_data.username, 30)  # Blocca per 30 minuti
        
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
    
    # Se il 2FA è abilitato e attivo per l'utente, richiedi il token
    if ENABLE_2FA and user.is_two_factor_enabled:
        # Genera e invia il codice OTP
        otp_code = generate_otp_code()
        save_otp_token(user.id, otp_code)
        send_otp_email(user.email, otp_code, user.username)
        
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
    if not ENABLE_2FA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA non è abilitato nel sistema"
        )
    
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
    
    # Genera e invia il codice OTP
    otp_code = generate_otp_code()
    save_otp_token(user.id, otp_code)
    send_otp_email(user.email, otp_code, user.username)
    
    return {"message": "Codice 2FA inviato all'email"}

@router.post("/two-factor/verify", response_model=Token)
async def verify_two_factor_token_endpoint(two_factor_verify: TwoFactorVerify):
    """Endpoint per verificare il token 2FA e ottenere il token di accesso"""
    if not ENABLE_2FA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA non è abilitato nel sistema"
        )
    
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
    
    # Verifica il token OTP
    if not verify_otp_token(user.id, two_factor_verify.token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Codice 2FA non valido o scaduto"
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
async def create_new_user(user: UserCreate, current_user: User = Depends(require_admin)):
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

@router.get("/users/", response_model=UserListResponse)
async def list_users(current_user: User = Depends(require_admin)):
    """Endpoint per ottenere la lista di tutti gli utenti"""
    try:
        users_db = get_all_users()
        # Converti gli oggetti in dizionari e poi in oggetti User
        users_list = []
        for user_db in users_db:
            # Se è già un dizionario, crea direttamente l'oggetto User
            if isinstance(user_db, dict):
                user = User(**user_db)
                users_list.append(user)
            else:
                # Se è un oggetto Pydantic, convertilo in dizionario e poi in User
                user_data = user_db.model_dump()
                user = User(**user_data)
                users_list.append(user)
        return UserListResponse(users=users_list)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore nel recupero degli utenti: {str(e)}"
        )

@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    """Endpoint per ottenere un utente specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_row = cursor.fetchone()
    conn.close()
    
    if not user_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    # Gestisci i campi che potrebbero essere NULL nel database
    if user_row.get('locked_until') is not None and isinstance(user_row.get('locked_until'), datetime):
        user_row['locked_until'] = user_row['locked_until'].isoformat()
    elif user_row.get('locked_until') is None:
        user_row['locked_until'] = None
        
    if user_row.get('last_login') is not None and isinstance(user_row.get('last_login'), datetime):
        user_row['last_login'] = user_row['last_login'].isoformat()
    elif user_row.get('last_login') is None:
        user_row['last_login'] = None
        
    # Converti i datetime in stringhe se necessario
    if isinstance(user_row.get('created_at'), datetime):
        user_row['created_at'] = user_row['created_at'].isoformat()
    if isinstance(user_row.get('updated_at'), datetime):
        user_row['updated_at'] = user_row['updated_at'].isoformat()
    
    return User(**user_row)


@router.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, current_user: User = Depends(require_admin)):
    """Endpoint per eliminare un utente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica che l'utente esista
    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    # Elimina l'utente
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Errore nell'eliminazione dell'utente"
        )
    
    return {"message": "Utente eliminato con successo"}

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

@router.put("/users/{user_id}", response_model=User)
async def update_user_endpoint(user_id: int, user_update: UserUpdate, current_user: User = Depends(require_admin)):
    """Endpoint per aggiornare un utente esistente"""
    try:
        print(f"[DEBUG] Updating user {user_id}")
        
        # Verifica che l'utente esista
        print(f"[DEBUG] Checking if user {user_id} exists")
        existing_user = get_user_by_id(user_id)
        if not existing_user:
            print(f"[DEBUG] User {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utente non trovato"
            )
        
        # Aggiorna l'utente
        update_data = user_update.dict(exclude_unset=True)
        print(f"[DEBUG] Update data: {update_data}")
        
        if update_data:
            print(f"[DEBUG] Calling update_user function")
            success = update_user(user_id, update_data)
            print(f"[DEBUG] Update function returned: {success}")
            
            # Anche se success è False, potrebbe essere perché non ci sono modifiche
            # Controlliamo comunque se l'utente esiste ancora
            print(f"[DEBUG] Checking user after update")
            updated_user = get_user_by_id(user_id)
            if not updated_user:
                print(f"[DEBUG] User not found after update")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Errore nell'aggiornamento dell'utente"
                )
            # Se l'utente esiste, consideriamo l'operazione andata a buon fine
        
        # Recupera l'utente aggiornato
        print(f"[DEBUG] Retrieving updated user {user_id}")
        updated_user = get_user_by_id(user_id)
        if not updated_user:
            print(f"[DEBUG] Updated user {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utente non trovato dopo l'aggiornamento"
            )
        
        print(f"[DEBUG] Returning updated user: {updated_user}")
        return updated_user
    except HTTPException as he:
        # Ri-lancia le eccezioni HTTP già create
        print(f"[DEBUG] HTTP Exception caught: {he.detail}")
        raise
    except Exception as e:
        # Gestisci gli errori generici
        print(f"[ERROR] Unexpected error updating user: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore nell'aggiornamento dell'utente: {str(e)}"
        )

@router.post("/users/{user_id}/enable-2fa")
async def enable_two_factor(user_id: int, current_user: User = Depends(require_admin)):
    """Endpoint per abilitare il 2FA per un utente"""
    # Verifica che l'utente abbia i permessi per modificare altri utenti
    # Solo admin o l'utente stesso può modificare le impostazioni 2FA
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permesso negato"
        )
    
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
async def disable_two_factor(user_id: int, current_user: User = Depends(require_admin)):
    """Endpoint per disabilitare il 2FA per un utente"""
    # Verifica che l'utente abbia i permessi per modificare altri utenti
    # Solo admin o l'utente stesso può modificare le impostazioni 2FA
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permesso negato"
        )
    
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