#!/usr/bin/env python3
"""
Script per popolare il database con dati di test coerenti
Include clienti, rischi, polizze, sinistri, premi, sottoscrittori e delegati
"""
import sys
import os
import random
import json
from datetime import datetime, date, timedelta
from decimal import Decimal

# Aggiungi il path per i moduli locali
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from modules.db import (
    create_client, create_risk, create_policy, create_claim, 
    create_premium, create_policy_subscriber, create_premium_delegate
)

def generate_fake_data():
    """Genera dati finti per il popolamento del database"""
    
    # Nomi e cognomi italiani
    first_names = [
        "Marco", "Luca", "Giulia", "Sofia", "Alessandro", "Francesca", 
        "Matteo", "Chiara", "Andrea", "Valentina", "Simone", "Elena",
        "Davide", "Martina", "Federico", "Alessia", "Roberto", "Elisa",
        "Stefano", "Alice", "Paolo", "Silvia", "Luigi", "Giorgia",
        "Antonio", "Laura", "Giovanni", "Michela", "Pietro", "Roberta"
    ]
    
    last_names = [
        "Rossi", "Bianchi", "Verdi", "Russo", "Ferrari", "Esposito",
        "Romano", "Ricci", "Marino", "Greco", "Bruno", "Gallo",
        "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo",
        "Lombardi", "Moretti", "Santoro", "Barbieri", "Villa", "Colombo",
        "Fontana", "Leonardi", "Marchetti", "Rinaldi", "Caruso", "Ferrara"
    ]
    
    # Nomi aziende
    company_names = [
        "Studio Legale Associato", "ConsulTech SRL", "Edilizia Moderna SPA",
        "Trasporti Veloci SRL", "Medical Care SRL", "Ingegneria Italia",
        "Commercial Solutions", "Logistica Express", "Noleggio Pro",
        "Architects Studio", "Engineering Plus", "Legal Solutions",
        "Health Services", "Transport Group", "Construction Co",
        "Tech Solutions", "Business Consulting", "Medical Group",
        "Logistics Pro", "Rental Services", "Legal Partners",
        "Engineering Works", "Healthcare Plus", "Transport Solutions",
        "Building Experts", "Tech Group", "Business Solutions",
        "Medical Experts", "Logistics Group", "Rental Pro"
    ]
    
    # Settori
    sectors = [
        "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria",
        "Commercio", "Logistica", "Noleggio", "Assicurativo"
    ]
    
    # Tipi di rischio
    risk_types = [
        "Flotta Auto", "RC Professionale", "Fabbricato", 
        "Rischi Tecnici", "Cyber Security", "Infortuni", "Altro"
    ]
    
    # Compagnie assicurative
    insurance_companies = [
        "Allianz Italia S.p.A.", "Generali Italia S.p.A.", "UnipolSai Assicurazioni",
        "AXA XL Italia", "Chubb European Group", "Zurich Italia",
        "Aon Insurance", "Willis Towers Watson", "Marsh Italia",
        "Lockton Companies"
    ]
    
    # Città italiane
    cities = [
        "Milano", "Roma", "Napoli", "Torino", "Palermo", "Genova",
        "Bologna", "Firenze", "Bari", "Catania", "Venezia", "Verona",
        "Messina", "Padova", "Trieste", "Taranto", "Brescia", "Parma",
        "Prato", "Modena", "Reggio Calabria", "Reggio Emilia", "Perugia",
        "Livorno", "Ravenna", "Cagliari", "Foggia", "Rimini", "Salerno",
        "Ferrara"
    ]
    
    return {
        "first_names": first_names,
        "last_names": last_names,
        "company_names": company_names,
        "sectors": sectors,
        "risk_types": risk_types,
        "insurance_companies": insurance_companies,
        "cities": cities
    }

def create_test_clients(fake_data, count=30):
    """Crea clienti di test"""
    print("Creazione clienti...")
    clients = []
    
    for i in range(count):
        is_company = random.choice([True, False])
        
        if is_company:
            # Cliente aziendale
            client_type = random.choice(["company", "freelance"])
            name = f"{random.choice(fake_data['first_names'])} {random.choice(fake_data['last_names'])}"
            company = random.choice(fake_data['company_names']) + f" {i+1}"
            fiscal_code = f"FC{i:03d}{random.randint(10000000, 99999999)}F"  # 16 caratteri max
            vat_number = f"{random.randint(10000000000, 99999999999)}"
            birth_date = None
            establishment_date = (date.today() - timedelta(days=random.randint(365, 7300))).isoformat()
        else:
            # Cliente privato
            client_type = "individual"
            name = f"{random.choice(fake_data['first_names'])} {random.choice(fake_data['last_names'])}"
            company = ""
            fiscal_code = f"CF{i:03d}{random.randint(10000000, 99999999)}P"  # 16 caratteri max
            vat_number = ""
            birth_date = (date.today() - timedelta(days=random.randint(6570, 25550))).isoformat()
            establishment_date = None
        
        client_data = {
            "name": name,
            "company": company,
            "client_type": client_type,
            "email": f"cliente{i+1}@{'azienda' if is_company else 'privato'}.it",
            "phone": f"0{random.randint(100, 999)}{random.randint(1000000, 9999999)}",
            "mobile": f"3{random.randint(100000000, 999999999)}",
            "fax": f"0{random.randint(100, 999)}{random.randint(1000000, 9999999)}" if random.choice([True, False]) else None,
            "address": f"Via {random.choice(['Roma', 'Milano', 'Napoli', 'Torino'])}, {random.randint(1, 200)}",
            "city": random.choice(fake_data['cities']),
            "province": random.choice(["MI", "RM", "NA", "TO", "BG", "VE", "FI", "BO", "PA", "GE"]),
            "postal_code": f"{random.randint(10000, 99999)}",
            "country": "Italy",
            "fiscal_code": fiscal_code,
            "vat_number": vat_number,
            "tax_regime": "Ordinario" if is_company else "PF",
            "sdi_code": f"{random.choice(['ABC', 'XYZ', 'DEF'])}{random.randint(100, 999)}",
            "pec_email": f"pec{i+1}@{'azienda' if is_company else 'privato'}.pec.it" if random.choice([True, False]) else None,
            "legal_form": random.choice(["SRL", "SPA", "SNC", "SAS"]) if is_company else None,
            "company_registration_number": f"REG{i:05d}" if is_company else None,
            "rea_office": random.choice(["RM", "MI", "NA", "TO"]) if is_company else None,
            "rea_number": f"REA{i:05d}" if is_company else None,
            "share_capital": float(random.randint(10000, 1000000)) if is_company else 0.0,
            "vat_settlement": random.choice(["monthly", "quarterly", "annual"]),
            "iban": f"IT{random.randint(10, 99)}{random.choice(['ABI', 'XYZ', 'DEF'])}{random.randint(1000000000000000000000, 9999999999999999999999)}",
            "bank_name": random.choice(["Intesa Sanpaolo", "UniCredit", "BNL", "Banco BPM", "Credem"]),
            "bank_iban": f"IT{random.randint(10, 99)}{random.choice(['BAN', 'KIA', 'BKO'])}{random.randint(1000000000000000000000, 9999999999999999999999)}" if random.choice([True, False]) else None,
            "sector": random.choice(fake_data['sectors']),
            "customer_segment": random.choice(["premium", "standard", "basic"]),
            "customer_status": random.choice(["active", "inactive", "prospect"]),
            "referred_by": random.choice(["Sito Web", "Referenza", "Pubblicità", "Evento", "Altro"]),
            "birth_date": birth_date,
            "birth_place": random.choice(fake_data['cities']) if not is_company else None,
            "establishment_date": establishment_date,
            "notes": f"Cliente di test numero {i+1}",
            "preferred_communication": random.choice(["email", "phone", "mail", "pec"]),
            "language": "it"
        }
        
        try:
            client_id = create_client(client_data)
            client_data['id'] = client_id
            clients.append(client_data)
            print(f"  Cliente {i+1}/{count}: {name} ({'Azienda' if is_company else 'Privato'}) - ID: {client_id}")
        except Exception as e:
            print(f"  Errore creazione cliente {i+1}: {str(e)}")
    
    return clients

def create_insurance_companies(fake_data, count=10):
    """Crea compagnie assicurative"""
    print("Creazione compagnie assicurative...")
    companies = []
    
    for i in range(count):
        company_data = {
            "name": fake_data['insurance_companies'][i] if i < len(fake_data['insurance_companies']) else f"Compagnia {i+1}",
            "company": fake_data['insurance_companies'][i] if i < len(fake_data['insurance_companies']) else f"Compagnia {i+1}",
            "client_type": "company",
            "email": f"info@compagnia{i+1}.it",
            "phone": f"0{random.randint(100, 999)}{random.randint(1000000, 9999999)}",
            "mobile": f"3{random.randint(100000000, 999999999)}",
            "address": f"Via Assicurazioni, {random.randint(1, 100)}",
            "city": random.choice(fake_data['cities']),
            "province": random.choice(["MI", "RM", "NA", "TO"]),
            "postal_code": f"{random.randint(10000, 99999)}",
            "country": "Italy",
            "fiscal_code": f"FC{i:03d}{random.randint(10000000, 99999999)}C",  # 16 caratteri max
            "vat_number": f"{random.randint(10000000000, 99999999999)}",
            "sector": "Assicurativo",
            "customer_status": "active"
        }
        
        try:
            company_id = create_client(company_data)
            company_data['id'] = company_id
            companies.append(company_data)
            print(f"  Compagnia {i+1}/{count}: {company_data['company']} - ID: {company_id}")
        except Exception as e:
            print(f"  Errore creazione compagnia {i+1}: {str(e)}")
    
    return companies

def create_risks_for_clients(clients, fake_data, risks_per_client=2):
    """Crea rischi per i clienti"""
    print("Creazione rischi per clienti...")
    risks = []
    risk_id_counter = 1
    
    for client in clients:
        for i in range(risks_per_client):
            risk_data = {
                "client_id": client['id'],
                "broker_id": None,  # Può essere impostato in futuro
                "risk_type": random.choice(fake_data['risk_types']),
                "details": json.dumps({
                    "description": f"Rischio {i+1} per {client['name']}",
                    "coverage_limit": float(random.randint(100000, 1000000)),
                    "deductible": float(random.randint(500, 5000))
                })
            }
            
            try:
                risk_id = create_risk(risk_data)
                risk_data['id'] = risk_id
                risks.append(risk_data)
                print(f"  Rischio {risk_id_counter}: {risk_data['risk_type']} per cliente {client['name']} - ID: {risk_id}")
                risk_id_counter += 1
            except Exception as e:
                print(f"  Errore creazione rischio: {str(e)}")
    
    return risks

def create_policies_for_risks(risks, insurance_companies, fake_data, policies_per_risk=1):
    """Crea polizze per i rischi"""
    print("Creazione polizze per rischi...")
    policies = []
    policy_id_counter = 1
    
    for risk in risks:
        for i in range(policies_per_risk):
            # Seleziona una compagnia assicurativa casuale
            insurance_company = random.choice(insurance_companies)
            
            # Genera date coerenti
            start_date = date.today() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=365)
            subscription_date = start_date - timedelta(days=random.randint(1, 30))
            
            policy_data = {
                "risk_id": risk['id'],
                "company_id": insurance_company['id'],
                "company": insurance_company['company'],
                "policy_number": f"POL{random.randint(100000, 999999)}{i+1}",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "status": random.choice(["active", "expired", "cancelled", "pending"]),
                "subscription_date": subscription_date.isoformat(),
                "subscription_method": random.choice(["digital", "paper", "agent"]),
                "premium_amount": float(random.randint(1000, 10000)),
                "premium_frequency": random.choice(["annual", "semiannual", "quarterly", "monthly"]),
                "payment_method": random.choice(["direct_debit", "bank_transfer", "credit_card", "cash", "check"]),
                "primary_subscriber_id": None,  # Sarà impostato dopo
                "premium_delegate_id": None     # Sarà impostato dopo
            }
            
            try:
                policy_id = create_policy(policy_data)
                policy_data['id'] = policy_id
                policies.append(policy_data)
                print(f"  Polizza {policy_id_counter}: {policy_data['policy_number']} - ID: {policy_id}")
                policy_id_counter += 1
            except Exception as e:
                print(f"  Errore creazione polizza: {str(e)}")
    
    return policies

def create_subscribers_for_policies(policies, clients):
    """Crea sottoscrittori per le polizze"""
    print("Creazione sottoscrittori per polizze...")
    subscribers = []
    
    for i, policy in enumerate(policies):
        # Seleziona un cliente casuale come sottoscrittore
        client = random.choice(clients)
        
        # Determina il tipo di entità
        entity_type = client['client_type']
        
        if entity_type == 'individual':
            subscriber_data = {
                "policy_id": policy['id'],
                "subscriber_type": "primary",
                "entity_type": entity_type,
                "first_name": client['name'].split()[0] if client['name'] else "",
                "last_name": " ".join(client['name'].split()[1:]) if len(client['name'].split()) > 1 else "",
                "fiscal_code": client['fiscal_code'],
                "birth_date": client['birth_date'],
                "birth_place": client['birth_place'],
                "company_name": None,
                "vat_number": None,
                "legal_form": None,
                "email": client['email'],
                "phone": client['phone'],
                "mobile": client['mobile'],
                "address": client['address'],
                "city": client['city'],
                "province": client['province'],
                "postal_code": client['postal_code'],
                "country": client['country']
            }
        else:
            subscriber_data = {
                "policy_id": policy['id'],
                "subscriber_type": "primary",
                "entity_type": entity_type,
                "first_name": None,
                "last_name": None,
                "fiscal_code": client['fiscal_code'],
                "birth_date": None,
                "birth_place": None,
                "company_name": client['company'],
                "vat_number": client['vat_number'],
                "legal_form": client['legal_form'],
                "email": client['email'],
                "phone": client['phone'],
                "mobile": client['mobile'],
                "address": client['address'],
                "city": client['city'],
                "province": client['province'],
                "postal_code": client['postal_code'],
                "country": client['country']
            }
        
        try:
            subscriber_id = create_policy_subscriber(subscriber_data)
            subscriber_data['id'] = subscriber_id
            subscribers.append(subscriber_data)
            print(f"  Sottoscrittore {i+1}: {client['name']} per polizza {policy['policy_number']} - ID: {subscriber_id}")
        except Exception as e:
            print(f"  Errore creazione sottoscrittore: {str(e)}")
    
    return subscribers

def create_delegates_for_clients(clients):
    """Crea delegati al pagamento per i clienti"""
    print("Creazione delegati al pagamento per clienti...")
    delegates = []
    
    # Solo per alcuni clienti (i primi 15)
    clients_subset = clients[:15] if len(clients) > 15 else clients
    
    for i, client in enumerate(clients_subset):
        delegate_type = random.choice(["individual", "company"])
        
        if delegate_type == "individual":
            delegate_data = {
                "client_id": client['id'],
                "delegate_type": delegate_type,
                "first_name": f"Delegato{i+1}",
                "last_name": f"Cognome{i+1}",
                "fiscal_code": f"DF{i:03d}{random.randint(10000000, 99999999)}D",
                "company_name": None,
                "vat_number": None,
                "email": f"delegato{i+1}@azienda.it",
                "phone": f"0{random.randint(100, 999)}{random.randint(1000000, 9999999)}",
                "mobile": f"3{random.randint(100000000, 999999999)}",
                "address": f"Via Delegati, {random.randint(1, 50)}",
                "city": client['city'],
                "province": client['province'],
                "postal_code": client['postal_code'],
                "country": client['country'],
                "authorization_level": random.choice(["full", "limited", "specific_policy"]),
                "authorization_start": (date.today() - timedelta(days=30)).isoformat(),
                "authorization_end": (date.today() + timedelta(days=335)).isoformat(),
                "is_active": True
            }
        else:
            delegate_data = {
                "client_id": client['id'],
                "delegate_type": delegate_type,
                "first_name": None,
                "last_name": None,
                "fiscal_code": None,
                "company_name": f"Azienda Delegata {i+1}",
                "vat_number": f"{random.randint(10000000000, 99999999999)}",
                "email": f"delegato{i+1}@azienda.it",
                "phone": f"0{random.randint(100, 999)}{random.randint(1000000, 9999999)}",
                "mobile": f"3{random.randint(100000000, 999999999)}",
                "address": f"Via Delegati, {random.randint(1, 50)}",
                "city": client['city'],
                "province": client['province'],
                "postal_code": client['postal_code'],
                "country": client['country'],
                "authorization_level": random.choice(["full", "limited", "specific_policy"]),
                "authorization_start": (date.today() - timedelta(days=30)).isoformat(),
                "authorization_end": (date.today() + timedelta(days=335)).isoformat(),
                "is_active": True
            }
        
        try:
            delegate_id = create_premium_delegate(delegate_data)
            delegate_data['id'] = delegate_id
            delegates.append(delegate_data)
            print(f"  Delegato {i+1}: {delegate_data['first_name'] or delegate_data['company_name']} per cliente {client['name']} - ID: {delegate_id}")
        except Exception as e:
            print(f"  Errore creazione delegato: {str(e)}")
    
    return delegates

def create_claims_for_policies(policies, claims_per_policy=1):
    """Crea sinistri per le polizze"""
    print("Creazione sinistri per polizze...")
    claims = []
    claim_id_counter = 1
    
    # Seleziona solo alcune polizze per creare sinistri
    policies_with_claims = random.sample(policies, min(len(policies), 15)) if policies else []
    
    for policy in policies_with_claims:
        for i in range(claims_per_policy):
            # Genera una data di sinistro coerente con la polizza
            policy_start = datetime.fromisoformat(policy['start_date']).date()
            policy_end = datetime.fromisoformat(policy['end_date']).date()
            
            # Genera una data casuale tra inizio e fine polizza
            days_diff = (policy_end - policy_start).days
            claim_date = policy_start + timedelta(days=random.randint(0, days_diff))
            
            claim_data = {
                "policy_id": policy['id'],
                "claim_date": claim_date.isoformat(),
                "amount": float(random.randint(1000, 15000)),
                "status": random.choice(["open", "in_review", "approved", "rejected"]),
                "description": random.choice([
                    "Danno verificato a causa di evento coperto",
                    "Incidente stradale con danni al veicolo",
                    "Furto con scasso dell'abitazione",
                    "Infortunio sul lavoro",
                    "Danno causato da evento naturale",
                    "Responsabilità civile verso terzi"
                ])
            }
            
            try:
                claim_id = create_claim(claim_data)
                claim_data['id'] = claim_id
                claims.append(claim_data)
                print(f"  Sinistro {claim_id_counter}: €{claim_data['amount']:,.2f} per polizza {policy['policy_number']} - ID: {claim_id}")
                claim_id_counter += 1
            except Exception as e:
                print(f"  Errore creazione sinistro: {str(e)}")
    
    return claims

def create_premiums_for_policies(policies):
    """Crea premi per le polizze"""
    print("Creazione premi per polizze...")
    premiums = []
    premium_id_counter = 1
    
    for policy in policies:
        # Crea un premio per ogni polizza
        policy_start = datetime.fromisoformat(policy['start_date']).date()
        
        premium_data = {
            "policy_id": policy['id'],
            "amount": policy['premium_amount'] or float(random.randint(1000, 10000)),
            "due_date": (policy_start + timedelta(days=30)).isoformat(),  # 30 giorni dopo l'inizio
            "payment_status": random.choice(["pending", "paid", "overdue"]),
            "payment_date": None  # Sarà impostata per i premi pagati
        }
        
        # Se il premio è pagato, imposta la data di pagamento
        if premium_data['payment_status'] == 'paid':
            premium_data['payment_date'] = (policy_start + timedelta(days=random.randint(1, 30))).isoformat()
        
        try:
            premium_id = create_premium(premium_data)
            premium_data['id'] = premium_id
            premiums.append(premium_data)
            print(f"  Premio {premium_id_counter}: €{premium_data['amount']:,.2f} per polizza {policy['policy_number']} - ID: {premium_id}")
            premium_id_counter += 1
        except Exception as e:
            print(f"  Errore creazione premio: {str(e)}")
    
    return premiums

def main():
    """Funzione principale per popolare il database"""
    print("=" * 60)
    print("POPOLAMENTO DATABASE - BrokerFlow AI")
    print("=" * 60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Genera dati finti
        fake_data = generate_fake_data()
        
        # 1. Crea clienti (20 clienti)
        clients = create_test_clients(fake_data, count=20)
        print(f"\n✅ Creati {len(clients)} clienti")
        
        # Verifica che ci siano clienti creati
        if len(clients) == 0:
            print("\n❌ Nessun cliente creato. Impossibile continuare.")
            return False
            
        # 2. Crea compagnie assicurative (10 compagnie)
        insurance_companies = create_insurance_companies(fake_data, count=10)
        print(f"✅ Create {len(insurance_companies)} compagnie assicurative")
        
        # 3. Crea rischi per i clienti (2 rischi per cliente)
        risks = create_risks_for_clients(clients, fake_data, risks_per_client=2)
        print(f"✅ Creati {len(risks)} rischi")
        
        # 4. Crea polizze per i rischi (1 polizza per rischio)
        policies = create_policies_for_risks(risks, insurance_companies, fake_data, policies_per_risk=1)
        print(f"✅ Create {len(policies)} polizze")
        
        # 5. Crea sottoscrittori per le polizze
        subscribers = create_subscribers_for_policies(policies, clients)
        print(f"✅ Creati {len(subscribers)} sottoscrittori")
        
        # 6. Crea delegati al pagamento per i clienti
        delegates = create_delegates_for_clients(clients)
        print(f"✅ Creati {len(delegates)} delegati al pagamento")
        
        # 7. Crea sinistri per le polizze
        claims = create_claims_for_policies(policies, claims_per_policy=1)
        print(f"✅ Creati {len(claims)} sinistri")
        
        # 8. Crea premi per le polizze
        premiums = create_premiums_for_policies(policies)
        print(f"✅ Creati {len(premiums)} premi")
        
        print("\n" + "=" * 60)
        print("RIEPILOGO DATI CREATI:")
        print("=" * 60)
        print(f"👥 Clienti: {len(clients)}")
        print(f"🏢 Compagnie Assicurative: {len(insurance_companies)}")
        print(f"⚠️  Rischi: {len(risks)}")
        print(f"📜 Polizze: {len(policies)}")
        print(f"✍️  Sottoscrittori: {len(subscribers)}")
        print(f"💳 Delegati Pagamento: {len(delegates)}")
        print(f"🚨 Sinistri: {len(claims)}")
        print(f"💰 Premi: {len(premiums)}")
        print("\n🎉 Popolamento database completato con successo!")
        
        # Statistiche aggiuntive (solo se ci sono dati)
        if len(policies) > 0:
            active_policies = len([p for p in policies if p.get('status') == 'active'])
            expired_policies = len([p for p in policies if p.get('status') == 'expired'])
            print(f"\n📊 STATISTICHE:")
            print(f"   Polizze Attive: {active_policies}")
            print(f"   Polizze Scadute: {expired_policies}")
        
        if len(premiums) > 0:
            total_premium_amount = sum([p.get('amount', 0) for p in premiums])
            print(f"   Totale Premi: €{total_premium_amount:,.2f}")
        
        if len(claims) > 0:
            total_claim_amount = sum([c.get('amount', 0) for c in claims])
            print(f"   Totale Sinistri: €{total_claim_amount:,.2f}")
        
        # Solo se ci sono sia premi che sinistri e il totale premi è maggiore di zero
        if len(premiums) > 0 and len(claims) > 0:
            total_premium_amount = sum([p.get('amount', 0) for p in premiums])
            total_claim_amount = sum([c.get('amount', 0) for c in claims])
            if total_premium_amount > 0:
                ratio = total_claim_amount / total_premium_amount * 100
                print(f"   Rapporto Sinistri/Premi: {ratio:.1f}%")
        
    except Exception as e:
        print(f"\n❌ Errore durante il popolamento del database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()