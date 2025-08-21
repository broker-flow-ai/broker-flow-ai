import mysql.connector
import json
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from datetime import datetime, timedelta

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def populate_audit_log():
    conn = get_db_connection()
    cursor = conn.cursor()
    
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

if __name__ == "__main__":
    populate_audit_log()