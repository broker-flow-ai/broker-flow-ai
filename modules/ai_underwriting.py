import openai
import json
from config import OPENAI_API_KEY
from modules.db import get_db_connection

# Inizializza il client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def suggest_pricing(client_profile, risk_analysis, market_data):
    """
    Suggerisce pricing basato su AI per una polizza
    """
    prompt = f"""
    In base al profilo cliente e all'analisi del rischio, suggerisci un pricing competitivo:
    
    Profilo Cliente:
    {json.dumps(client_profile, indent=2)}
    
    Analisi Rischio:
    {json.dumps(risk_analysis, indent=2)}
    
    Dati di Mercato:
    {json.dumps(market_data, indent=2)}
    
    Fornisci:
    1. Premium suggerito
    2. Massimali consigliati
    3. Franchigie ottimali
    4. Coperture consigliate
    5. Giustificazione del pricing
    
    Rispondi in formato JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un underwriter esperto nel settore assicurativo"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        pricing = json.loads(response.choices[0].message.content)
        return pricing
    except Exception as e:
        return {
            "error": f"Suggerimento pricing non disponibile: {str(e)}",
            "premium": 0,
            "coverage": "Contattare underwriting",
            "franchise": "Da definire",
            "justification": "Richiede valutazione manuale"
        }

def predict_claims(client_profile, historical_data):
    """
    Predice la probabilità e l'impatto dei sinistri futuri
    """
    prompt = f"""
    Analizza il profilo cliente e i dati storici per predire sinistri futuri:
    
    Profilo Cliente:
    {json.dumps(client_profile, indent=2)}
    
    Dati Storici:
    {json.dumps(historical_data, indent=2)}
    
    Fornisci:
    1. Probabilità sinistro annuale (%)
    2. Impatto medio previsto (€)
    3. Tipologie di sinistro più probabili
    4. Periodi di maggiore esposizione
    5. Raccomandazioni di mitigazione
    
    Rispondi in formato JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un analista predittivo nel settore assicurativo"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        prediction = json.loads(response.choices[0].message.content)
        return prediction
    except Exception as e:
        return {
            "error": f"Predizione non disponibile: {str(e)}",
            "claim_probability": 0,
            "expected_impact": 0,
            "likely_claim_types": [],
            "high_risk_periods": [],
            "mitigation_recommendations": "Richiede valutazione manuale"
        }

def automated_underwriting(risk_data):
    """
    Processo di underwriting automatizzato
    """
    prompt = f"""
    Esegui un underwriting automatizzato per questa richiesta:
    
    Dati Rischio:
    {json.dumps(risk_data, indent=2)}
    
    Fornisci:
    1. Decisione underwriting (Approvato/Condizionato/Rifiutato)
    2. Condizioni speciali
    3. Limiti di copertura
    4. Esclusioni
    5. Raccomandazioni per il broker
    
    Rispondi in formato JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sei un underwriter capo con 20 anni di esperienza"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        underwriting = json.loads(response.choices[0].message.content)
        return underwriting
    except Exception as e:
        return {
            "error": f"Underwriting non disponibile: {str(e)}",
            "decision": "Condizionato",
            "conditions": ["Richiede documentazione aggiuntiva"],
            "coverage_limits": "Da definire",
            "exclusions": ["In attesa di valutazione"],
            "broker_recommendations": "Contattare underwriting specializzato"
        }