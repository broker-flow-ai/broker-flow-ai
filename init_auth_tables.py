#!/usr/bin/env python3
"""
Script per inizializzare le tabelle di autenticazione nel database
"""
import sys
import os
import mysql.connector

# Aggiungi il path per i moduli locali
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def init_auth_tables():
    """Inizializza le tabelle di autenticazione nel database"""
    try:
        # Connessione al database
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()
        
        # Crea le tabelle di autenticazione
        print("Creazione tabelle di autenticazione...")
        
        # Tabella utenti
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'broker', 'underwriter', 'claims_adjuster', 'customer_service', 'viewer') NOT NULL,
                status ENUM('active', 'inactive', 'pending', 'suspended') DEFAULT 'pending',
                is_two_factor_enabled BOOLEAN DEFAULT FALSE,
                two_factor_secret VARCHAR(255),
                last_login TIMESTAMP NULL,
                failed_login_attempts INT DEFAULT 0,
                locked_until TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabella 'users' creata")
        
        # Tabella permessi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS permissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabella 'permissions' creata")
        
        # Tabella associazione ruoli-permessi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_permissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role ENUM('admin', 'broker', 'underwriter', 'claims_adjuster', 'customer_service', 'viewer') NOT NULL,
                permission_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
                UNIQUE KEY unique_role_permission (role, permission_id)
            )
        """)
        print("✅ Tabella 'role_permissions' creata")
        
        # Tabella token 2FA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS two_factor_tokens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                token VARCHAR(6) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabella 'two_factor_tokens' creata")
        
        # Tabella sessioni utente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                session_token VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("✅ Tabella 'user_sessions' creata")
        
        conn.commit()
        print("\n🎉 Tutte le tabelle di autenticazione sono state create con successo!")
        
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione delle tabelle: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_auth_tables()