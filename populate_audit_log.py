import mysql.connector
import json
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from datetime import datetime, timedelta
import time

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def table_exists(cursor, table_name):
    """Controlla se una tabella esiste nel database"""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
    """, (MYSQL_DATABASE, table_name))
    return cursor.fetchone()[0] > 0

def populate_audit_log():
    # Attendi che il database sia pronto
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Controlla se la tabella audit_log esiste
            if not table_exists(cursor, 'audit_log'):
                print("Tabella audit_log non trovata. Attendo che lo schema venga applicato...")
                conn.close()
                retry_count += 1
                time.sleep(2)
                continue
            
            # Inserisci alcuni dati di esempio nell'audit log
            audit_data = [
                ("clients", "INSERT", datetime.now() - timedelta(days=30), 1, {"action": "New client registration", "client_id": 1}),
                ("policies", "INSERT", datetime.now() - timedelta(days=25), 1, {"action": "Policy created", "policy_id": 1}),
                ("risks", "INSERT", datetime.now() - timedelta(days=25), 1, {"action": "Risk assessment", "risk_id": 1}),
                ("clients", "UPDATE", datetime.now() - timedelta(days=20), 2, {"action": "Client data updated", "client_id": 2}),
                ("policies", "INSERT", datetime.now() - timedelta(days=15), 2, {"action": "Policy created", "policy_id": 2}),
                ("risks", "INSERT", datetime.now() - timedelta(days=15), 2, {"action": "Risk assessment", "risk_id": 2}),
                ("claims", "INSERT", datetime.now() - timedelta(days=10), 1, {"action": "Claim filed", "claim_id": 1}),
                ("clients", "INSERT", datetime.now() - timedelta(days=5), 3, {"action": "New client registration", "client_id": 3}),
                ("policies", "INSERT", datetime.now() - timedelta(days=3), 3, {"action": "Policy created", "policy_id": 3}),
                ("risks", "INSERT", datetime.now() - timedelta(days=3), 3, {"action": "Risk assessment", "risk_id": 3}),
            ]
            
            for table_name, action, timestamp, user_id, details in audit_data:
                cursor.execute("""
                    INSERT INTO audit_log (table_name, action, timestamp, user_id, details)
                    VALUES (%s, %s, %s, %s, %s)
                """, (table_name, action, timestamp, user_id, json.dumps(details)))
            
            conn.commit()
            conn.close()
            print("Audit log populated with sample data")
            return
            
        except mysql.connector.Error as e:
            if conn:
                conn.close()
            print(f"Errore nel database (tentativo {retry_count + 1}/{max_retries}): {e}")
            retry_count += 1
            time.sleep(2)
        except Exception as e:
            if conn:
                conn.close()
            print(f"Errore generico (tentativo {retry_count + 1}/{max_retries}): {e}")
            retry_count += 1
            time.sleep(2)
    
    print("Impossibile popolare l'audit log dopo {max_retries} tentativi")
    return

if __name__ == "__main__":
    populate_audit_log()