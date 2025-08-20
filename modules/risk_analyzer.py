import openai
import json
from config import OPENAI_API_KEY
from modules.db import get_db_connection

# Inizializza il client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def analyze_risk_sustainability(client_profile, historical_data):
    """
    Analizza la sostenibilità del rischio per la compagnia assicurativa
    - Profilo cliente (settore, storico sinistri, fatturato)
    - Analisi comparativa con portafoglio esistente
    - Score di rischio assicurativo
    - Raccomandazioni pricing
    """
    prompt = f"""
    Analizza la sostenibilità del rischio assicurativo per questo cliente:
    
    Profilo Cliente:
    {json.dumps(client_profile, indent=2)}
    
    Dati Storici:
    {json.dumps(historical_data, indent=2)}
    
    Fornisci un'analisi completa con:
    1. Score di rischio (0-100, dove 0 è rischio minimo)
    2. Analisi settore e comparazione con benchmark
    3. Raccomandazioni di pricing
    4. Livello di raccomandazione (Alto/Medio/Basso)
    5. Note di underwriting
    
    Rispondi in formato JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un analista assicurativo esperto"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    except Exception as e:
        return {
            "error": f"Analisi non disponibile: {str(e)}",
            "risk_score": 50,
            "sector_analysis": "Analisi temporaneamente non disponibile",
            "pricing_recommendation": "Contattare underwriting",
            "recommendation_level": "Medio",
            "underwriting_notes": "Richiede valutazione manuale"
        }

def get_client_profile(client_id):
    """Recupera il profilo completo del cliente dal database"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Recupera informazioni cliente
    cursor.execute("""
        SELECT c.*, 
               COUNT(p.id) as policies_count,
               SUM(CASE WHEN p.status = 'active' THEN 1 ELSE 0 END) as active_policies
        FROM clients c
        LEFT JOIN risks r ON c.id = r.client_id
        LEFT JOIN policies p ON r.id = p.risk_id
        WHERE c.id = %s
        GROUP BY c.id
    """, (client_id,))
    
    client = cursor.fetchone()
    
    # Recupera storico sinistri
    cursor.execute("""
        SELECT c.claim_date, c.amount, p.company, r.risk_type
        FROM claims c
        JOIN policies p ON c.policy_id = p.id
        JOIN risks r ON p.risk_id = r.id
        WHERE r.client_id = %s
        ORDER BY c.claim_date DESC
    """, (client_id,))
    
    claims = cursor.fetchall()
    
    conn.close()
    
    # Converti i datetime in stringhe per evitare problemi di serializzazione
    for claim in claims:
        if 'claim_date' in claim and claim['claim_date']:
            claim['claim_date'] = claim['claim_date'].isoformat()
    
    # Converti i datetime nel client_info
    if client and 'created_at' in client and client['created_at']:
        client['created_at'] = client['created_at'].isoformat()
    
    return {
        "client_info": client,
        "claim_history": claims
    }

def save_risk_analysis(client_id, analysis):
    """Salva l'analisi del rischio nel database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO risk_analysis (client_id, risk_score, sector_analysis, 
                                 pricing_recommendation, recommendation_level, 
                                 underwriting_notes, full_analysis)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        client_id,
        analysis.get('risk_score', 50),
        analysis.get('sector_analysis', ''),
        analysis.get('pricing_recommendation', ''),
        analysis.get('recommendation_level', 'Medio'),
        analysis.get('underwriting_notes', ''),
        json.dumps(analysis)
    ))
    
    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return analysis_id