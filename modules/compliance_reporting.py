import openai
import json
from config import OPENAI_API_KEY
from modules.db import get_db_connection

# Inizializza il client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_compliance_report(report_type, period_start, period_end):
    """
    Genera report di compliance automatici
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Recupera i dati necessari per il report
    if report_type == "GDPR":
        # Recupera tutti i client con i loro dati
        cursor.execute("""
            SELECT id, name, company, email, created_at
            FROM clients
            WHERE created_at BETWEEN %s AND %s
        """, (period_start, period_end))
        
        client_data = cursor.fetchall()
        
        # Recupera storico modifiche
        cursor.execute("""
            SELECT table_name, action, timestamp, user_id
            FROM audit_log
            WHERE timestamp BETWEEN %s AND %s
            AND table_name IN ('clients', 'policies', 'risks')
        """, (period_start, period_end))
        
        audit_data = cursor.fetchall()
        
        report_content = {
            "client_data_summary": f"Totale client registrati: {len(client_data)}",
            "data_processing_activities": audit_data,
            "retention_policies": "Dati mantenuti per 365 giorni",
            "security_measures": "Crittografia AES-256, backup giornalieri"
        }
        
    elif report_type == "SOX":
        # Recupera dati finanziari
        cursor.execute("""
            SELECT 
                SUM(amount) as total_premiums,
                COUNT(*) as policies_count
            FROM premiums
            WHERE payment_date BETWEEN %s AND %s
        """, (period_start, period_end))
        
        financial_data = cursor.fetchone()
        
        report_content = {
            "financial_summary": financial_data,
            "controls_implementation": "Controlli finanziari implementati",
            "audit_trail": "Tracciamento completo delle transazioni"
        }
        
    elif report_type == "IVASS":
        # Recupera dati assicurativi
        cursor.execute("""
            SELECT 
                r.risk_type,
                COUNT(p.id) as policies_count,
                SUM(pr.amount) as total_premiums
            FROM policies p
            JOIN risks r ON p.risk_id = r.id
            JOIN premiums pr ON p.id = pr.policy_id
            WHERE p.start_date BETWEEN %s AND %s
            GROUP BY r.risk_type
        """, (period_start, period_end))
        
        insurance_data = cursor.fetchall()
        
        report_content = {
            "portfolio_analysis": insurance_data,
            "compliance_status": "Conforme alle direttive IVASS",
            "risk_distribution": "Distribuzione rischi monitorata"
        }
    
    conn.close()
    
    # Genera contenuto del report con AI
    prompt = f"""
    Genera un report di compliance {report_type} per il periodo {period_start} a {period_end}.
    
    Dati disponibili:
    {json.dumps(report_content, indent=2, default=str)}
    
    Il report deve includere:
    1. Intestazione ufficiale
    2. Riepilogo esecutivo
    3. Dettagli tecnici
    4. Conclusioni e raccomandazioni
    5. Firma digitale (simulata)
    
    Formato: JSON con campi: title, executive_summary, technical_details, conclusions, signature
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un esperto di compliance normativa nel settore assicurativo"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        report = json.loads(response.choices[0].message.content)
        
        # Salva il report nel database
        save_compliance_report(report_type, period_start, period_end, report)
        
        return report
    except Exception as e:
        return {
            "error": f"Generazione report fallita: {str(e)}",
            "title": f"Report {report_type} - Errore Generazione",
            "executive_summary": "Impossibile generare il report automatico",
            "technical_details": str(e),
            "conclusions": "Richiede generazione manuale",
            "signature": "Sistema BrokerFlow AI"
        }

def save_compliance_report(report_type, period_start, period_end, content):
    """Salva il report di compliance nel database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO compliance_reports (report_type, period_start, period_end, content)
        VALUES (%s, %s, %s, %s)
    """, (report_type, period_start, period_end, json.dumps(content)))
    
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return report_id

def get_compliance_reports(report_type=None):
    """Recupera i report di compliance"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if report_type:
        cursor.execute("""
            SELECT * FROM compliance_reports 
            WHERE report_type = %s 
            ORDER BY generated_at DESC
        """, (report_type,))
    else:
        cursor.execute("""
            SELECT * FROM compliance_reports 
            ORDER BY generated_at DESC
        """)
    
    reports = cursor.fetchall()
    conn.close()
    
    return reports