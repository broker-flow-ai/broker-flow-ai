import json
from modules.db import get_db_connection
from datetime import datetime, timedelta

def get_portfolio_analytics(company_id=None):
    """Recupera analisi aggregata del portafoglio"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query principale per analisi portafoglio
    query = """
        SELECT 
            r.risk_type,
            COUNT(p.id) as policy_count,
            SUM(CASE WHEN p.status = 'active' THEN 1 ELSE 0 END) as active_policies,
            AVG(ra.risk_score) as avg_risk_score,
            SUM(pr.amount) as total_premium,
            COUNT(c.id) as claim_count,
            SUM(c.amount) as total_claims,
            (SUM(c.amount) / SUM(pr.amount) * 100) as claims_ratio
        FROM policies p
        JOIN risks r ON p.risk_id = r.id
        LEFT JOIN risk_analysis ra ON r.id = ra.client_id
        LEFT JOIN premiums pr ON p.id = pr.policy_id
        LEFT JOIN claims c ON p.id = c.policy_id
    """
    
    params = []
    if company_id:
        query += " WHERE p.company_id = %s"
        params.append(company_id)
    
    query += " GROUP BY r.risk_type"
    
    cursor.execute(query, params)
    portfolio_data = cursor.fetchall()
    
    # Analisi trend temporale
    trend_query = """
        SELECT 
            DATE_FORMAT(p.created_at, '%Y-%m') as month,
            COUNT(p.id) as policies_issued,
            SUM(pr.amount) as premium_collected
        FROM policies p
        LEFT JOIN premiums pr ON p.id = pr.policy_id
    """
    
    if company_id:
        trend_query += " WHERE p.company_id = %s"
    
    trend_query += " GROUP BY DATE_FORMAT(p.created_at, '%Y-%m') ORDER BY month"
    
    cursor.execute(trend_query, params)
    trend_data = cursor.fetchall()
    
    # Analisi per settore
    sector_query = """
        SELECT 
            c.sector,
            COUNT(DISTINCT c.id) as client_count,
            COUNT(p.id) as policy_count,
            AVG(ra.risk_score) as avg_risk_score
        FROM clients c
        JOIN risks r ON c.id = r.client_id
        JOIN policies p ON r.id = p.risk_id
        LEFT JOIN risk_analysis ra ON c.id = ra.client_id
    """
    
    if company_id:
        sector_query += " WHERE p.company_id = %s"
    
    sector_query += " GROUP BY c.sector"
    
    cursor.execute(sector_query, params)
    sector_data = cursor.fetchall()
    
    conn.close()
    
    return {
        "portfolio_summary": portfolio_data,
        "trend_analysis": trend_data,
        "sector_breakdown": sector_data,
        "generated_at": datetime.now().isoformat()
    }

def get_company_performance(company_id):
    """Recupera performance specifica di una compagnia"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # KPI principali
    cursor.execute("""
        SELECT 
            COUNT(p.id) as total_policies,
            SUM(CASE WHEN p.status = 'active' THEN 1 ELSE 0 END) as active_policies,
            SUM(pr.amount) as total_premium,
            COUNT(c.id) as total_claims,
            SUM(c.amount) as total_claim_amount,
            (SUM(c.amount) / SUM(pr.amount) * 100) as loss_ratio
        FROM policies p
        LEFT JOIN premiums pr ON p.id = pr.policy_id
        LEFT JOIN claims c ON p.id = c.policy_id
        WHERE p.company_id = %s
    """, (company_id,))
    
    kpi_data = cursor.fetchone()
    
    # Confronto con benchmark di mercato (simulato)
    benchmark = {
        "market_avg_loss_ratio": 65.5,
        "market_avg_premium": 1250.00,
        "market_avg_risk_score": 45.2
    }
    
    # Calcola posizionamento rispetto al mercato
    performance = {
        "kpi": kpi_data,
        "benchmark": benchmark,
        "market_position": {
            "loss_ratio_vs_market": kpi_data["loss_ratio"] - benchmark["market_avg_loss_ratio"],
            "premium_vs_market": float(kpi_data["total_premium"] / kpi_data["total_policies"] if kpi_data["total_policies"] > 0 else 0) - benchmark["market_avg_premium"]
        }
    }
    
    conn.close()
    return performance

def get_broker_performance(broker_id):
    """Recupera performance di un broker partner"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            COUNT(r.id) as risks_processed,
            COUNT(p.id) as policies_issued,
            AVG(ra.risk_score) as avg_risk_score,
            COUNT(c.id) as claims_processed
        FROM risks r
        LEFT JOIN policies p ON r.id = p.risk_id
        LEFT JOIN risk_analysis ra ON r.client_id = ra.client_id
        LEFT JOIN claims c ON p.id = c.policy_id
        WHERE r.broker_id = %s
    """, (broker_id,))
    
    performance = cursor.fetchone()
    conn.close()
    return performance