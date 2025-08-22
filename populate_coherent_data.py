#!/usr/bin/env python3
"""
Script per popolare dati coerenti per dashboard compagnia assicurativa e broker
"""

import mysql.connector
import random
from datetime import datetime, timedelta
import os

# Configurazione database
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
MYSQL_USER = os.environ.get('MYSQL_USER', 'brokerflow')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'brokerflow123')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'brokerflow_ai')

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def create_insurance_companies():
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
            print(f"Inserita compagnia: {company_data['company']}")
    
    conn.commit()
    conn.close()
    print(f"Compagnie assicurative create/aggiornate: {len(company_ids)}")
    return company_ids

def assign_policies_to_insurance_companies(insurance_company_ids):
    """Associa le policy esistenti a compagnie assicurative"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Seleziona tutte le policy esistenti senza compagnia
    cursor.execute("SELECT id FROM policies WHERE company_id IS NULL")
    policies = cursor.fetchall()
    
    if not policies:
        print("Nessuna policy da associare alle compagnie")
        conn.close()
        return 0
    
    # Aggiorna le policy con compagnie assicurative casuali
    updated_count = 0
    for (policy_id,) in policies:
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
        updated_count += 1
    
    conn.commit()
    conn.close()
    print(f"Policies associate a compagnie assicurative: {updated_count}")
    return updated_count

def create_realistic_premiums_and_claims():
    """Crea premi e sinistri realistici per tutte le policy"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Seleziona tutte le policy
    cursor.execute("""
        SELECT p.id, p.risk_id, r.risk_type 
        FROM policies p 
        JOIN risks r ON p.risk_id = r.id
    """)
    policies = cursor.fetchall()
    
    premiums_count = 0
    claims_count = 0
    
    for policy_id, risk_id, risk_type in policies:
        # Definisci valori basati sul tipo di rischio
        risk_profiles = {
            "Flotta Auto": {"premium_base": 2000, "claim_probability": 0.15, "claim_base": 8000},
            "RC Professionale": {"premium_base": 1500, "claim_probability": 0.08, "claim_base": 15000},
            "Fabbricato": {"premium_base": 1200, "claim_probability": 0.12, "claim_base": 25000},
            "Rischi Tecnici": {"premium_base": 2500, "claim_probability": 0.10, "claim_base": 20000}
        }
        
        profile = risk_profiles.get(risk_type, risk_profiles["Flotta Auto"])
        
        # Crea 12 premi mensili per 12 mesi
        for month in range(12):
            # Data pagamento casuale nell'ultimo anno
            days_back = random.randint(0, 365)
            payment_date = datetime.now() - timedelta(days=days_back)
            due_date = payment_date + timedelta(days=30)
            
            # Importo premio con variazione casuale
            amount = profile["premium_base"] * random.uniform(0.8, 1.3)
            
            # Stato pagamento (85% pagati, 10% pending, 5% overdue)
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
        if random.random() < profile["claim_probability"]:
            # Data sinistro casuale
            days_back = random.randint(0, 365)
            claim_date = datetime.now() - timedelta(days=days_back)
            claim_amount = profile["claim_base"] * random.uniform(0.5, 2.0)
            
            # Stato sinistro
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
    return premiums_count, claims_count

def update_broker_metrics():
    """Aggiorna le metriche dei broker esistenti"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Seleziona i clienti che possono essere broker
    cursor.execute("""
        SELECT DISTINCT c.id, c.name, c.company, c.sector
        FROM clients c
        JOIN risks r ON c.id = r.client_id
        JOIN policies p ON r.id = p.risk_id
        WHERE c.sector IN ('Trasporti', 'Sanità', 'Edilizia', 'Legalità', 'Ingegneria', 'Commercio', 'Logistica', 'Noleggio')
    """)
    brokers = cursor.fetchall()
    
    updated_brokers = 0
    for broker_id, name, company, sector in brokers:
        # Calcola metriche realistiche per ogni broker
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT p.id) as policies_count,
                SUM(pr.amount) as total_premium,
                COUNT(cl.id) as claims_count,
                SUM(cl.amount) as total_claims
            FROM risks r
            JOIN policies p ON r.id = p.risk_id
            LEFT JOIN premiums pr ON p.id = pr.policy_id AND pr.payment_status = 'paid'
            LEFT JOIN claims cl ON p.id = cl.policy_id
            WHERE r.client_id = %s
        """, (broker_id,))
        
        metrics = cursor.fetchone()
        policies_count = metrics[0] or 0
        total_premium = metrics[1] or 0
        claims_count = metrics[2] or 0
        total_claims = metrics[3] or 0
        
        # Non dobbiamo aggiornare nulla nella tabella clients, 
        # ma possiamo confermare che i dati sono stati calcolati
        print(f"Broker {name} ({company}): {policies_count} polizze, €{total_premium:.2f} premi, {claims_count} sinistri")
        updated_brokers += 1
    
    conn.close()
    print(f"Metriche broker aggiornate per {updated_brokers} broker")
    return updated_brokers

def verify_data_consistency():
    """Verifica la coerenza dei dati"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\\n=== VERIFICA COERENZA DATI ===")
    
    # Verifica compagnie assicurative
    cursor.execute("SELECT COUNT(*) FROM clients WHERE sector = 'Assicurativo'")
    insurance_companies = cursor.fetchone()[0]
    print(f"Compagnie assicurative: {insurance_companies}")
    
    # Verifica policy associate a compagnie
    cursor.execute("SELECT COUNT(*) FROM policies WHERE company_id IS NOT NULL")
    policies_with_company = cursor.fetchone()[0]
    print(f"Policy con compagnia associata: {policies_with_company}")
    
    # Verifica premi
    cursor.execute("SELECT COUNT(*), SUM(amount) FROM premiums")
    premiums_count, premiums_sum = cursor.fetchone()
    print(f"Premi totali: {premiums_count}, Somma: €{premiums_sum or 0:.2f}")
    
    # Verifica sinistri
    cursor.execute("SELECT COUNT(*), SUM(amount) FROM claims")
    claims_count, claims_sum = cursor.fetchone()
    print(f"Sinistri totali: {claims_count}, Somma: €{claims_sum or 0:.2f}")
    
    # Verifica policy attive
    cursor.execute("SELECT COUNT(*) FROM policies WHERE status = 'active'")
    active_policies = cursor.fetchone()[0]
    print(f"Policy attive: {active_policies}")
    
    conn.close()

def main():
    print("=== Popolamento dati coerenti per dashboard ===")
    
    try:
        # 1. Crea/aggiorna compagnie assicurative
        insurance_company_ids = create_insurance_companies()
        
        # 2. Associa policy a compagnie assicurative
        policies_updated = assign_policies_to_insurance_companies(insurance_company_ids)
        
        # 3. Crea premi e sinistri realistici
        premiums_created, claims_created = create_realistic_premiums_and_claims()
        
        # 4. Aggiorna metriche broker
        brokers_updated = update_broker_metrics()
        
        # 5. Verifica coerenza dati
        verify_data_consistency()
        
        print("\\n=== POPOLAMENTO COMPLETATO CON SUCCESSO ===")
        print(f"- Compagnie assicurative: {len(insurance_company_ids)}")
        print(f"- Policy aggiornate: {policies_updated}")
        print(f"- Premi creati: {premiums_created}")
        print(f"- Sinistri creati: {claims_created}")
        print(f"- Broker con metriche: {brokers_updated}")
        
    except Exception as e:
        print(f"\\n=== ERRORE DURANTE IL POPOLAMENTO ===")
        print(f"Errore: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()