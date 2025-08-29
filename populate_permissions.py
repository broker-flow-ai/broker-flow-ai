#!/usr/bin/env python3
"""
Script per popolare le tabelle di permessi e ruoli nel database
"""
import sys
import os

# Aggiungi il path per i moduli locali
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from modules.db import get_db_connection

def populate_permissions():
    """Popola la tabella dei permessi con i permessi di base"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Permessi di base
    permissions = [
        ("view_clients", "Visualizzare la lista dei clienti"),
        ("manage_clients", "Creare, modificare ed eliminare clienti"),
        ("view_policies", "Visualizzare la lista delle polizze"),
        ("manage_policies", "Creare, modificare ed eliminare polizze"),
        ("view_claims", "Visualizzare la lista dei sinistri"),
        ("manage_claims", "Creare, modificare ed eliminare sinistri"),
        ("view_risks", "Visualizzare la lista dei rischi"),
        ("manage_risks", "Creare, modificare ed eliminare rischi"),
        ("generate_reports", "Generare report di compliance"),
        ("view_reports", "Visualizzare report di compliance esistenti"),
        ("view_analytics", "Visualizzare analisi e dashboard"),
        ("manage_discounts", "Gestire programmi sconto e fedeltà"),
        ("view_system", "Visualizzare metriche di sistema"),
        ("manage_users", "Gestire utenti e permessi"),
        ("view_audit", "Visualizzare log di audit")
    ]
    
    try:
        # Inserisci i permessi
        for name, description in permissions:
            cursor.execute("""
                INSERT IGNORE INTO permissions (name, description) 
                VALUES (%s, %s)
            """, (name, description))
        
        conn.commit()
        print(f"✅ Inseriti {cursor.rowcount} permessi")
        
        # Associa i permessi ai ruoli
        role_permissions = {
            "admin": [name for name, _ in permissions],  # Admin ha tutti i permessi
            "broker": [
                "view_clients", "manage_clients",
                "view_policies", "manage_policies",
                "view_claims", "manage_claims",
                "view_risks", "manage_risks",
                "view_reports", "generate_reports",
                "view_analytics"
            ],
            "underwriter": [
                "view_clients", "view_policies", "view_risks",
                "view_analytics", "view_reports"
            ],
            "claims_adjuster": [
                "view_clients", "view_policies", "view_claims", "manage_claims",
                "view_analytics"
            ],
            "customer_service": [
                "view_clients", "view_policies", "view_claims",
                "view_risks", "view_reports"
            ],
            "viewer": [
                "view_clients", "view_policies", "view_claims",
                "view_risks", "view_reports", "view_analytics"
            ]
        }
        
        # Inserisci le associazioni ruolo-permessi
        for role, perms in role_permissions.items():
            for perm_name in perms:
                cursor.execute("""
                    INSERT IGNORE INTO role_permissions (role, permission_id)
                    SELECT %s, id FROM permissions WHERE name = %s
                """, (role, perm_name))
        
        conn.commit()
        print("✅ Associazioni ruolo-permessi create")
        
    except Exception as e:
        print(f"❌ Errore nel popolamento dei permessi: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def create_default_admin():
    """Crea un utente admin di default"""
    # Import qui per evitare problemi di dipendenze circolari
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        get_password_hash = lambda p: pwd_context.hash(p)
    except ImportError:
        print("❌ Modulo passlib non disponibile, impossibile creare l'utente admin")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verifica se esiste già un admin
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            print("✅ Utente admin già esistente")
            return
        
        # Crea l'utente admin
        hashed_password = get_password_hash("admin123")
        cursor.execute("""
            INSERT INTO users (username, email, full_name, hashed_password, role, status, is_two_factor_enabled)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("admin", "lantoniotrento@gmail.com", "Amministratore di Sistema", hashed_password, "admin", "active", False))
        
        conn.commit()
        print("✅ Utente admin creato (username: admin, password: admin123)")
        
    except Exception as e:
        print(f"❌ Errore nella creazione dell'admin: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Funzione principale"""
    print("=" * 60)
    print("POPOLAMENTO PERMESSI E RUOLI - BrokerFlow AI")
    print("=" * 60)
    
    populate_permissions()
    create_default_admin()
    
    print("\n🎉 Popolamento completato con successo!")

if __name__ == "__main__":
    main()