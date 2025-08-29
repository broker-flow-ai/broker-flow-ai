#!/usr/bin/env python3
"""
Script per creare l'utente admin di default
"""
import sys
import os
import mysql.connector

# Aggiungi il path per i moduli locali
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def create_admin_user():
    """Crea l'utente admin di default"""
    try:
        # Connessione al database
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()
        
        # Verifica se esiste già un admin
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            print("✅ Utente admin già esistente")
            return True
        
        # Import passlib per l'hashing delle password
        try:
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            get_password_hash = lambda p: pwd_context.hash(p)
        except ImportError:
            print("❌ Modulo passlib non disponibile")
            # Usa una password hashata pre-calcolata per admin123
            hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S"
            print("⚠️  Usando password hashata pre-calcolata")
        else:
            hashed_password = get_password_hash("admin123")
        
        # Crea l'utente admin
        cursor.execute("""
            INSERT INTO users (username, email, full_name, hashed_password, role, status, is_two_factor_enabled)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("admin", "lantoniotrento@gmail.com", "Amministratore di Sistema", hashed_password, "admin", "active", False))
        
        conn.commit()
        print("✅ Utente admin creato con successo!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   ⚠️  Cambia la password dopo il primo accesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nella creazione dell'utente admin: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("CREAZIONE UTENTE ADMIN - BrokerFlow AI")
    print("=" * 50)
    
    success = create_admin_user()
    
    if success:
        print("\n🎉 Utente admin pronto per l'uso!")
    else:
        print("\n❌ Errore nella creazione dell'utente admin")
        sys.exit(1)