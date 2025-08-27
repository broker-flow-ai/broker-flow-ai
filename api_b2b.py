from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
import json
import os
from fastapi.encoders import jsonable_encoder

from modules.db import (
    get_db_connection,
    # Funzioni per clienti
    get_clients, get_client, create_client, update_client, delete_client,
    # Funzioni per polizze
    get_policies, get_policy, create_policy, update_policy, delete_policy,
    # Funzioni per sinistri
    get_claims, get_claim, create_claim, update_claim, delete_claim,
    # Funzioni per documenti sinistri
    get_claim_documents, create_claim_document, delete_claim_document,
    # Funzioni per comunicazioni sinistri
    get_claim_communications, create_claim_communication, update_claim_communication
)
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

class EmailRequest(BaseModel):
    recipient_email: str
    format_type: str = "pdf"

class RiskCreateRequest(BaseModel):
    client_id: int
    broker_id: Optional[int] = None
    risk_type: str
    details: Optional[dict] = None

class RiskUpdateRequest(BaseModel):
    client_id: Optional[int] = None
    broker_id: Optional[int] = None
    risk_type: Optional[str] = None
    details: Optional[dict] = None

class PolicyIssuanceRequest(BaseModel):
    client_data: dict
    risk_data: dict
    premium_data: dict
    company_id: int

# Modelli per clienti, polizze e sinistri
class ClientCreateRequest(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    sector: Optional[str] = None

class ClientUpdateRequest(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    sector: Optional[str] = None

class PolicyCreateRequest(BaseModel):
    risk_id: int
    company_id: int
    company: str
    policy_number: str
    start_date: date
    end_date: date
    status: str = "active"

class PolicyUpdateRequest(BaseModel):
    risk_id: Optional[int] = None
    company_id: Optional[int] = None
    company: Optional[str] = None
    policy_number: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class ClaimCreateRequest(BaseModel):
    policy_id: int
    claim_date: date
    amount: float
    description: str
    status: str = "open"

class ClaimUpdateRequest(BaseModel):
    policy_id: Optional[int] = None
    claim_date: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ClaimDocumentCreateRequest(BaseModel):
    claim_id: int
    document_name: str
    document_type: str
    file_path: str
    file_size: int

class ClaimCommunicationCreateRequest(BaseModel):
    claim_id: int
    sender: str
    recipient: str
    subject: str
    message: str
    status: str = "sent"

class ClaimCommunicationUpdateRequest(BaseModel):
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None

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
        import traceback
        error_details = f"Error in risk analysis: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_details)  # Log per debugging
        raise HTTPException(status_code=500, detail=error_details)

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
        return jsonable_encoder(performance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/broker-performance")
async def api_broker_performance(broker_id: int):
    """Performance di un broker partner"""
    try:
        performance = get_broker_performance(broker_id)
        return jsonable_encoder(performance)
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
        return jsonable_encoder(report)
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
        return jsonable_encoder(pricing)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/insurance/claims-prediction")
async def api_claims_prediction(client_profile: dict, historical_data: dict):
    """Predizione sinistri futuri"""
    try:
        prediction = predict_claims(client_profile, historical_data)
        return jsonable_encoder(prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/insurance/automated-underwriting")
async def api_automated_underwriting(risk_data: dict):
    """Processo di underwriting automatizzato"""
    try:
        underwriting = automated_underwriting(risk_data)
        return jsonable_encoder(underwriting)
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
        return jsonable_encoder({"discount_id": discount_id, "message": "Sconto creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/discounts")
async def api_get_discounts(company_id: Optional[int] = None, broker_id: Optional[int] = None):
    """Recupera sconti attivi"""
    try:
        discounts = get_active_discounts(company_id, broker_id)
        return jsonable_encoder({"discounts": discounts})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/discounted-premium")
async def api_calculate_discounted_premium(base_premium: float, company_id: int, broker_id: int):
    """Calcola premio scontato"""
    try:
        discounted_premium, discount_percentage = calculate_discounted_premium(base_premium, company_id, broker_id)
        return jsonable_encoder({
            "base_premium": base_premium,
            "discounted_premium": discounted_premium,
            "discount_percentage": discount_percentage
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/broker-metrics")
async def api_broker_metrics(broker_id: int):
    """Recupera metriche performance broker"""
    try:
        metrics = get_broker_performance_metrics(broker_id)
        return jsonable_encoder(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per gestione clienti
@app.get("/api/v1/clients")
async def api_get_clients(
    name: Optional[str] = None,
    company: Optional[str] = None,
    sector: Optional[str] = None,
    email: Optional[str] = None
):
    """Recupera la lista dei clienti con filtri opzionali"""
    try:
        filters = {}
        if name: filters['name'] = name
        if company: filters['company'] = company
        if sector: filters['sector'] = sector
        if email: filters['email'] = email
        
        clients = get_clients(filters)
        return jsonable_encoder(clients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/clients/{client_id}")
async def api_get_client(client_id: int):
    """Recupera un cliente specifico per ID"""
    try:
        client = get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente non trovato")
        return jsonable_encoder(client)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/clients")
async def api_create_client(request: ClientCreateRequest):
    """Crea un nuovo cliente"""
    try:
        client_data = request.dict()
        client_id = create_client(client_data)
        return jsonable_encoder({"client_id": client_id, "message": "Cliente creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/clients/{client_id}")
async def api_update_client(client_id: int, request: ClientUpdateRequest):
    """Aggiorna un cliente esistente"""
    try:
        client_data = request.dict(exclude_unset=True)
        if not client_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_client(client_id, client_data)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente non trovato")
        
        return jsonable_encoder({"client_id": client_id, "message": "Cliente aggiornato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/clients/{client_id}")
async def api_delete_client(client_id: int):
    """Elimina un cliente"""
    try:
        success = delete_client(client_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente non trovato")
        
        return jsonable_encoder({"client_id": client_id, "message": "Cliente eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per gestione polizze
@app.get("/api/v1/policies")
async def api_get_policies(
    client_id: Optional[int] = None,
    risk_type: Optional[str] = None,
    company: Optional[str] = None,
    policy_number: Optional[str] = None,
    status: Optional[str] = None
):
    """Recupera la lista delle polizze con filtri opzionali"""
    try:
        filters = {}
        if client_id: filters['client_id'] = client_id
        if risk_type: filters['risk_type'] = risk_type
        if company: filters['company'] = company
        if policy_number: filters['policy_number'] = policy_number
        if status: filters['status'] = status
        
        policies = get_policies(filters)
        return jsonable_encoder(policies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policies/{policy_id}")
async def api_get_policy(policy_id: int):
    """Recupera una polizza specifica per ID"""
    try:
        policy = get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Polizza non trovata")
        return jsonable_encoder(policy)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per relazioni clienti-rischi-polizze-sinistri
@app.get("/api/v1/clients/{client_id}/risks")
async def api_get_client_risks(client_id: int):
    """Recupera tutti i rischi associati a un cliente"""
    try:
        risks = get_client_risks(client_id)
        return jsonable_encoder(risks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/risks/{risk_id}/policies")
async def api_get_risk_policies(risk_id: int):
    """Recupera tutte le polizze associate a un rischio"""
    try:
        policies = get_risk_policies(risk_id)
        return jsonable_encoder(policies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policies/{policy_id}/claims")
async def api_get_policy_claims(policy_id: int):
    """Recupera tutti i sinistri associati a una polizza"""
    try:
        claims = get_policy_claims(policy_id)
        return jsonable_encoder(claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/policies")
async def api_create_policy(request: PolicyCreateRequest):
    """Crea una nuova polizza"""
    try:
        policy_data = request.dict()
        policy_id = create_policy(policy_data)
        return jsonable_encoder({"policy_id": policy_id, "message": "Polizza creata con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per gestione rischi
@app.get("/api/v1/risks")
async def api_get_risks(
    client_id: Optional[int] = None,
    broker_id: Optional[int] = None,
    risk_type: Optional[str] = None
):
    """Recupera la lista dei rischi con filtri opzionali"""
    try:
        filters = {}
        if client_id: filters['client_id'] = client_id
        if broker_id: filters['broker_id'] = broker_id
        if risk_type: filters['risk_type'] = risk_type
        
        risks = get_risks(filters)
        return jsonable_encoder({"risks": risks})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/risks/{risk_id}")
async def api_get_risk(risk_id: int):
    """Recupera un rischio specifico per ID"""
    try:
        risk = get_risk(risk_id)
        if not risk:
            raise HTTPException(status_code=404, detail="Rischio non trovato")
        return jsonable_encoder(risk)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/risks")
async def api_create_risk(request: RiskCreateRequest):
    """Crea un nuovo rischio"""
    try:
        risk_data = request.dict()
        risk_id = create_risk(risk_data)
        return jsonable_encoder({"risk_id": risk_id, "message": "Rischio creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/risks/{risk_id}")
async def api_update_risk(risk_id: int, request: RiskUpdateRequest):
    """Aggiorna un rischio esistente"""
    try:
        risk_data = request.dict(exclude_unset=True)
        if not risk_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_risk(risk_id, risk_data)
        if not success:
            raise HTTPException(status_code=404, detail="Rischio non trovato")
        
        return jsonable_encoder({"risk_id": risk_id, "message": "Rischio aggiornato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/risks/{risk_id}")
async def api_delete_risk(risk_id: int):
    """Elimina un rischio"""
    try:
        success = delete_risk(risk_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rischio non trovato")
        
        return jsonable_encoder({"risk_id": risk_id, "message": "Rischio eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per relazioni clienti-rischi-polizze-sinistri
@app.get("/api/v1/clients/{client_id}/risks")
async def api_get_client_risks(client_id: int):
    """Recupera tutti i rischi associati a un cliente"""
    try:
        risks = get_client_risks(client_id)
        return jsonable_encoder(risks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/risks/{risk_id}/policies")
async def api_get_risk_policies(risk_id: int):
    """Recupera tutte le polizze associate a un rischio"""
    try:
        policies = get_risk_policies(risk_id)
        return jsonable_encoder(policies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policies/{policy_id}/claims")
async def api_get_policy_claims(policy_id: int):
    """Recupera tutti i sinistri associati a una polizza"""
    try:
        claims = get_policy_claims(policy_id)
        return jsonable_encoder(claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policies/{policy_id}/premiums")
async def api_get_policy_premiums(policy_id: int):
    """Recupera tutti i premi associati a una polizza"""
    try:
        premiums = get_policy_premiums(policy_id)
        return jsonable_encoder(premiums)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/policies")
async def api_update_policy(policy_id: int, request: PolicyUpdateRequest):
    """Aggiorna una polizza esistente"""
    try:
        policy_data = request.dict(exclude_unset=True)
        if not policy_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_policy(policy_id, policy_data)
        if not success:
            raise HTTPException(status_code=404, detail="Polizza non trovata")
        
        return jsonable_encoder({"policy_id": policy_id, "message": "Polizza aggiornata con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/policies/{policy_id}")
async def api_delete_policy(policy_id: int):
    """Elimina una polizza"""
    try:
        success = delete_policy(policy_id)
        if not success:
            raise HTTPException(status_code=404, detail="Polizza non trovata")
        
        return jsonable_encoder({"policy_id": policy_id, "message": "Polizza eliminata con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per gestione sinistri
@app.get("/api/v1/claims")
async def api_get_claims(
    policy_id: Optional[int] = None,
    status: Optional[str] = None,
    claim_date_from: Optional[date] = None,
    claim_date_to: Optional[date] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    description: Optional[str] = None
):
    """Recupera la lista dei sinistri con filtri opzionali"""
    try:
        filters = {}
        if policy_id: filters['policy_id'] = policy_id
        if status: filters['status'] = status
        if claim_date_from: filters['claim_date_from'] = claim_date_from
        if claim_date_to: filters['claim_date_to'] = claim_date_to
        if amount_min: filters['amount_min'] = amount_min
        if amount_max: filters['amount_max'] = amount_max
        if description: filters['description'] = description
        
        claims = get_claims(filters)
        return jsonable_encoder(claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/claims/{claim_id}")
async def api_get_claim(claim_id: int):
    """Recupera un sinistro specifico per ID"""
    try:
        claim = get_claim(claim_id)
        if not claim:
            raise HTTPException(status_code=404, detail="Sinistro non trovato")
        return jsonable_encoder(claim)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/claims")
async def api_create_claim(request: ClaimCreateRequest):
    """Crea un nuovo sinistro"""
    try:
        claim_data = request.dict()
        claim_id = create_claim(claim_data)
        return jsonable_encoder({"claim_id": claim_id, "message": "Sinistro creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/claims/{claim_id}")
async def api_update_claim(claim_id: int, request: ClaimUpdateRequest):
    """Aggiorna un sinistro esistente"""
    try:
        claim_data = request.dict(exclude_unset=True)
        if not claim_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_claim(claim_id, claim_data)
        if not success:
            raise HTTPException(status_code=404, detail="Sinistro non trovato")
        
        return jsonable_encoder({"claim_id": claim_id, "message": "Sinistro aggiornato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/claims/{claim_id}")
async def api_delete_claim(claim_id: int):
    """Elimina un sinistro"""
    try:
        success = delete_claim(claim_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sinistro non trovato")
        
        return jsonable_encoder({"claim_id": claim_id, "message": "Sinistro eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per documenti sinistri
@app.get("/api/v1/claims/{claim_id}/documents")
async def api_get_claim_documents(claim_id: int):
    """Recupera i documenti associati a un sinistro"""
    try:
        documents = get_claim_documents(claim_id)
        return jsonable_encoder(documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/claim-documents")
async def api_create_claim_document(request: ClaimDocumentCreateRequest):
    """Crea un nuovo documento per un sinistro"""
    try:
        document_data = request.dict()
        document_id = create_claim_document(document_data)
        return jsonable_encoder({"document_id": document_id, "message": "Documento creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/claim-documents/{document_id}")
async def api_delete_claim_document(document_id: int):
    """Elimina un documento di sinistro"""
    try:
        success = delete_claim_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Documento non trovato")
        
        return jsonable_encoder({"document_id": document_id, "message": "Documento eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per comunicazioni sinistri
@app.get("/api/v1/claims/{claim_id}/communications")
async def api_get_claim_communications(claim_id: int):
    """Recupera le comunicazioni associate a un sinistro"""
    try:
        communications = get_claim_communications(claim_id)
        return jsonable_encoder(communications)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/claim-communications")
async def api_create_claim_communication(request: ClaimCommunicationCreateRequest):
    """Crea una nuova comunicazione per un sinistro"""
    try:
        communication_data = request.dict()
        communication_id = create_claim_communication(communication_data)
        return jsonable_encoder({"communication_id": communication_id, "message": "Comunicazione creata con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/claim-communications/{communication_id}")
async def api_update_claim_communication(communication_id: int, request: ClaimCommunicationUpdateRequest):
    """Aggiorna una comunicazione di sinistro"""
    try:
        communication_data = request.dict(exclude_unset=True)
        if not communication_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_claim_communication(communication_id, communication_data)
        if not success:
            raise HTTPException(status_code=404, detail="Comunicazione non trovata")
        
        return jsonable_encoder({"communication_id": communication_id, "message": "Comunicazione aggiornata con successo"})
    except HTTPException:
        raise
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
        
        return jsonable_encoder({
            "policy_id": "POL20250001",
            "status": "issued",
            "message": "Polizza emessa con successo"
        })
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

class EmailRequest(BaseModel):
    recipient_email: str
    format_type: str = "pdf"

# Endpoint per download report compliance
@app.get("/api/v1/compliance/reports/{report_id}/download/pdf")
async def download_compliance_report_pdf(report_id: int):
    """Download report di compliance in formato PDF"""
    try:
        # Recupera il report dal database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM compliance_reports WHERE id = %s", (report_id,))
        report = cursor.fetchone()
        
        conn.close()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report non trovato")
        
        # Verifica che il file esista
        file_path = report.get('file_path')
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File del report non trovato")
        
        # Restituisce il file
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='application/pdf'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/compliance/reports/{report_id}/download/excel")
async def download_compliance_report_excel(report_id: int):
    """Download report di compliance in formato Excel"""
    try:
        # Recupera il report dal database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM compliance_reports WHERE id = %s", (report_id,))
        report = cursor.fetchone()
        
        conn.close()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report non trovato")
        
        # Verifica che il file esista
        file_path = report.get('excel_path')
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File del report non trovato")
        
        # Restituisce il file
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/compliance/reports/{report_id}/download/word")
async def download_compliance_report_word(report_id: int):
    """Download report di compliance in formato Word"""
    try:
        # Recupera il report dal database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM compliance_reports WHERE id = %s", (report_id,))
        report = cursor.fetchone()
        
        conn.close()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report non trovato")
        
        # Verifica che il file esista
        file_path = report.get('word_path')
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File del report non trovato")
        
        # Restituisce il file
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/compliance/reports/{report_id}/send-email")
async def send_compliance_report_email(report_id: int, request: EmailRequest):
    """Invia un report di compliance via email"""
    try:
        # Import locale per evitare dipendenze circolari
        from modules.compliance_reporting import send_report_via_email
        
        result = send_report_via_email(report_id, request.recipient_email, request.format_type)
        
        if result["success"]:
            return jsonable_encoder({"message": "Email inviata con successo"})
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/compliance/reports/{report_id}")
async def delete_compliance_report(report_id: int):
    """Elimina un report di compliance"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Recupera i percorsi dei file prima dell'eliminazione
        cursor.execute("SELECT file_path, excel_path, word_path FROM compliance_reports WHERE id = %s", (report_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            raise HTTPException(status_code=404, detail="Report non trovato")
        
        pdf_path, excel_path, word_path = result
        
        # Elimina il record dal database
        cursor.execute("DELETE FROM compliance_reports WHERE id = %s", (report_id,))
        conn.commit()
        conn.close()
        
        # Elimina i file fisici se esistono
        for file_path in [pdf_path, excel_path, word_path]:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        
        return jsonable_encoder({"message": "Report eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))