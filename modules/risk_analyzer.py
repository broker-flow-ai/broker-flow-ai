import openai
import json
import decimal
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
                {"role": "system", "content": "Sei un analista assicurativo esperto. Rispondi in formato JSON valido con i seguenti campi: risk_score, sector_analysis, pricing_recommendation, recommendation_level, underwriting_notes"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Estrai e pulisci il contenuto JSON
        content = response.choices[0].message.content.strip()
        # Rimuovi eventuali marcatori di codice
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        analysis = json.loads(content)
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
    
    # Converti i datetime e i Decimal in tipi serializzabili
    for claim in claims:
        if 'claim_date' in claim and claim['claim_date']:
            claim['claim_date'] = claim['claim_date'].isoformat()
        if 'amount' in claim and claim['amount']:
            claim['amount'] = float(claim['amount'])
    
    # Converti i datetime e i Decimal nel client_info
    if client:
        if 'created_at' in client and client['created_at']:
            client['created_at'] = client['created_at'].isoformat()
        # Converti tutti i valori Decimal in float
        for key, value in client.items():
            if isinstance(value, decimal.Decimal):
                client[key] = float(value)
    
    return {
        "client_info": client,
        "claim_history": claims
    }

def save_risk_analysis(client_id, analysis):
    """Salva l'analisi del rischio nel database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Converti l'analisi in JSON serializzabile
        clean_analysis = {}
        for key, value in analysis.items():
            try:
                # Prova a serializzare il valore
                json.dumps(value)
                clean_analysis[key] = value
            except (TypeError, ValueError):
                # Se non si può serializzare, convertilo in stringa
                clean_analysis[key] = str(value)
        
        # Estrai i valori specifici con valori di default
        risk_score = clean_analysis.get('risk_score', 50)
        if isinstance(risk_score, (int, float, decimal.Decimal)):
            risk_score = float(risk_score)
        else:
            risk_score = 50.0
            
        sector_analysis = str(clean_analysis.get('sector_analysis', ''))
        pricing_recommendation = str(clean_analysis.get('pricing_recommendation', ''))
        underwriting_notes = str(clean_analysis.get('underwriting_notes', ''))
        
        # Gestisci recommendation_level per assicurarsi che sia uno dei valori ENUM permessi
        recommendation_level = str(clean_analysis.get('recommendation_level', 'Medio'))
        # Normalizza il valore
        if 'alto' in recommendation_level.lower():
            recommendation_level = 'Alto'
        elif 'basso' in recommendation_level.lower():
            recommendation_level = 'Basso'
        else:
            recommendation_level = 'Medio'  # Valore di default
        
        # Serializza l'intera analisi come JSON
        full_analysis_json = json.dumps(clean_analysis, default=str)
        
        cursor.execute("""
            INSERT INTO risk_analysis (client_id, risk_score, sector_analysis, 
                                     pricing_recommendation, recommendation_level, 
                                     underwriting_notes, full_analysis)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            client_id,
            risk_score,
            sector_analysis,
            pricing_recommendation,
            recommendation_level,
            underwriting_notes,
            full_analysis_json
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    except Exception as e:
        conn.close()
        raise Exception(f"Error saving risk analysis: {str(e)}")