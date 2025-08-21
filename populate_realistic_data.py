import mysql.connector
import random
from datetime import datetime, timedelta
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def populate_policies_claims_premiums():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Definisci tipi di rischio e settori
    risk_types = ["Flotta Auto", "RC Professionale", "Fabbricato", "Rischi Tecnici"]
    sectors = ["Trasporti", "Sanità", "Edilizia", "Tecnologia", "Commercio", "Industria", "Agricoltura"]
    
    # Aggiorna i settori dei clienti esistenti
    cursor.execute("SELECT id FROM clients")
    client_ids = [row[0] for row in cursor.fetchall()]
    
    for client_id in client_ids:
        sector = random.choice(sectors)
        cursor.execute("UPDATE clients SET sector = %s WHERE id = %s", (sector, client_id))
    
    # Genera polizze, premi e sinistri per i prossimi 2 anni
    policy_id_counter = 1
    claim_id_counter = 1
    premium_id_counter = 1
    
    for client_id in client_ids:
        # Genera 3-5 polizze per cliente negli ultimi 2 anni
        num_policies = random.randint(3, 5)
        
        for _ in range(num_policies):
            # Seleziona un tipo di rischio casuale
            risk_type = random.choice(risk_types)
            
            # Genera dati della polizza
            start_date = datetime.now() - timedelta(days=random.randint(0, 730))
            end_date = start_date + timedelta(days=365)
            status = random.choices(["active", "expired", "cancelled"], weights=[0.7, 0.25, 0.05])[0]
            policy_number = f"POL{datetime.now().year}{random.randint(1000, 9999)}"
            
            # Inserisci il rischio
            cursor.execute("""
                INSERT INTO risks (client_id, risk_type, details)
                VALUES (%s, %s, %s)
            """, (client_id, risk_type, '{"source": "data_enrichment"}'))
            risk_id = cursor.lastrowid
            
            # Inserisci la polizza
            cursor.execute("""
                INSERT INTO policies (risk_id, company_id, company, policy_number, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (risk_id, client_id, "BrokerFlow AI", policy_number, start_date.date(), end_date.date(), status))
            policy_id = cursor.lastrowid
            
            # Genera premi per la polizza (mensili)
            for month in range(12):
                payment_date = start_date + timedelta(days=30*month)
                if payment_date > datetime.now():
                    break
                    
                amount = random.uniform(500, 5000)
                due_date = payment_date + timedelta(days=30)
                payment_status = random.choices(["paid", "pending", "overdue"], weights=[0.8, 0.15, 0.05])[0]
                
                cursor.execute("""
                    INSERT INTO premiums (policy_id, amount, due_date, payment_status, payment_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (policy_id, amount, due_date.date(), payment_status, payment_date.date() if payment_status == "paid" else None))
            
            # Genera sinistri occasionali (10% di probabilità)
            if random.random() < 0.1:
                claim_date = start_date + timedelta(days=random.randint(30, 330))
                claim_amount = random.uniform(1000, 10000)
                claim_status = random.choices(["open", "in_review", "approved", "rejected"], weights=[0.1, 0.2, 0.6, 0.1])[0]
                
                cursor.execute("""
                    INSERT INTO claims (policy_id, claim_date, amount, status, description)
                    VALUES (%s, %s, %s, %s, %s)
                """, (policy_id, claim_date.date(), claim_amount, claim_status, f"Sinistro {risk_type}"))
    
    conn.commit()
    conn.close()
    print("Dati di polizze, sinistri e premi generati con successo!")

if __name__ == "__main__":
    populate_policies_claims_premiums()