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
    
    # Definisci tipi di rischio e settori con premi e sinistri realistici
    risk_data = {
        "Flotta Auto": {
            "sectors": ["Trasporti", "Logistica", "Noleggio"],
            "premium_range": (2000, 15000),
            "claim_probability": 0.15,
            "claim_range": (5000, 50000)
        },
        "RC Professionale": {
            "sectors": ["Sanità", "Legalità", "Ingegneria", "Architettura"],
            "premium_range": (1000, 8000),
            "claim_probability": 0.08,
            "claim_range": (10000, 100000)
        },
        "Fabbricato": {
            "sectors": ["Edilizia", "Commercio", "Industria"],
            "premium_range": (1500, 10000),
            "claim_probability": 0.12,
            "claim_range": (20000, 200000)
        },
        "Rischi Tecnici": {
            "sectors": ["Tecnologia", "Telecomunicazioni", "Elettronica"],
            "premium_range": (3000, 12000),
            "claim_probability": 0.10,
            "claim_range": (15000, 80000)
        }
    }
    
    # Seleziona i clienti esistenti con settore
    cursor.execute("SELECT id, sector FROM clients WHERE sector IS NOT NULL AND sector != 'Unknown'")
    clients = cursor.fetchall()
    
    if not clients:
        print("Nessun cliente con settore trovato. Popolamento annullato.")
        conn.close()
        return
    
    policy_counter = 1
    claim_counter = 1
    
    for client_id, sector in clients:
        # Trova il tipo di rischio appropriato per il settore
        risk_type = None
        for rt, data in risk_data.items():
            if sector in data["sectors"]:
                risk_type = rt
                break
        
        # Se non troviamo un rischio specifico, ne scegliamo uno casuale
        if not risk_type:
            risk_type = random.choice(list(risk_data.keys()))
        
        risk_info = risk_data[risk_type]
        
        # Genera 2-4 polizze per cliente negli ultimi 3 anni
        num_policies = random.randint(2, 4)
        
        for policy_num in range(num_policies):
            # Genera dati della polizza
            policy_age_days = random.randint(0, 1095)  # Ultimi 3 anni
            start_date = datetime.now() - timedelta(days=policy_age_days)
            end_date = start_date + timedelta(days=365)
            
            # Determina lo stato della polizza
            if end_date > datetime.now():
                status = "active"
            else:
                status = random.choices(["expired", "cancelled"], weights=[0.8, 0.2])[0]
            
            policy_number = f"POL{start_date.year}{random.randint(10000, 99999)}"
            company = f"Compagnia {random.choice(['Alfa', 'Beta', 'Gamma', 'Delta', 'Epsilon'])}"
            
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
            """, (risk_id, client_id, company, policy_number, start_date.date(), end_date.date(), status))
            policy_id = cursor.lastrowid
            
            # Genera premi per la polizza (mensili)
            premium_base = random.uniform(*risk_info["premium_range"])
            for month in range(12):
                payment_date = start_date + timedelta(days=30*month)
                if payment_date > datetime.now():
                    break
                    
                # Variazione del 10% sul premio base
                amount = premium_base * random.uniform(0.9, 1.1)
                due_date = payment_date + timedelta(days=30)
                
                # Determina lo stato del pagamento
                if payment_date <= datetime.now():
                    payment_status = random.choices(["paid", "pending", "overdue"], weights=[0.85, 0.1, 0.05])[0]
                else:
                    payment_status = "pending"
                
                payment_date_db = payment_date.date() if payment_status == "paid" else None
                
                cursor.execute("""
                    INSERT INTO premiums (policy_id, amount, due_date, payment_status, payment_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (policy_id, amount, due_date.date(), payment_status, payment_date_db))
            
            # Genera sinistri occasionali
            if random.random() < risk_info["claim_probability"]:
                # Sinistri avvengono dopo 60 giorni dall'inizio della polizza
                claim_min_date = start_date + timedelta(days=60)
                if claim_min_date < datetime.now():
                    claim_date = claim_min_date + timedelta(days=random.randint(0, (end_date - claim_min_date).days))
                    if claim_date <= datetime.now():
                        claim_amount = random.uniform(*risk_info["claim_range"])
                        claim_status = random.choices(["open", "in_review", "approved", "rejected"], weights=[0.05, 0.15, 0.7, 0.1])[0]
                        description = f"Sinistro {risk_type} - Settore {sector}"
                        
                        cursor.execute("""
                            INSERT INTO claims (policy_id, claim_date, amount, status, description)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (policy_id, claim_date.date(), claim_amount, claim_status, description))
    
    conn.commit()
    conn.close()
    print("Dati di polizze, sinistri e premi generati con successo!")

if __name__ == "__main__":
    populate_policies_claims_premiums()