import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, EMAIL_CONFIG
from modules.db import get_db_connection
from modules.auth_models import UserInDB, User, TokenData, UserRole

# Configurazione della password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funzioni di utilità per le password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Funzioni di utilità per i token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            return None
        return TokenData(username=username, role=role)
    except jwt.JWTError:
        return None

# Funzioni per la gestione degli utenti
def get_user(username: str) -> Optional[UserInDB]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user_row = cursor.fetchone()
    conn.close()
    
    if user_row:
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
            
        return UserInDB(**user_row)
    return None

def get_user_by_email(email: str) -> Optional[UserInDB]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_row = cursor.fetchone()
    conn.close()
    
    if user_row:
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
            
        return UserInDB(**user_row)
    return None

def create_user(user_data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = get_password_hash(user_data["password"])
    
    query = """
        INSERT INTO users (username, email, full_name, hashed_password, role, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        user_data["username"],
        user_data["email"],
        user_data["full_name"],
        hashed_password,
        user_data["role"],
        user_data["status"] if "status" in user_data else "pending"
    )
    
    cursor.execute(query, params)
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return user_id

def update_user(user_id: int, user_data: Dict[str, Any]) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruisci la query dinamicamente
    set_parts = []
    params = []
    
    for key, value in user_data.items():
        if key == "password":
            set_parts.append("hashed_password = %s")
            params.append(get_password_hash(value))
        elif key in ["username", "email", "full_name", "role", "status", "is_two_factor_enabled"]:
            set_parts.append(f"{key} = %s")
            params.append(value)
    
    if not set_parts:
        return False
    
    params.append(user_id)
    query = f"UPDATE users SET {', '.join(set_parts)} WHERE id = %s"
    
    cursor.execute(query, params)
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Funzioni per la gestione delle sessioni
def create_session(user_id: int, session_token: str, expires_at: datetime, ip_address: str = None, user_agent: str = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (user_id, session_token, expires_at, ip_address, user_agent)
    
    cursor.execute(query, params)
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return session_id

def get_session(session_token: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT us.*, u.username, u.role 
        FROM user_sessions us 
        JOIN users u ON us.user_id = u.id 
        WHERE us.session_token = %s AND us.expires_at > NOW()
    """, (session_token,))
    
    session = cursor.fetchone()
    conn.close()
    
    return session

def delete_session(session_token: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM user_sessions WHERE session_token = %s", (session_token,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

# Funzioni per la gestione del 2FA
def generate_two_factor_token() -> str:
    """Genera un token 2FA a 6 cifre"""
    return str(secrets.randbelow(1000000)).zfill(6)

def save_two_factor_token(user_id: int, token: str, expires_in_minutes: int = 10) -> int:
    """Salva un token 2FA nel database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    
    query = """
        INSERT INTO two_factor_tokens (user_id, token, expires_at)
        VALUES (%s, %s, %s)
    """
    params = (user_id, token, expires_at)
    
    cursor.execute(query, params)
    token_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return token_id

def verify_two_factor_token(user_id: int, token: str) -> bool:
    """Verifica un token 2FA"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM two_factor_tokens 
        WHERE user_id = %s AND token = %s AND expires_at > NOW() AND used = FALSE
    """, (user_id, token))
    
    token_record = cursor.fetchone()
    conn.close()
    
    if token_record:
        # Segna il token come usato
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE two_factor_tokens SET used = TRUE WHERE id = %s", (token_record['id'],))
        conn.commit()
        conn.close()
        return True
    
    return False

def send_two_factor_email(email: str, token: str) -> bool:
    """Invia il token 2FA via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = email
        msg['Subject'] = "Codice di Verifica 2FA - BrokerFlow AI"
        
        body = f"""
        Il tuo codice di verifica 2FA per BrokerFlow AI è: {token}
        
        Questo codice scadrà tra 10 minuti.
        
        Se non hai richiesto questo codice, ignora questa email.
        
        Grazie,
        Team BrokerFlow AI
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        if EMAIL_CONFIG['smtp_port'] == 465:
            server = smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        else:
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
        
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Errore nell'invio dell'email 2FA: {str(e)}")
        return False

# Funzioni per la gestione dei permessi
def get_user_permissions(role: UserRole) -> list:
    """Recupera i permessi per un ruolo specifico"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.name 
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        WHERE rp.role = %s
    """, (role.value,))
    
    permissions = [row['name'] for row in cursor.fetchall()]
    conn.close()
    
    return permissions

def has_permission(user_role: UserRole, permission: str) -> bool:
    """Verifica se un ruolo ha un permesso specifico"""
    permissions = get_user_permissions(user_role)
    return permission in permissions

# Funzioni per la gestione dei tentativi di login falliti
def increment_failed_login_attempts(username: str) -> int:
    """Incrementa i tentativi di login falliti"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET failed_login_attempts = failed_login_attempts + 1 
        WHERE username = %s
    """, (username,))
    
    conn.commit()
    conn.close()
    
    # Recupera il nuovo valore
    user = get_user(username)
    return user.failed_login_attempts if user else 0

def reset_failed_login_attempts(username: str) -> bool:
    """Resetta i tentativi di login falliti"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET failed_login_attempts = 0, locked_until = NULL 
        WHERE username = %s
    """, (username,))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

def lock_user_account(username: str, lock_duration_minutes: int = 30) -> bool:
    """Blocca un account per un periodo specifico"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    locked_until = datetime.utcnow() + timedelta(minutes=lock_duration_minutes)
    
    cursor.execute("""
        UPDATE users 
        SET locked_until = %s 
        WHERE username = %s
    """, (locked_until, username))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    return success

def is_account_locked(username: str) -> bool:
    """Verifica se un account è bloccato"""
    user = get_user(username)
    if not user or not user.locked_until:
        return False
    
    # Converti locked_until in datetime se è una stringa
    if isinstance(user.locked_until, str):
        from datetime import datetime
        locked_until = datetime.fromisoformat(user.locked_until.replace('Z', '+00:00'))
    else:
        locked_until = user.locked_until
    
    return locked_until > datetime.utcnow()