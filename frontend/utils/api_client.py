import requests
import json
from typing import Dict, Any, List, Optional
from decimal import Decimal
import os

class APIClient:
    """Client API per comunicare con il backend BrokerFlow AI"""
    
    def __init__(self):
        # URL base dell'API - può essere sovrascritto da variabile d'ambiente
        self.base_url = os.getenv("API_BASE_URL", "http://api:8000/api/v1")
        
    def _serialize_decimal(self, obj):
        """Serializza oggetti Decimal per JSON"""
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Effettua una richiesta HTTP all'API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise Exception(f"API Error: {error_detail.get('detail', str(e))}")
                except:
                    raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            else:
                raise Exception(f"Connection Error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON Decode Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")
    
    # === METODI PER CLIENTI ===
    
    def get_clients(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Recupera la lista dei clienti"""
        # Pulisci i filtri rimuovendo valori vuoti o None
        if filters:
            clean_filters = {k: v for k, v in filters.items() if v not in [None, "", [], {}]}
            # Gestisci i filtri booleani per i pulsanti
            if 'apply' in clean_filters:
                del clean_filters['apply']
            if 'clear' in clean_filters:
                del clean_filters['clear']
            return self._make_request("GET", "/clients", params=clean_filters)
        return self._make_request("GET", "/clients")
    
    def get_client(self, client_id: int) -> Dict[str, Any]:
        """Recupera i dettagli di un cliente specifico"""
        return self._make_request("GET", f"/clients/{client_id}")
    
    def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo cliente"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(client_data, default=self._serialize_decimal))
        return self._make_request("POST", "/clients", json=serialized_data)
    
    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un cliente esistente"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(client_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/clients/{client_id}", json=serialized_data)
    
    def delete_client(self, client_id: int) -> Dict[str, Any]:
        """Elimina un cliente"""
        return self._make_request("DELETE", f"/clients/{client_id}")
    
    # === METODI PER POLIZZE ===
    
    def get_policies(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Recupera la lista delle polizze"""
        # Pulisci i filtri rimuovendo valori vuoti o None
        if filters:
            clean_filters = {k: v for k, v in filters.items() if v not in [None, "", [], {}]}
            # Gestisci i filtri booleani per i pulsanti
            if 'apply' in clean_filters:
                del clean_filters['apply']
            if 'clear' in clean_filters:
                del clean_filters['clear']
            return self._make_request("GET", "/policies", params=clean_filters)
        return self._make_request("GET", "/policies")
    
    def get_policy(self, policy_id: int) -> Dict[str, Any]:
        """Recupera i dettagli di una polizza specifica"""
        return self._make_request("GET", f"/policies/{policy_id}")
    
    def create_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nuova polizza"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(policy_data, default=self._serialize_decimal))
        return self._make_request("POST", "/policies", json=serialized_data)
    
    def update_policy(self, policy_id: int, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna una polizza esistente"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(policy_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/policies/{policy_id}", json=serialized_data)
    
    def delete_policy(self, policy_id: int) -> Dict[str, Any]:
        """Elimina una polizza"""
        return self._make_request("DELETE", f"/policies/{policy_id}")
    
    # === METODI PER SINISTRI ===
    
    def get_claims(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Recupera la lista dei sinistri"""
        # Pulisci i filtri rimuovendo valori vuoti o None
        if filters:
            clean_filters = {k: v for k, v in filters.items() if v not in [None, "", [], {}]}
            # Gestisci i filtri booleani per i pulsanti
            if 'apply' in clean_filters:
                del clean_filters['apply']
            if 'clear' in clean_filters:
                del clean_filters['clear']
            return self._make_request("GET", "/claims", params=clean_filters)
        return self._make_request("GET", "/claims")
    
    def get_claim(self, claim_id: int) -> Dict[str, Any]:
        """Recupera i dettagli di un sinistro specifico"""
        return self._make_request("GET", f"/claims/{claim_id}")
    
    def create_claim(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo sinistro"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(claim_data, default=self._serialize_decimal))
        return self._make_request("POST", "/claims", json=serialized_data)
    
    def update_claim(self, claim_id: int, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un sinistro esistente"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(claim_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/claims/{claim_id}", json=serialized_data)
    
    def delete_claim(self, claim_id: int) -> Dict[str, Any]:
        """Elimina un sinistro"""
        return self._make_request("DELETE", f"/claims/{claim_id}")

    # === METODI PER DOCUMENTI SINISTRI ===
    
    def get_claim_documents(self, claim_id: int) -> List[Dict[str, Any]]:
        """Recupera i documenti associati a un sinistro"""
        return self._make_request("GET", f"/claims/{claim_id}/documents")
    
    def create_claim_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo documento per un sinistro"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(document_data, default=self._serialize_decimal))
        return self._make_request("POST", "/claim-documents", json=serialized_data)
    
    def delete_claim_document(self, document_id: int) -> Dict[str, Any]:
        """Elimina un documento di sinistro"""
        return self._make_request("DELETE", f"/claim-documents/{document_id}")

    # === METODI PER COMUNICAZIONI SINISTRI ===
    
    def get_claim_communications(self, claim_id: int) -> List[Dict[str, Any]]:
        """Recupera le comunicazioni associate a un sinistro"""
        return self._make_request("GET", f"/claims/{claim_id}/communications")
    
    def create_claim_communication(self, communication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nuova comunicazione per un sinistro"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(communication_data, default=self._serialize_decimal))
        return self._make_request("POST", "/claim-communications", json=serialized_data)
    
    def update_claim_communication(self, communication_id: int, communication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna una comunicazione di sinistro"""
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(communication_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/claim-communications/{communication_id}", json=serialized_data)
    
    # === METODI PER ANALISI E DASHBOARD ===
    
    def analyze_risk(self, client_id: int) -> Dict[str, Any]:
        """Effettua l'analisi del rischio per un cliente"""
        data = {"client_id": client_id}
        return self._make_request("POST", "/insurance/risk-analysis", json=data)
    
    def get_portfolio_analytics(self, company_id: Optional[int] = None) -> Dict[str, Any]:
        """Recupera le analisi del portafoglio"""
        params = {"company_id": company_id} if company_id else {}
        return self._make_request("GET", "/insurance/portfolio-analytics", params=params)
    
    def get_company_performance(self, company_id: int) -> Dict[str, Any]:
        """Recupera le performance di una compagnia assicurativa"""
        return self._make_request("GET", f"/insurance/company-performance?company_id={company_id}")
    
    def get_broker_metrics(self, broker_id: int) -> Dict[str, Any]:
        """Recupera le metriche di performance di un broker"""
        return self._make_request("GET", f"/insurance/broker-metrics?broker_id={broker_id}")
    
    # === METODI PER COMPLIANCE ===
    
    def generate_compliance_report(self, report_type: str, period_start: str, period_end: str) -> Dict[str, Any]:
        """Genera un report di compliance"""
        data = {
            "report_type": report_type,
            "period_start": period_start,
            "period_end": period_end
        }
        return self._make_request("POST", "/insurance/compliance-report", json=data)
    
    def get_compliance_reports(self, report_type: Optional[str] = None) -> Dict[str, Any]:
        """Recupera i report di compliance"""
        params = {"report_type": report_type} if report_type else {}
        return self._make_request("GET", "/insurance/compliance-reports", params=params)
    
    # === METODI PER SCONTI E PROGRAMMI FEDALTÀ ===
    
    def create_discount(self, company_id: int, broker_id: int, discount_type: str, 
                       percentage: float, start_date: str, end_date: str) -> Dict[str, Any]:
        """Crea un nuovo sconto/convenzione"""
        data = {
            "company_id": company_id,
            "broker_id": broker_id,
            "discount_type": discount_type,
            "percentage": percentage,
            "start_date": start_date,
            "end_date": end_date
        }
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(data, default=self._serialize_decimal))
        return self._make_request("POST", "/insurance/discounts", json=serialized_data)
    
    def get_discounts(self, company_id: Optional[int] = None, broker_id: Optional[int] = None) -> Dict[str, Any]:
        """Recupera i sconti attivi"""
        params = {}
        if company_id:
            params["company_id"] = company_id
        if broker_id:
            params["broker_id"] = broker_id
        return self._make_request("GET", "/insurance/discounts", params=params)
    
    def calculate_discounted_premium(self, base_premium: float, company_id: int, broker_id: int) -> Dict[str, Any]:
        """Calcola il premio scontato"""
        params = {
            "base_premium": base_premium,
            "company_id": company_id,
            "broker_id": broker_id
        }
        return self._make_request("GET", "/insurance/discounted-premium", params=params)
    
    # === METODI DI SISTEMA ===
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Recupera le metriche di sistema"""
        return self._make_request("GET", "/metrics")
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica lo stato di salute del sistema"""
        return self._make_request("GET", "/health")

# Istanza singleton del client API
api_client = APIClient()