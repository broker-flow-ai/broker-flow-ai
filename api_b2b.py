from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
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
from modules.auth_api import router as auth_router
from modules.auth_middleware import get_current_user, require_permission, require_role
from modules.auth_models import User, UserRole

app = FastAPI(title="BrokerFlow AI - API Assicurativa B2B2B", version="2.0.0")

# Aggiungi il router di autenticazione
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


class PolicySubscriberCreateRequest(BaseModel):
    policy_id: int
    subscriber_type: str = "primary"
    entity_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fiscal_code: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None
    legal_form: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Italy"


class PolicySubscriberUpdateRequest(BaseModel):
    policy_id: Optional[int] = None
    subscriber_type: Optional[str] = None
    entity_type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fiscal_code: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None
    legal_form: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class PremiumDelegateCreateRequest(BaseModel):
    client_id: int
    delegate_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fiscal_code: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "Italy"
    authorization_level: str = "full"
    authorization_start: Optional[date] = None
    authorization_end: Optional[date] = None
    is_active: bool = True


class PremiumDelegateUpdateRequest(BaseModel):
    client_id: Optional[int] = None
    delegate_type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fiscal_code: Optional[str] = None
    company_name: Optional[str] = None
    vat_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    authorization_level: Optional[str] = None
    authorization_start: Optional[date] = None
    authorization_end: Optional[date] = None
    is_active: Optional[bool] = None


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

# Endpoint per sottoscrittori polizze
@app.get("/api/v1/policy-subscribers")
async def api_get_policy_subscribers(policy_id: Optional[int] = None):
    """Recupera la lista dei sottoscrittori"""
    try:
        from modules.db import get_policy_subscribers
        if policy_id:
            subscribers = get_policy_subscribers(policy_id)
        else:
            # Se non viene specificato policy_id, restituiamo un errore
            raise HTTPException(status_code=400, detail="policy_id è obbligatorio")
        return jsonable_encoder(subscribers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policy-subscribers/{subscriber_id}")
async def api_get_policy_subscriber(subscriber_id: int):
    """Recupera un sottoscrittore specifico per ID"""
    try:
        from modules.db import get_policy_subscriber
        subscriber = get_policy_subscriber(subscriber_id)
        if not subscriber:
            raise HTTPException(status_code=404, detail="Sottoscrittore non trovato")
        return jsonable_encoder(subscriber)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/policy-subscribers")
async def api_create_policy_subscriber(request: PolicySubscriberCreateRequest):
    """Crea un nuovo sottoscrittore"""
    try:
        from modules.db import create_policy_subscriber
        subscriber_data = request.dict()
        subscriber_id = create_policy_subscriber(subscriber_data)
        return jsonable_encoder({"subscriber_id": subscriber_id, "message": "Sottoscrittore creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/policy-subscribers/{subscriber_id}")
async def api_update_policy_subscriber(subscriber_id: int, request: PolicySubscriberUpdateRequest):
    """Aggiorna un sottoscrittore esistente"""
    try:
        from modules.db import update_policy_subscriber
        subscriber_data = request.dict(exclude_unset=True)
        if not subscriber_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_policy_subscriber(subscriber_id, subscriber_data)
        if not success:
            raise HTTPException(status_code=404, detail="Sottoscrittore non trovato")
        
        return jsonable_encoder({"subscriber_id": subscriber_id, "message": "Sottoscrittore aggiornato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/policy-subscribers/{subscriber_id}")
async def api_delete_policy_subscriber(subscriber_id: int):
    """Elimina un sottoscrittore"""
    try:
        from modules.db import delete_policy_subscriber
        success = delete_policy_subscriber(subscriber_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sottoscrittore non trovato")
        
        return jsonable_encoder({"subscriber_id": subscriber_id, "message": "Sottoscrittore eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per delegati pagamento premi
@app.get("/api/v1/premium-delegates")
async def api_get_premium_delegates(client_id: Optional[int] = None):
    """Recupera la lista dei delegati al pagamento"""
    try:
        from modules.db import get_premium_delegates
        if client_id:
            delegates = get_premium_delegates(client_id)
        else:
            # Se non viene specificato client_id, restituiamo un errore
            raise HTTPException(status_code=400, detail="client_id è obbligatorio")
        return jsonable_encoder(delegates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/premium-delegates/{delegate_id}")
async def api_get_premium_delegate(delegate_id: int):
    """Recupera un delegato specifico per ID"""
    try:
        from modules.db import get_premium_delegate
        delegate = get_premium_delegate(delegate_id)
        if not delegate:
            raise HTTPException(status_code=404, detail="Delegato non trovato")
        return jsonable_encoder(delegate)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/premium-delegates")
async def api_create_premium_delegate(request: PremiumDelegateCreateRequest):
    """Crea un nuovo delegato"""
    try:
        from modules.db import create_premium_delegate
        delegate_data = request.dict()
        delegate_id = create_premium_delegate(delegate_data)
        return jsonable_encoder({"delegate_id": delegate_id, "message": "Delegato creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/premium-delegates/{delegate_id}")
async def api_update_premium_delegate(delegate_id: int, request: PremiumDelegateUpdateRequest):
    """Aggiorna un delegato esistente"""
    try:
        from modules.db import update_premium_delegate
        delegate_data = request.dict(exclude_unset=True)
        if not delegate_data:
            raise HTTPException(status_code=400, detail="Nessun dato fornito per l'aggiornamento")
        
        success = update_premium_delegate(delegate_id, delegate_data)
        if not success:
            raise HTTPException(status_code=404, detail="Delegato non trovato")
        
        return jsonable_encoder({"delegate_id": delegate_id, "message": "Delegato aggiornato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/premium-delegates/{delegate_id}")
async def api_delete_premium_delegate(delegate_id: int):
    """Elimina un delegato"""
    try:
        from modules.db import delete_premium_delegate
        success = delete_premium_delegate(delegate_id)
        if not success:
            raise HTTPException(status_code=404, detail="Delegato non trovato")
        
        return jsonable_encoder({"delegate_id": delegate_id, "message": "Delegato eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per clienti
@app.get("/api/v1/clients")
async def api_get_clients(
    name: Optional[str] = None,
    company: Optional[str] = None,
    sector: Optional[str] = None,
    email: Optional[str] = None,
    client_type: Optional[str] = None,
    fiscal_code: Optional[str] = None,
    vat_number: Optional[str] = None,
    city: Optional[str] = None,
    province: Optional[str] = None,
    postal_code: Optional[str] = None,
    country: Optional[str] = None,
    customer_segment: Optional[str] = None,
    customer_status: Optional[str] = None,
    current_user: User = Depends(require_permission("view_clients"))
):
    """Recupera la lista dei clienti con filtri opzionali"""
    try:
        from modules.db import get_clients
        filters = {}
        if name: filters['name'] = name
        if company: filters['company'] = company
        if sector: filters['sector'] = sector
        if email: filters['email'] = email
        if client_type: filters['client_type'] = client_type
        if fiscal_code: filters['fiscal_code'] = fiscal_code
        if vat_number: filters['vat_number'] = vat_number
        if city: filters['city'] = city
        if province: filters['province'] = province
        if postal_code: filters['postal_code'] = postal_code
        if country: filters['country'] = country
        if customer_segment: filters['customer_segment'] = customer_segment
        if customer_status: filters['customer_status'] = customer_status
        
        clients = get_clients(filters)
        return jsonable_encoder(clients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/clients/{client_id}")
async def api_get_client(client_id: int):
    """Recupera un cliente specifico per ID"""
    try:
        from modules.db import get_client
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
        from modules.db import create_client
        client_data = request.dict()
        client_id = create_client(client_data)
        return jsonable_encoder({"client_id": client_id, "message": "Cliente creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/clients/{client_id}")
async def api_update_client(client_id: int, request: ClientUpdateRequest):
    """Aggiorna un cliente esistente"""
    try:
        from modules.db import update_client
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
        from modules.db import delete_client
        success = delete_client(client_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente non trovato")
        
        return jsonable_encoder({"client_id": client_id, "message": "Cliente eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/clients/{client_id}/risks")
async def api_get_client_risks(client_id: int):
    """Recupera tutti i rischi associati a un cliente"""
    try:
        from modules.db import get_client_risks
        risks = get_client_risks(client_id)
        return jsonable_encoder({"risks": risks})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per polizze
@app.get("/api/v1/policies")
async def api_get_policies(
    policy_number: Optional[str] = None,
    company: Optional[str] = None,
    status: Optional[str] = None,
    start_date_from: Optional[date] = None,
    start_date_to: Optional[date] = None,
    end_date_from: Optional[date] = None,
    end_date_to: Optional[date] = None,
    client_id: Optional[int] = None,
    company_id: Optional[int] = None
):
    """Recupera la lista delle polizze con filtri opzionali"""
    try:
        from modules.db import get_policies
        filters = {}
        if policy_number: filters['policy_number'] = policy_number
        if company: filters['company'] = company
        if status: filters['status'] = status
        if start_date_from: filters['start_date_from'] = start_date_from
        if start_date_to: filters['start_date_to'] = start_date_to
        if end_date_from: filters['end_date_from'] = end_date_from
        if end_date_to: filters['end_date_to'] = end_date_to
        if client_id: filters['client_id'] = client_id
        if company_id: filters['company_id'] = company_id
        
        policies = get_policies(filters)
        return jsonable_encoder(policies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/policies/{policy_id}")
async def api_get_policy(policy_id: int):
    """Recupera una polizza specifica per ID"""
    try:
        from modules.db import get_policy
        policy = get_policy(policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Polizza non trovata")
        return jsonable_encoder(policy)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/policies")
async def api_create_policy(request: PolicyCreateRequest):
    """Crea una nuova polizza"""
    try:
        from modules.db import create_policy
        policy_data = request.dict()
        policy_id = create_policy(policy_data)
        return jsonable_encoder({"policy_id": policy_id, "message": "Polizza creata con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/policies/{policy_id}")
async def api_update_policy(policy_id: int, request: PolicyUpdateRequest):
    """Aggiorna una polizza esistente"""
    try:
        from modules.db import update_policy
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
        from modules.db import delete_policy
        success = delete_policy(policy_id)
        if not success:
            raise HTTPException(status_code=404, detail="Polizza non trovata")
        
        return jsonable_encoder({"policy_id": policy_id, "message": "Polizza eliminata con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/risks/{risk_id}/policies")
async def api_get_risk_policies(risk_id: int):
    """Recupera tutte le polizze associate a un rischio"""
    try:
        from modules.db import get_risk_policies
        policies = get_risk_policies(risk_id)
        return jsonable_encoder({"policies": policies})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per sinistri
@app.get("/api/v1/claims")
async def api_get_claims(
    policy_id: Optional[int] = None,
    status: Optional[str] = None,
    claim_date_from: Optional[date] = None,
    claim_date_to: Optional[date] = None,
    amount_from: Optional[float] = None,
    amount_to: Optional[float] = None
):
    """Recupera la lista dei sinistri con filtri opzionali"""
    try:
        from modules.db import get_claims
        filters = {}
        if policy_id: filters['policy_id'] = policy_id
        if status: filters['status'] = status
        if claim_date_from: filters['claim_date_from'] = claim_date_from
        if claim_date_to: filters['claim_date_to'] = claim_date_to
        if amount_from: filters['amount_from'] = amount_from
        if amount_to: filters['amount_to'] = amount_to
        
        claims = get_claims(filters)
        return jsonable_encoder(claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/claims/{claim_id}")
async def api_get_claim(claim_id: int):
    """Recupera un sinistro specifico per ID"""
    try:
        from modules.db import get_claim
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
        from modules.db import create_claim
        claim_data = request.dict()
        claim_id = create_claim(claim_data)
        return jsonable_encoder({"claim_id": claim_id, "message": "Sinistro creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/claims/{claim_id}")
async def api_update_claim(claim_id: int, request: ClaimUpdateRequest):
    """Aggiorna un sinistro esistente"""
    try:
        from modules.db import update_claim
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
        from modules.db import delete_claim
        success = delete_claim(claim_id)
        if not success:
            raise HTTPException(status_code=404, detail="Sinistro non trovato")
        
        return jsonable_encoder({"claim_id": claim_id, "message": "Sinistro eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per analisi portafoglio
@app.get("/api/v1/insurance/portfolio-analytics")
async def api_get_portfolio_analytics(company_id: Optional[int] = None):
    """Recupera l'analisi del portafoglio assicurativo"""
    try:
        from modules.dashboard_analytics import get_portfolio_analytics
        analytics = get_portfolio_analytics(company_id)
        return jsonable_encoder(analytics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per performance compagnia
@app.get("/api/v1/insurance/company-performance")
async def api_get_company_performance(company_id: int):
    """Recupera le performance di una compagnia assicurativa"""
    try:
        from modules.dashboard_analytics import get_company_performance
        performance = get_company_performance(company_id)
        return jsonable_encoder(performance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per metriche broker
@app.get("/api/v1/insurance/broker-metrics")
async def api_get_broker_metrics(broker_id: int):
    """Recupera le metriche di performance di un broker"""
    try:
        from modules.dashboard_analytics import get_broker_performance
        metrics = get_broker_performance(broker_id)
        return jsonable_encoder(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per report compliance
@app.post("/api/v1/insurance/compliance-report")
async def api_generate_compliance_report(request: ComplianceReportRequest):
    """Genera un report di compliance"""
    try:
        from modules.compliance_reporting import generate_compliance_report
        report_data = request.dict()
        report = generate_compliance_report(
            report_data["report_type"],
            report_data["period_start"],
            report_data["period_end"]
        )
        return jsonable_encoder(report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/insurance/compliance-reports")
async def api_get_compliance_reports(report_type: str = None):
    """Recupera i report di compliance esistenti"""
    try:
        from modules.compliance_reporting import get_compliance_reports
        reports = get_compliance_reports(report_type)
        return jsonable_encoder({"reports": reports})
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

# Endpoint per rischi
@app.get("/api/v1/risks")
async def api_get_risks(risk_type: str = None, client_id: int = None):
    """Recupera la lista dei rischi con filtri opzionali"""
    try:
        from modules.db import get_risks
        filters = {}
        if risk_type:
            filters['risk_type'] = risk_type
        if client_id:
            filters['client_id'] = client_id
        
        risks = get_risks(filters)
        return jsonable_encoder({"risks": risks})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/risks/{risk_id}")
async def api_get_risk(risk_id: int):
    """Recupera un rischio specifico per ID"""
    try:
        from modules.db import get_risk
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
        from modules.db import create_risk
        risk_data = request.dict()
        risk_id = create_risk(risk_data)
        return jsonable_encoder({"risk_id": risk_id, "message": "Rischio creato con successo"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/risks/{risk_id}")
async def api_update_risk(risk_id: int, request: RiskUpdateRequest):
    """Aggiorna un rischio esistente"""
    try:
        from modules.db import update_risk
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
        from modules.db import delete_risk
        success = delete_risk(risk_id)
        if not success:
            raise HTTPException(status_code=404, detail="Rischio non trovato")
        
        return jsonable_encoder({"risk_id": risk_id, "message": "Rischio eliminato con successo"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))