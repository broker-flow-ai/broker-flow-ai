from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
import json
from fastapi.encoders import jsonable_encoder

from modules.db import get_db_connection
from modules.risk_analyzer import analyze_risk_sustainability, get_client_profile, save_risk_analysis
from modules.dashboard_analytics import get_portfolio_analytics, get_company_performance, get_broker_performance
from modules.compliance_reporting import generate_compliance_report, get_compliance_reports
from modules.ai_underwriting import suggest_pricing, predict_claims, automated_underwriting
from modules.b2b_integrations import integrate_with_sga_system, sync_with_broker_portal, process_payment
from modules.discount_program import create_discount, get_active_discounts, calculate_discounted_premium, get_broker_performance_metrics

app = FastAPI(title="BrokerFlow AI - API Assicurativa B2B2B", version="2.0.0")

# Modelli per le richieste API
class RiskAnalysisRequest(BaseModel):
    client_id: int

class ComplianceReportRequest(BaseModel):
    report_type: str
    period_start: date
    period_end: date

class PricingRequest(BaseModel):
    client_profile: dict
    risk_analysis: dict
    market_data: dict

class DiscountCreateRequest(BaseModel):
    company_id: int
    broker_id: int
    discount_type: str
    percentage: float
    start_date: date
    end_date: date

class PolicyIssuanceRequest(BaseModel):
    client_data: dict
    risk_data: dict
    premium_data: dict
    company_id: int

# Endpoint per analisi rischio
@app.post("/api/v1/insurance/risk-analysis")
async def api_risk_analysis(request: RiskAnalysisRequest):
    """Analisi avanzata del rischio assicurativo"""
    try:
        # Recupera profilo cliente
        client_profile = get_client_profile(request.client_id)
        
        if not client_profile["client_info"]:
            raise HTTPException(status_code=404, detail="Cliente non trovato")
        
        # Analizza rischio con AI
        analysis = analyze_risk_sustainability(
            client_profile["client_info"],
            client_profile["claim_history"]
        )
        
        # Salva analisi nel database
        analysis_id = save_risk_analysis(request.client_id, analysis)
        
        # Convert datetime objects to strings for JSON serialization
        response = {
            "analysis_id": analysis_id,
            "client_id": request.client_id,
            "analysis": analysis
        }
        
        return jsonable_encoder(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per dashboard analytics
@app.get("/api/v1/insurance/portfolio-analytics")
async def api_portfolio_analytics(company_id: Optional[int] = None):
    """Analisi aggregata del portafoglio assicurativo"""
    try:
        analytics = get_portfolio_analytics(company_id)
        return jsonable_encoder(analytics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/company-performance")
async def api_company_performance(company_id: int):
    """Performance specifica di una compagnia assicurativa"""
    try:
        performance = get_company_performance(company_id)
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/broker-performance")
async def api_broker_performance(broker_id: int):
    """Performance di un broker partner"""
    try:
        performance = get_broker_performance(broker_id)
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per compliance reporting
@app.post("/api/v1/insurance/compliance-report")
async def api_generate_compliance_report(request: ComplianceReportRequest):
    """Generazione automatica di report di compliance"""
    try:
        report = generate_compliance_report(
            request.report_type,
            request.period_start,
            request.period_end
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/compliance-reports")
async def api_get_compliance_reports(report_type: Optional[str] = None):
    """Recupero report di compliance"""
    try:
        reports = get_compliance_reports(report_type)
        return jsonable_encoder({"reports": reports})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per AI pricing e underwriting
@app.post("/api/v1/insurance/pricing-suggestion")
async def api_pricing_suggestion(request: PricingRequest):
    """Suggerimento di pricing basato su AI"""
    try:
        pricing = suggest_pricing(
            request.client_profile,
            request.risk_analysis,
            request.market_data
        )
        return pricing
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/insurance/claims-prediction")
async def api_claims_prediction(client_profile: dict, historical_data: dict):
    """Predizione sinistri futuri"""
    try:
        prediction = predict_claims(client_profile, historical_data)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/insurance/automated-underwriting")
async def api_automated_underwriting(risk_data: dict):
    """Processo di underwriting automatizzato"""
    try:
        underwriting = automated_underwriting(risk_data)
        return underwriting
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per gestione sconti e programmi fedeltà
@app.post("/api/v1/insurance/discounts")
async def api_create_discount(request: DiscountCreateRequest):
    """Crea un nuovo sconto/convenzione"""
    try:
        discount_id = create_discount(
            request.company_id,
            request.broker_id,
            request.discount_type,
            request.percentage,
            request.start_date,
            request.end_date
        )
        return {"discount_id": discount_id, "message": "Sconto creato con successo"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/discounts")
async def api_get_discounts(company_id: Optional[int] = None, broker_id: Optional[int] = None):
    """Recupera sconti attivi"""
    try:
        discounts = get_active_discounts(company_id, broker_id)
        return {"discounts": discounts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/discounted-premium")
async def api_calculate_discounted_premium(base_premium: float, company_id: int, broker_id: int):
    """Calcola premio scontato"""
    try:
        discounted_premium, discount_percentage = calculate_discounted_premium(base_premium, company_id, broker_id)
        return {
            "base_premium": base_premium,
            "discounted_premium": discounted_premium,
            "discount_percentage": discount_percentage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/broker-metrics")
async def api_broker_metrics(broker_id: int):
    """Recupera metriche performance broker"""
    try:
        metrics = get_broker_performance_metrics(broker_id)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per emissione polizza
@app.post("/api/v1/insurance/policy-issuance")
async def api_policy_issuance(request: PolicyIssuanceRequest):
    """Emissione completa di polizza con integrazioni"""
    try:
        # TODO: Implementare logica completa di emissione polizza
        # Questo è un esempio semplificato
        
        # 1. Analisi rischio
        # 2. Underwriting automatizzato
        # 3. Calcolo premio con sconti
        # 4. Integrazione con SGA
        # 5. Sincronizzazione con portale broker
        # 6. Processamento pagamento
        
        return {
            "policy_id": "POL20250001",
            "status": "issued",
            "message": "Polizza emessa con successo"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint di salute del sistema
@app.get("/api/v1/health")
async def health_check():
    """Verifica lo stato del sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# Endpoint per metriche di sistema
@app.get("/api/v1/metrics")
async def system_metrics():
    """Recupera metriche di sistema"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Conta record in varie tabelle
    metrics = {}
    tables = ['clients', 'policies', 'risks', 'claims', 'premiums']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        result = cursor.fetchone()
        metrics[table] = result['count']
    
    conn.close()
    
    response = {
        "database_metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonable_encoder(response)