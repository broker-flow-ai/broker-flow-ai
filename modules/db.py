import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from typing import List, Dict, Any, Optional
from datetime import date, datetime

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
        INSERT INTO clients (name, company, email, sector, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        client_data['name'],
        client_data['company'],
        client_data.get('email'),
        client_data.get('sector'),
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
    
    for field in ['name', 'company', 'email', 'sector']:
        if field in client_data and client_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(client_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE clients SET {', '.join(set_parts)} WHERE id = %s"
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
        INSERT INTO policies (risk_id, company_id, company, policy_number, start_date, end_date, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        policy_data['risk_id'],
        policy_data['company_id'],
        policy_data['company'],
        policy_data['policy_number'],
        policy_data['start_date'],
        policy_data['end_date'],
        policy_data.get('status', 'active'),
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
    
    for field in ['risk_id', 'company_id', 'company', 'policy_number', 'start_date', 'end_date', 'status']:
        if field in policy_data and policy_data[field] is not None:
            set_parts.append(f"{field} = %s")
            params.append(policy_data[field])
    
    if not set_parts:
        return False
    
    query = f"UPDATE policies SET {', '.join(set_parts)} WHERE id = %s"
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
        if filters.get('amount_min'):
            query += " AND c.amount >= %s"
            params.append(filters['amount_min'])
        if filters.get('amount_max'):
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
    
    query = f"UPDATE claims SET {', '.join(set_parts)} WHERE id = %s"
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
    
    query = f"UPDATE claim_communications SET {', '.join(set_parts)} WHERE id = %s"
    params.append(communication_id)
    
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0