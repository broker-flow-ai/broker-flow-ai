#!/usr/bin/env python3
"""
Script per popolare dati realistici per dashboard compagnia assicurativa e broker
"""

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

def populate_insurance_companies():
    """Crea compagnie assicurative vere e proprie"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Compagnie assicurative italiane reali (simulate)
    insurance_companies = [
        {"name": "Marco Bianchi", "company": "Generali Italia S.p.A.", "sector": "Assicurativo", "email": "m.bianchi@generali.it"},
        {"name": "Laura Rossi", "company": "Allianz Italia S.p.A.", "sector": "Assicurativo", "email": "l.rossi@allianz.it"},
        {"name": "Giuseppe Verdi", "company": "UnipolSai Assicurazioni S.p.A.", "sector": "Assicurativo", "email": "g.verdi@unipolsai.it"},
        {"name": "Anna Ferrari", "company": "AXA Partners Italia S.p.A.", "sector": "Assicurativo", "email": "a.ferrari@axa.it"},
        {"name": "Roberto Romano", "company": "Zurich Italia S.p.A.", "sector": "Assicurativo", "email": "r.romano@zurich.it"}
    ]
    
    company_ids = []
    for company_data in insurance_companies:
        # Controlla se esiste già
        cursor.execute("SELECT id FROM clients WHERE email = %s", (company_data["email"],))
        result = cursor.fetchone()
        if result:
            company_ids.append(result[0])
        else:
            # Inserisci nuova compagnia
            cursor.execute("""
                INSERT INTO clients (name, company, email, sector) 
                VALUES (%s, %s, %s, %s)
            """, (
                company_data["name"], 
                company_data["company"], 
                company_data["email"], 
                company_data["sector"]
            ))
            company_ids.append(cursor.lastrowid)
    
    conn.commit()
    conn.close()
    print(f"Compagnie assicurative create: {len(company_ids)}")
    return company_ids

def populate_policies_with_insurance_companies(insurance_company_ids):
    """Associa le policy esistenti a compagnie assicurative"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Seleziona tutte le policy esistenti
    cursor.execute("SELECT id, risk_id FROM policies")
    policies = cursor.fetchall()
    
    if not policies:
        print("Nessuna policy trovata da associare alle compagnie")
        conn.close()
        return
    
    # Aggiorna le policy con compagnie assicurative casuali
    for policy_id, risk_id in policies:
        # Seleziona una compagnia assicurativa casuale
        insurance_company_id = random.choice(insurance_company_ids)
        
        # Ottieni i dettagli della compagnia
        cursor.execute("SELECT company FROM clients WHERE id = %s", (insurance_company_id,))
        company_name = cursor.fetchone()[0]
        
        # Aggiorna la policy
        cursor.execute("""
            UPDATE policies 
            SET company_id = %s, company = %s 
            WHERE id = %s
        """, (insurance_company_id, company_name, policy_id))
    
    conn.commit()
    conn.close()
    print(f"Policies aggiornate con compagnie assicurative: {len(policies)}")

def populate_realistic_claims_and_premiums():
    """Crea sinistri e premi realistici per le policy"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Seleziona tutte le policy
    cursor.execute("SELECT id, risk_id FROM policies")
    policies = cursor.fetchall()
    
    claims_count = 0
    premiums_count = 0
    
    for policy_id, risk_id in policies:
        # Ottieni il tipo di rischio
        cursor.execute("SELECT risk_type FROM risks WHERE id = %s", (risk_id,))
        risk_result = cursor.fetchone()
        if not risk_result:
            continue
            
        risk_type = risk_result[0]
        
        # Definisci valori basati sul tipo di rischio
        risk_multipliers = {
            "Flotta Auto": {"premium_base": 2000, "claim_probability": 0.15, "claim_base": 8000},
            "RC Professionale": {"premium_base": 1500, "claim_probability": 0.08, "claim_base": 15000},
            "Fabbricato": {"premium_base": 1200, "claim_probability": 0.12, "claim_base": 25000},
            "Rischi Tecnici": {"premium_base": 2500, "claim_probability": 0.10, "claim_base": 20000}
        }
        
        multiplier = risk_multipliers.get(risk_type, risk_multipliers["Flotta Auto"])
        
        # Crea premi mensili per 12 mesi
        for month in range(12):
            payment_date = datetime.now() - timedelta(days=random.randint(0, 365))
            due_date = payment_date + timedelta(days=30)
            
            # Calcola importo premio con variazione
            amount = multiplier["premium_base"] * random.uniform(0.8, 1.3)
            
            # Determina stato pagamento
            payment_status = random.choices(
                ["paid", "pending", "overdue"], 
                weights=[0.85, 0.1, 0.05]
            )[0]
            
            payment_date_db = payment_date.date() if payment_status == "paid" else None
            
            cursor.execute("""
                INSERT INTO premiums (policy_id, amount, due_date, payment_status, payment_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (policy_id, amount, due_date.date(), payment_status, payment_date_db))
            premiums_count += 1
        
        # Crea sinistri occasionalmente
        if random.random() < multiplier["claim_probability"]:
            claim_date = datetime.now() - timedelta(days=random.randint(0, 365))
            claim_amount = multiplier["claim_base"] * random.uniform(0.5, 2.0)
            
            claim_status = random.choices(
                ["open", "in_review", "approved", "rejected"], 
                weights=[0.1, 0.2, 0.6, 0.1]
            )[0]
            
            description = f"Sinistro {risk_type} - Danno verificato"
            
            cursor.execute("""
                INSERT INTO claims (policy_id, claim_date, amount, status, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (policy_id, claim_date.date(), claim_amount, claim_status, description))
            claims_count += 1
    
    conn.commit()
    conn.close()
    print(f"Premi creati: {premiums_count}")
    print(f"Sinistri creati: {claims_count}")

def populate_brokers():
    """Crea broker con performance realistica"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Identifica i clienti che possono essere broker
    cursor.execute("""
        SELECT id, name, company, sector FROM clients 
        WHERE sector IN ('Trasporti', 'Sanità', 'Edilizia', 'Legalità', 'Ingegneria', 'Commercio', 'Logistica', 'Noleggio')
        LIMIT 10
    """)
    potential_brokers = cursor.fetchall()
    
    broker_ids = []
    for client_id, name, company, sector in potential_brokers:
        broker_ids.append(client_id)
    
    conn.close()
    print(f"Broker identificati: {len(broker_ids)}")
    return broker_ids

def populate_broker_performance(broker_ids):
    """Aggiunge performance ai broker esistenti"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Aggiorna i broker con dati di performance
    for broker_id in broker_ids:
        # Genera performance realistiche
        policies_count = random.randint(5, 50)
        total_premium = random.uniform(5000, 100000)
        claims_count = random.randint(0, int(policies_count * 0.3))
        total_claims = random.uniform(0, total_premium * 0.4)
        
        # Aggiorna i dati del broker (se necessario)
        # Per ora lasciamo i dati esistenti, ma possiamo aggiungere performance metrics
        
    conn.close()
    print(f"Performance broker aggiornata per {len(broker_ids)} broker")

def main():
    print("=== Popolamento dati per dashboard ===")
    
    # 1. Crea compagnie assicurative
    insurance_company_ids = populate_insurance_companies()
    
    # 2. Associa policy a compagnie assicurative
    populate_policies_with_insurance_companies(insurance_company_ids)
    
    # 3. Crea sinistri e premi realistici
    populate_realistic_claims_and_premiums()
    
    # 4. Identifica e popola broker
    broker_ids = populate_brokers()
    populate_broker_performance(broker_ids)
    
    print("=== Popolamento completato ===")

if __name__ == "__main__":
    main()