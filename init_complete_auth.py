#!/usr/bin/env python3
"""
Script completo per inizializzare il sistema di autenticazione
"""
import sys
import os

# Aggiungi il path per i moduli locali
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

def main():
    """Funzione principale per inizializzare tutto il sistema di autenticazione"""
    print("=" * 60)
    print("INIZIALIZZAZIONE COMPLETA SISTEMA DI AUTENTICAZIONE")
    print("=" * 60)
    
    # 1. Inizializza le tabelle nel database
    print("\n1. Inizializzazione tabelle di autenticazione...")
    try:
        import init_auth_tables
        init_auth_tables.init_auth_tables()
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione delle tabelle: {str(e)}")
        return False
    
    # 2. Popola i permessi e i ruoli
    print("\n2. Popolamento permessi e ruoli...")
    try:
        import populate_permissions
        populate_permissions.populate_permissions()
        print("✅ Permessi e ruoli popolati con successo")
    except Exception as e:
        print(f"❌ Errore nel popolamento dei permessi: {str(e)}")
        # Non interrompere l'esecuzione, continua comunque
    
    # 3. Crea l'utente admin
    print("\n3. Creazione utente admin...")
    try:
        import create_admin_user
        success = create_admin_user.create_admin_user()
        if not success:
            print("❌ Errore nella creazione dell'utente admin")
            return False
    except Exception as e:
        print(f"❌ Errore nella creazione dell'utente admin: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ SISTEMA DI AUTENTICAZIONE INIZIALIZZATO CON SUCCESSO!")
    print("=" * 60)
    print("\nCredenziali di default:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nRicorda di cambiare la password dopo il primo accesso!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)