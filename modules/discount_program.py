from modules.db import get_db_connection
from datetime import datetime, timedelta

def create_discount(company_id, broker_id, discount_type, percentage, start_date, end_date):
    """
    Crea un nuovo sconto/convenzione
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO discounts (company_id, broker_id, discount_type, discount_percentage, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (company_id, broker_id, discount_type, percentage, start_date, end_date))
    
    discount_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return discount_id

def get_active_discounts(company_id=None, broker_id=None):
    """
    Recupera sconti attivi
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT d.*, c.name as company_name, b.name as broker_name
        FROM discounts d
        JOIN clients c ON d.company_id = c.id
        JOIN clients b ON d.broker_id = b.id
        WHERE d.end_date >= CURDATE()
    """
    
    params = []
    if company_id:
        query += " AND d.company_id = %s"
        params.append(company_id)
    
    if broker_id:
        query += " AND d.broker_id = %s"
        params.append(broker_id)
    
    query += " ORDER BY d.start_date"
    
    cursor.execute(query, params)
    discounts = cursor.fetchall()
    conn.close()
    
    return discounts

def calculate_discounted_premium(base_premium, company_id, broker_id):
    """
    Calcola il premio scontato applicabile
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT discount_percentage
        FROM discounts
        WHERE company_id = %s AND broker_id = %s
        AND start_date <= CURDATE() AND end_date >= CURDATE()
        ORDER BY discount_percentage DESC
        LIMIT 1
    """, (company_id, broker_id))
    
    discount = cursor.fetchone()
    conn.close()
    
    if discount:
        discount_amount = base_premium * (discount['discount_percentage'] / 100)
        return base_premium - discount_amount, discount['discount_percentage']
    else:
        return base_premium, 0

def get_broker_performance_metrics(broker_id):
    """
    Recupera metriche di performance del broker per programmi fedeltà
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Volume polizze
    cursor.execute("""
        SELECT COUNT(*) as policies_count, SUM(pr.amount) as total_premium
        FROM policies p
        JOIN risks r ON p.risk_id = r.id
        JOIN premiums pr ON p.id = pr.policy_id
        WHERE r.broker_id = %s AND p.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    """, (broker_id,))
    
    volume_data = cursor.fetchone()
    
    # Qualità (sinistri)
    cursor.execute("""
        SELECT COUNT(c.id) as claims_count, SUM(c.amount) as total_claims
        FROM claims c
        JOIN policies p ON c.policy_id = p.id
        JOIN risks r ON p.risk_id = r.id
        WHERE r.broker_id = %s AND c.claim_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    """, (broker_id,))
    
    claims_data = cursor.fetchone()
    
    # Calcola punteggio performance
    policies_count = volume_data['policies_count'] or 0
    total_premium = volume_data['total_premium'] or 0
    claims_count = claims_data['claims_count'] or 0
    total_claims = claims_data['total_claims'] or 0
    
    # Punteggio base su volume
    volume_score = min(policies_count / 100, 10) * 5  # Max 50 punti
    
    # Punteggio su qualità (minore sinistrosità = punteggio migliore)
    if total_premium > 0:
        loss_ratio = (total_claims / total_premium) * 100
        quality_score = max(0, (100 - loss_ratio) / 2)  # Max 50 punti
    else:
        quality_score = 25  # Punteggio medio se non ci sono dati
    
    total_score = volume_score + quality_score
    
    conn.close()
    
    return {
        "volume_metrics": volume_data,
        "claims_metrics": claims_data,
        "performance_score": total_score,
        "tier": determine_broker_tier(total_score)
    }

def determine_broker_tier(score):
    """
    Determina il livello del broker basato sul punteggio
    """
    if score >= 90:
        return "Platinum"
    elif score >= 75:
        return "Gold"
    elif score >= 60:
        return "Silver"
    else:
        return "Bronze"