import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import json

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise

# Funzioni per clienti
def get_clients(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Recupera la lista dei clienti con filtri opzionali"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM clients WHERE 1=1"
    params = []
    
    if filters:
        if filters.get('name'):
            query += " AND name LIKE %s"
            params.append(f"%{filters['name']}%")
        if filters.get('company'):
            query += " AND company LIKE %s"
            params.append(f"%{filters['company']}%")
        if filters.get('sector'):
            query += " AND sector = %s"
            params.append(filters['sector'])
        if filters.get('email'):
            query += " AND email LIKE %s"
            params.append(f"%{filters['email']}%")
        if filters.get('client_type'):
            query += " AND client_type = %s"
            params.append(filters['client_type'])
        if filters.get('fiscal_code'):
            query += " AND fiscal_code LIKE %s"
            params.append(f"%{filters['fiscal_code']}%")
        if filters.get('vat_number'):
            query += " AND vat_number LIKE %s"
            params.append(f"%{filters['vat_number']}%")
        if filters.get('city'):
            query += " AND city LIKE %s"
            params.append(f"%{filters['city']}%")
        if filters.get('province'):
            query += " AND province = %s"
            params.append(filters['province'])
        if filters.get('customer_status'):
            query += " AND customer_status = %s"
            params.append(filters['customer_status'])
        if filters.get('date_from'):
            query += " AND created_at >= %s"
            params.append(filters['date_from'])
        if filters.get('date_to'):
            query += " AND created_at <= %s"
            params.append(filters['date_to'])
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_client(client_id: int) -> Optional[Dict[str, Any]]:
    """Recupera un cliente specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_client(client_data: Dict[str, Any]) -> int:
    """Crea un nuovo cliente e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO clients (
            name, company, client_type, email, phone, mobile, fax,
            address, city, province, postal_code, country,
            fiscal_code, vat_number, tax_regime, sdi_code, pec_email,
            legal_form, company_registration_number, rea_office, rea_number, 
            share_capital, vat_settlement,
            iban, bank_name, bank_iban,
            sector, customer_segment, customer_status, referred_by,
            birth_date, birth_place, establishment_date,
            notes, preferred_communication, language,
            created_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s
        )
    """
    params = (
        client_data['name'],
        client_data.get('company'),
        client_data.get('client_type', 'individual'),
        client_data.get('email'),
        client_data.get('phone'),
        client_data.get('mobile'),
        client_data.get('fax'),
        client_data.get('address'),
        client_data.get('city'),
        client_data.get('province'),
        client_data.get('postal_code'),
        client_data.get('country', 'Italy'),
        client_data.get('fiscal_code'),
        client_data.get('vat_number'),
        client_data.get('tax_regime'),
        client_data.get('sdi_code'),
        client_data.get('pec_email'),
        client_data.get('legal_form'),
        client_data.get('company_registration_number'),
        client_data.get('rea_office'),
        client_data.get('rea_number'),
        client_data.get('share_capital'),
        client_data.get('vat_settlement'),
        client_data.get('iban'),
        client_data.get('bank_name'),
        client_data.get('bank_iban'),
        client_data.get('sector'),
        client_data.get('customer_segment'),
        client_data.get('customer_status', 'active'),
        client_data.get('referred_by'),
        client_data.get('birth_date'),
        client_data.get('birth_place'),
        client_data.get('establishment_date'),
        client_data.get('notes'),
        client_data.get('preferred_communication'),
        client_data.get('language', 'it'),
        datetime.now()
    )
    
    cursor.execute(query, params)
    client_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return client_id

def update_client(client_id: int, client_data: Dict[str, Any]) -> bool:
    """Aggiorna un cliente esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    # Campi aggiornabili
    updatable_fields = [
        'name', 'company', 'client_type', 'email', 'phone', 'mobile', 'fax',
        'address', 'city', 'province', 'postal_code', 'country',
        'fiscal_code', 'vat_number', 'tax_regime', 'sdi_code', 'pec_email',
        'legal_form', 'company_registration_number', 'rea_office', 'rea_number',
        'share_capital', 'vat_settlement',
        'iban', 'bank_name', 'bank_iban',
        'sector', 'customer_segment', 'customer_status', 'referred_by',
        'birth_date', 'birth_place', 'establishment_date',
        'notes', 'preferred_communication', 'language'
    ]
    
    for field in updatable_fields:
        if field in client_data and client_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(client_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE clients SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(client_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_client(client_id: int) -> bool:
    """Elimina un cliente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per rischi
def get_risks(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Recupera la lista dei rischi con filtri opzionali"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query principale con join per ottenere informazioni sul cliente
    query = """
        SELECT r.*, c.name as client_name, c.company as client_company
        FROM risks r
        LEFT JOIN clients c ON r.client_id = c.id
        WHERE 1=1
    """
    params = []
    
    if filters:
        if filters.get('client_id'):
            query += " AND r.client_id = %s"
            params.append(filters['client_id'])
        if filters.get('broker_id'):
            query += " AND r.broker_id = %s"
            params.append(filters['broker_id'])
        if filters.get('risk_type'):
            query += " AND r.risk_type = %s"
            params.append(filters['risk_type'])
    
    query += " ORDER BY r.created_at DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_risk(risk_id: int) -> Optional[Dict[str, Any]]:
    """Recupera un rischio specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT r.*, c.name as client_name, c.company as client_company
        FROM risks r
        LEFT JOIN clients c ON r.client_id = c.id
        WHERE r.id = %s
    """, (risk_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_risk(risk_data: Dict[str, Any]) -> int:
    """Crea un nuovo rischio e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO risks (client_id, broker_id, risk_type, details, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        risk_data['client_id'],
        risk_data.get('broker_id'),
        risk_data['risk_type'],
        json.dumps(risk_data.get('details', {})),
        datetime.now()
    )
    
    cursor.execute(query, params)
    risk_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return risk_id

def update_risk(risk_id: int, risk_data: Dict[str, Any]) -> bool:
    """Aggiorna un rischio esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    for field in ['client_id', 'broker_id', 'risk_type', 'details']:
        if field in risk_data and risk_data[field] is not None:
            set_parts.append(f"{field} = %s")
            if field == 'details':
                params.append(json.dumps(risk_data[field]))
            else:
                params.append(risk_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE risks SET {', '.join(set_parts)} WHERE id = %s"
    params.append(risk_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_risk(risk_id: int) -> bool:
    """Elimina un rischio"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM risks WHERE id = %s", (risk_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per polizze
def get_policies(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Recupera la lista delle polizze con filtri opzionali"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query principale con join per ottenere informazioni correlate
    query = """
        SELECT p.*, c.name as client_name, c.company as client_company
        FROM policies p
        LEFT JOIN risks r ON p.risk_id = r.id
        LEFT JOIN clients c ON r.client_id = c.id
        WHERE 1=1
    """
    params = []
    
    if filters:
        if filters.get('client_id'):
            query += " AND r.client_id = %s"
            params.append(filters['client_id'])
        if filters.get('client'):
            query += " AND (c.name LIKE %s OR c.company LIKE %s)"
            params.extend([f"%{filters['client']}%", f"%{filters['client']}%"])
        if filters.get('risk_type'):
            query += " AND r.risk_type = %s"
            params.append(filters['risk_type'])
        if filters.get('company'):
            query += " AND p.company LIKE %s"
            params.append(f"%{filters['company']}%")
        if filters.get('policy_number'):
            query += " AND p.policy_number LIKE %s"
            params.append(f"%{filters['policy_number']}%")
        if filters.get('status'):
            query += " AND p.status = %s"
            params.append(filters['status'])
        if filters.get('start_date_from'):
            query += " AND p.start_date >= %s"
            params.append(filters['start_date_from'])
        if filters.get('start_date_to'):
            query += " AND p.start_date <= %s"
            params.append(filters['start_date_to'])
        if filters.get('end_date_from'):
            query += " AND p.end_date >= %s"
            params.append(filters['end_date_from'])
        if filters.get('end_date_to'):
            query += " AND p.end_date <= %s"
            params.append(filters['end_date_to'])
        if filters.get('subscription_from'):
            query += " AND p.subscription_date >= %s"
            params.append(filters['subscription_from'])
        if filters.get('subscription_to'):
            query += " AND p.subscription_date <= %s"
            params.append(filters['subscription_to'])
        if filters.get('subscription_method'):
            query += " AND p.subscription_method = %s"
            params.append(filters['subscription_method'])
        if filters.get('payment_method'):
            query += " AND p.payment_method = %s"
            params.append(filters['payment_method'])
        if filters.get('premium_frequency'):
            query += " AND p.premium_frequency = %s"
            params.append(filters['premium_frequency'])
        if filters.get('premium_min') is not None:
            query += " AND p.premium_amount >= %s"
            params.append(filters['premium_min'])
        if filters.get('premium_max') is not None:
            query += " AND p.premium_amount <= %s"
            params.append(filters['premium_max'])
    
    query += " ORDER BY p.created_at DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_policy(policy_id: int) -> Optional[Dict[str, Any]]:
    """Recupera una polizza specifica per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM policies WHERE id = %s", (policy_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_policy(policy_data: Dict[str, Any]) -> int:
    """Crea una nuova polizza e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO policies (
            risk_id, company_id, company, policy_number, start_date, end_date, status,
            subscription_date, subscription_method,
            premium_amount, premium_frequency, payment_method,
            primary_subscriber_id, premium_delegate_id,
            created_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s,
            %s
        )
    """
    params = (
        policy_data['risk_id'],
        policy_data['company_id'],
        policy_data['company'],
        policy_data['policy_number'],
        policy_data['start_date'],
        policy_data['end_date'],
        policy_data.get('status', 'active'),
        policy_data.get('subscription_date'),
        policy_data.get('subscription_method', 'digital'),
        policy_data.get('premium_amount'),
        policy_data.get('premium_frequency', 'annual'),
        policy_data.get('payment_method'),
        policy_data.get('primary_subscriber_id'),
        policy_data.get('premium_delegate_id'),
        datetime.now()
    )
    
    cursor.execute(query, params)
    policy_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return policy_id

def update_policy(policy_id: int, policy_data: Dict[str, Any]) -> bool:
    """Aggiorna una polizza esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    # Campi aggiornabili
    updatable_fields = [
        'risk_id', 'company_id', 'company', 'policy_number', 'start_date', 'end_date', 'status',
        'subscription_date', 'subscription_method',
        'premium_amount', 'premium_frequency', 'payment_method',
        'primary_subscriber_id', 'premium_delegate_id'
    ]
    
    for field in updatable_fields:
        if field in policy_data and policy_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(policy_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE policies SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(policy_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_policy(policy_id: int) -> bool:
    """Elimina una polizza"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM policies WHERE id = %s", (policy_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per sinistri
def get_claims(filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Recupera la lista dei sinistri con filtri opzionali"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query principale con join per ottenere informazioni correlate
    query = """
        SELECT c.*, p.policy_number, cl.name as client_name, cl.company as client_company
        FROM claims c
        LEFT JOIN policies p ON c.policy_id = p.id
        LEFT JOIN risks r ON p.risk_id = r.id
        LEFT JOIN clients cl ON r.client_id = cl.id
        WHERE 1=1
    """
    params = []
    
    if filters:
        if filters.get('policy_id'):
            query += " AND c.policy_id = %s"
            params.append(filters['policy_id'])
        if filters.get('client_id'):
            query += " AND r.client_id = %s"
            params.append(filters['client_id'])
        if filters.get('status'):
            query += " AND c.status = %s"
            params.append(filters['status'])
        if filters.get('claim_date_from'):
            query += " AND c.claim_date >= %s"
            params.append(filters['claim_date_from'])
        if filters.get('claim_date_to'):
            query += " AND c.claim_date <= %s"
            params.append(filters['claim_date_to'])
        if filters.get('amount_min') is not None:
            query += " AND c.amount >= %s"
            params.append(filters['amount_min'])
        if filters.get('amount_max') is not None:
            query += " AND c.amount <= %s"
            params.append(filters['amount_max'])
        if filters.get('description'):
            query += " AND c.description LIKE %s"
            params.append(f"%{filters['description']}%")
    
    query += " ORDER BY c.claim_date DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_policy_claims(policy_id: int) -> List[Dict[str, Any]]:
    """Recupera tutti i sinistri associati a una polizza"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM claims 
        WHERE policy_id = %s
        ORDER BY claim_date DESC
    """, (policy_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_claim(claim_id: int) -> Optional[Dict[str, Any]]:
    """Recupera un sinistro specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM claims WHERE id = %s", (claim_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_claim(claim_data: Dict[str, Any]) -> int:
    """Crea un nuovo sinistro e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO claims (policy_id, claim_date, amount, description, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        claim_data['policy_id'],
        claim_data['claim_date'],
        claim_data['amount'],
        claim_data['description'],
        claim_data.get('status', 'open'),
        datetime.now()
    )
    
    cursor.execute(query, params)
    claim_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return claim_id

def update_claim(claim_id: int, claim_data: Dict[str, Any]) -> bool:
    """Aggiorna un sinistro esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    for field in ['policy_id', 'claim_date', 'amount', 'description', 'status']:
        if field in claim_data and claim_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(claim_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE claims SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(claim_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_claim(claim_id: int) -> bool:
    """Elimina un sinistro"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM claims WHERE id = %s", (claim_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per premi
def get_policy_premiums(policy_id: int) -> List[Dict[str, Any]]:
    """Recupera tutti i premi associati a una polizza"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM premiums 
        WHERE policy_id = %s
        ORDER BY due_date ASC
    """, (policy_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def create_premium(premium_data: Dict[str, Any]) -> int:
    """Crea un nuovo premio e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO premiums (policy_id, amount, due_date, payment_status, payment_date, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        premium_data['policy_id'],
        premium_data['amount'],
        premium_data['due_date'],
        premium_data.get('payment_status', 'pending'),
        premium_data.get('payment_date'),
        datetime.now()
    )
    
    cursor.execute(query, params)
    premium_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return premium_id

def update_premium(premium_id: int, premium_data: Dict[str, Any]) -> bool:
    """Aggiorna un premio esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    for field in ['amount', 'due_date', 'payment_status', 'payment_date']:
        if field in premium_data and premium_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(premium_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE premiums SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(premium_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_premium(premium_id: int) -> bool:
    """Elimina un premio"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM premiums WHERE id = %s", (premium_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per documenti sinistri
def get_claim_documents(claim_id: int) -> List[Dict[str, Any]]:
    """Recupera i documenti associati a un sinistro"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM claim_documents WHERE claim_id = %s ORDER BY uploaded_at DESC", (claim_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def create_claim_document(document_data: Dict[str, Any]) -> int:
    """Crea un nuovo documento per un sinistro e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO claim_documents (claim_id, document_name, document_type, file_path, file_size, uploaded_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        document_data['claim_id'],
        document_data['document_name'],
        document_data['document_type'],
        document_data['file_path'],
        document_data['file_size'],
        datetime.now()
    )
    
    cursor.execute(query, params)
    document_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return document_id

def delete_claim_document(document_id: int) -> bool:
    """Elimina un documento di sinistro"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM claim_documents WHERE id = %s", (document_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per comunicazioni sinistri
def get_claim_communications(claim_id: int) -> List[Dict[str, Any]]:
    """Recupera le comunicazioni associate a un sinistro"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM claim_communications WHERE claim_id = %s ORDER BY sent_at DESC", (claim_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def create_claim_communication(communication_data: Dict[str, Any]) -> int:
    """Crea una nuova comunicazione per un sinistro e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO claim_communications (claim_id, sender, recipient, subject, message, sent_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        communication_data['claim_id'],
        communication_data['sender'],
        communication_data['recipient'],
        communication_data['subject'],
        communication_data['message'],
        datetime.now(),
        communication_data.get('status', 'sent')
    )
    
    cursor.execute(query, params)
    communication_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return communication_id

def update_claim_communication(communication_id: int, communication_data: Dict[str, Any]) -> bool:
    """Aggiorna una comunicazione di sinistro"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    for field in ['sender', 'recipient', 'subject', 'message', 'status']:
        if field in communication_data and communication_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(communication_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE claim_communications SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(communication_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per relazioni clienti-rischi-polizze-sinistri
def get_client_risks(client_id: int) -> List[Dict[str, Any]]:
    """Recupera tutti i rischi associati a un cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT r.*, c.name as client_name, c.company as client_company
        FROM risks r
        LEFT JOIN clients c ON r.client_id = c.id
        WHERE r.client_id = %s
        ORDER BY r.created_at DESC
    """, (client_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_risk_policies(risk_id: int) -> List[Dict[str, Any]]:
    """Recupera tutte le polizze associate a un rischio"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.*, c.name as client_name, c.company as client_company
        FROM policies p
        LEFT JOIN clients c ON p.company_id = c.id
        WHERE p.risk_id = %s
        ORDER BY p.created_at DESC
    """, (risk_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

# Funzioni per sottoscrittori polizze
def get_policy_subscribers(policy_id: int) -> List[Dict[str, Any]]:
    """Recupera tutti i sottoscrittori associati a una polizza"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM policy_subscribers 
        WHERE policy_id = %s 
        ORDER BY subscriber_type, created_at
    """, (policy_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_policy_subscriber(subscriber_id: int) -> Optional[Dict[str, Any]]:
    """Recupera un sottoscrittore specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM policy_subscribers WHERE id = %s", (subscriber_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_policy_subscriber(subscriber_data: Dict[str, Any]) -> int:
    """Crea un nuovo sottoscrittore e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO policy_subscribers (
            policy_id, subscriber_type, entity_type,
            first_name, last_name, fiscal_code, birth_date, birth_place,
            company_name, vat_number, legal_form,
            email, phone, mobile,
            address, city, province, postal_code, country,
            created_at
        )
        VALUES (
            %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s
        )
    """
    params = (
        subscriber_data['policy_id'],
        subscriber_data.get('subscriber_type', 'primary'),
        subscriber_data['entity_type'],
        subscriber_data.get('first_name'),
        subscriber_data.get('last_name'),
        subscriber_data.get('fiscal_code'),
        subscriber_data.get('birth_date'),
        subscriber_data.get('birth_place'),
        subscriber_data.get('company_name'),
        subscriber_data.get('vat_number'),
        subscriber_data.get('legal_form'),
        subscriber_data.get('email'),
        subscriber_data.get('phone'),
        subscriber_data.get('mobile'),
        subscriber_data.get('address'),
        subscriber_data.get('city'),
        subscriber_data.get('province'),
        subscriber_data.get('postal_code'),
        subscriber_data.get('country', 'Italy'),
        datetime.now()
    )
    
    cursor.execute(query, params)
    subscriber_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return subscriber_id

def update_policy_subscriber(subscriber_id: int, subscriber_data: Dict[str, Any]) -> bool:
    """Aggiorna un sottoscrittore esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    # Campi aggiornabili
    updatable_fields = [
        'subscriber_type', 'entity_type',
        'first_name', 'last_name', 'fiscal_code', 'birth_date', 'birth_place',
        'company_name', 'vat_number', 'legal_form',
        'email', 'phone', 'mobile',
        'address', 'city', 'province', 'postal_code', 'country'
    ]
    
    for field in updatable_fields:
        if field in subscriber_data and subscriber_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(subscriber_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE policy_subscribers SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(subscriber_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_policy_subscriber(subscriber_id: int) -> bool:
    """Elimina un sottoscrittore"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM policy_subscribers WHERE id = %s", (subscriber_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Funzioni per delegati pagamento premi
def get_premium_delegates(client_id: int) -> List[Dict[str, Any]]:
    """Recupera tutti i delegati al pagamento associati a un cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM premium_delegates 
        WHERE client_id = %s AND is_active = TRUE
        ORDER BY created_at
    """, (client_id,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_premium_delegate(delegate_id: int) -> Optional[Dict[str, Any]]:
    """Recupera un delegato specifico per ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM premium_delegates WHERE id = %s", (delegate_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_premium_delegate(delegate_data: Dict[str, Any]) -> int:
    """Crea un nuovo delegato e restituisce l'ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO premium_delegates (
            client_id, delegate_type,
            first_name, last_name, fiscal_code,
            company_name, vat_number,
            email, phone, mobile,
            address, city, province, postal_code, country,
            authorization_level, authorization_start, authorization_end, is_active,
            created_at
        )
        VALUES (
            %s, %s,
            %s, %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s
        )
    """
    params = (
        delegate_data['client_id'],
        delegate_data['delegate_type'],
        delegate_data.get('first_name'),
        delegate_data.get('last_name'),
        delegate_data.get('fiscal_code'),
        delegate_data.get('company_name'),
        delegate_data.get('vat_number'),
        delegate_data.get('email'),
        delegate_data.get('phone'),
        delegate_data.get('mobile'),
        delegate_data.get('address'),
        delegate_data.get('city'),
        delegate_data.get('province'),
        delegate_data.get('postal_code'),
        delegate_data.get('country', 'Italy'),
        delegate_data.get('authorization_level', 'full'),
        delegate_data.get('authorization_start'),
        delegate_data.get('authorization_end'),
        delegate_data.get('is_active', True),
        datetime.now()
    )
    
    cursor.execute(query, params)
    delegate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return delegate_id

def update_premium_delegate(delegate_id: int, delegate_data: Dict[str, Any]) -> bool:
    """Aggiorna un delegato esistente"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Costruiamo la query dinamicamente solo con i campi forniti
    set_parts = []
    params = []
    
    # Campi aggiornabili
    updatable_fields = [
        'delegate_type',
        'first_name', 'last_name', 'fiscal_code',
        'company_name', 'vat_number',
        'email', 'phone', 'mobile',
        'address', 'city', 'province', 'postal_code', 'country',
        'authorization_level', 'authorization_start', 'authorization_end', 'is_active'
    ]
    
    for field in updatable_fields:
        if field in delegate_data and delegate_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(delegate_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE premium_delegates SET {', '.join(set_parts)}, updated_at = %s WHERE id = %s"
    params.append(datetime.now())
    params.append(delegate_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_premium_delegate(delegate_id: int) -> bool:
    """Elimina un delegato (imposta come non attivo)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE premium_delegates SET is_active = FALSE, updated_at = %s WHERE id = %s", 
                  (datetime.now(), delegate_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0