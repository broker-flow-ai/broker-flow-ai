import requests
import json
from typing import Dict, Any, List, Optional
from decimal import Decimal
from datetime import date, datetime
import os

class APIClient:
    """Client API per comunicare con il backend BrokerFlow AI"""
    
    def __init__(self):
        # URL base dell'API - può essere sovrascritto da variabile d'ambiente
        self.base_url = os.getenv("API_BASE_URL", "http://api:8000/api/v1")
        self.access_token = None
        
    def _serialize_decimal(self, obj):
        """Serializza oggetti Decimal e date per JSON"""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (date, datetime)):  # Gestisce esplicitamente date e datetime
            return obj.isoformat()
        elif hasattr(obj, 'isoformat'):  # Gestisce altri oggetti con isoformat
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Effettua una richiesta HTTP all'API"""
        url = f"{self.base_url}{endpoint}"
        
        # Aggiungi il token di autorizzazione se disponibile
        if self.access_token:
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f"Bearer {self.access_token}"
        
        try:
            response = requests.request(method, url, **kwargs)
            
            # Gestione speciale per il 2FA - anche con status 200 può richiedere 2FA
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and response_data.get("detail") == "2FA_REQUIRED":
                        raise Exception("2FA_REQUIRED")
                except json.JSONDecodeError:
                    pass  # Non è JSON, procedi normalmente
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error making request to {url}: {str(e)}")
            raise Exception(f"Connection Error: Impossibile connettersi all'API. Verifica che il servizio API sia attivo.")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error making request to {url}: {str(e)}")
            raise Exception(f"Timeout Error: La richiesta all'API ha impiegato troppo tempo.")
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    # Gestione speciale per il 2FA
                    if isinstance(error_detail, dict) and error_detail.get("detail") == "2FA_REQUIRED":
                        raise Exception("2FA_REQUIRED")
                    raise Exception(f"API Error: {error_detail.get('detail', str(e))}")
                except:
                    raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            else:
                raise Exception(f"Request Error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON Decode Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected Error: {str(e)}")
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Effettua il login e ottiene il token di accesso"""
        try:
            response = self._make_request("POST", "/auth/token", data={
                "username": username,
                "password": password
            })
            if "access_token" in response:
                self.access_token = response["access_token"]
                return response
            return None
        except Exception as e:
            if "2FA_REQUIRED" in str(e):
                raise Exception("2FA_REQUIRED")
            print(f"Login error: {str(e)}")
            return None
    
    def logout(self):
        """Effettua il logout"""
        self.access_token = None
    
    def is_authenticated(self) -> bool:
        """Verifica se l'utente è autenticato"""
        return self.access_token is not None
    
    def get_current_user_info(self) -> Optional[Dict[str, Any]]:
        """Ottiene le informazioni dell'utente corrente dal token JWT"""
        if not self.access_token:
            return None
        
        try:
            # Decodifica il token JWT per ottenere le informazioni dell'utente
            import base64
            import json
            
            # Il token JWT è formato da tre parti separate da punti: header.payload.signature
            token_parts = self.access_token.split('.')
            if len(token_parts) != 3:
                return None
                
            # Decodifica la parte payload (seconda parte)
            payload = token_parts[1]
            
            # Aggiungi padding se necessario
            padding = 4 - len(payload) % 4
            if padding:
                payload += '=' * padding
                
            # Decodifica base64
            decoded_payload = base64.urlsafe_b64decode(payload)
            payload_data = json.loads(decoded_payload)
            
            return {
                "username": payload_data.get("sub"),
                "role": payload_data.get("role")
            }
        except Exception as e:
            print(f"Error decoding JWT token: {str(e)}")
            return None
    
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
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(client_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/clients", json=serialized_data)
    
    def update_client(self, client_id: int, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un cliente esistente"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(client_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/clients/{client_id}", json=serialized_data)
    
    def _process_date_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa i campi data per convertirli in stringhe ISO"""
        processed_data = data.copy()
        date_fields = ['birth_date', 'establishment_date', 'start_date', 'end_date', 'subscription_date', 'claim_date']
        
        for field in date_fields:
            if field in processed_data and processed_data[field] is not None:
                if isinstance(processed_data[field], (date, datetime)):
                    processed_data[field] = processed_data[field].isoformat()
                elif isinstance(processed_data[field], str):
                    # Se è già una stringa, la lasciamo così
                    pass
                else:
                    # Se è un altro tipo, lo convertiamo in stringa
                    processed_data[field] = str(processed_data[field])
        
        return processed_data
    
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
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(policy_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/policies", json=serialized_data)
    
    def update_policy(self, policy_id: int, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna una polizza esistente"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(policy_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
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
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(claim_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/claims", json=serialized_data)
    
    def update_claim(self, claim_id: int, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un sinistro esistente"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(claim_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
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
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(document_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
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
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(communication_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/claim-communications", json=serialized_data)
    
    def update_claim_communication(self, communication_id: int, communication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna una comunicazione di sinistro"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(communication_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
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

    # === METODI PER RELAZIONI CLIENTI-RISCHI-POLIZZE-SINISTRI ===
    
    def get_client_risks(self, client_id: int) -> List[Dict[str, Any]]:
        """Recupera i rischi associati a un cliente"""
        try:
            response = self._make_request('GET', f'/clients/{client_id}/risks')
            return response.get('risks', []) if isinstance(response, dict) else response
        except Exception as e:
            print(f"Errore nel recupero dei rischi del cliente {client_id}: {str(e)}")
            return []

    def get_risk_policies(self, risk_id: int) -> List[Dict[str, Any]]:
        """Recupera le polizze associate a un rischio"""
        try:
            response = self._make_request('GET', f'/risks/{risk_id}/policies')
            return response.get('policies', []) if isinstance(response, dict) else response
        except Exception as e:
            print(f"Errore nel recupero delle polizze del rischio {risk_id}: {str(e)}")
            return []

    def get_policy_claims(self, policy_id: int) -> List[Dict[str, Any]]:
        """Recupera i sinistri associati a una polizza"""
        try:
            response = self._make_request('GET', f'/policies/{policy_id}/claims')
            return response.get('claims', []) if isinstance(response, dict) else response
        except Exception as e:
            print(f"Errore nel recupero dei sinistri della polizza {policy_id}: {str(e)}")
            return []

    def get_policy_premiums(self, policy_id: int) -> List[Dict[str, Any]]:
        """Recupera i premi associati a una polizza"""
        try:
            response = self._make_request('GET', f'/policies/{policy_id}/premiums')
            return response.get('premiums', []) if isinstance(response, dict) else response
        except Exception as e:
            print(f"Errore nel recupero dei premi della polizza {policy_id}: {str(e)}")
            return []

    def get_risks(self) -> List[Dict[str, Any]]:
        """Recupera la lista dei rischi"""
        try:
            response = self._make_request('GET', '/risks')
            return response.get('risks', []) if isinstance(response, dict) else response
        except Exception as e:
            print(f"Errore nel recupero dei rischi: {str(e)}")
            return []

    def get_risk(self, risk_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un rischio specifico per ID"""
        try:
            response = self._make_request('GET', f'/risks/{risk_id}')
            return response
        except Exception as e:
            print(f"Errore nel recupero del rischio {risk_id}: {str(e)}")
            return None

    def create_risk(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo rischio"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(risk_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/risks", json=serialized_data)

    # === METODI PER SOTTOSCRITTORI POLIZZE ===
    
    def get_policy_subscribers(self, policy_id: int) -> List[Dict[str, Any]]:
        """Recupera i sottoscrittori associati a una polizza"""
        try:
            response = self._make_request('GET', '/policy-subscribers', params={'policy_id': policy_id})
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Errore nel recupero dei sottoscrittori della polizza {policy_id}: {str(e)}")
            return []

    def get_policy_subscriber(self, subscriber_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un sottoscrittore specifico per ID"""
        try:
            response = self._make_request('GET', f'/policy-subscribers/{subscriber_id}')
            return response
        except Exception as e:
            print(f"Errore nel recupero del sottoscrittore {subscriber_id}: {str(e)}")
            return None

    def create_policy_subscriber(self, subscriber_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo sottoscrittore"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(subscriber_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/policy-subscribers", json=serialized_data)

    def update_policy_subscriber(self, subscriber_id: int, subscriber_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un sottoscrittore esistente"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(subscriber_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/policy-subscribers/{subscriber_id}", json=serialized_data)

    def delete_policy_subscriber(self, subscriber_id: int) -> Dict[str, Any]:
        """Elimina un sottoscrittore"""
        return self._make_request("DELETE", f"/policy-subscribers/{subscriber_id}")

    # === METODI PER DELEGATI PAGAMENTO PREMI ===
    
    def get_premium_delegates(self, client_id: int) -> List[Dict[str, Any]]:
        """Recupera i delegati al pagamento associati a un cliente"""
        try:
            response = self._make_request('GET', '/premium-delegates', params={'client_id': client_id})
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Errore nel recupero dei delegati del cliente {client_id}: {str(e)}")
            return []

    def get_premium_delegate(self, delegate_id: int) -> Optional[Dict[str, Any]]:
        """Recupera un delegato specifico per ID"""
        try:
            response = self._make_request('GET', f'/premium-delegates/{delegate_id}')
            return response
        except Exception as e:
            print(f"Errore nel recupero del delegato {delegate_id}: {str(e)}")
            return None

    def create_premium_delegate(self, delegate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuovo delegato"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(delegate_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("POST", "/premium-delegates", json=serialized_data)

    def update_premium_delegate(self, delegate_id: int, delegate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiorna un delegato esistente"""
        # Pre-processa i dati per convertire le date in stringhe
        processed_data = self._process_date_fields(delegate_data)
        # Converti Decimal in float per la serializzazione
        serialized_data = json.loads(json.dumps(processed_data, default=self._serialize_decimal))
        return self._make_request("PUT", f"/premium-delegates/{delegate_id}", json=serialized_data)

    def delete_premium_delegate(self, delegate_id: int) -> Dict[str, Any]:
        """Elimina un delegato"""
        return self._make_request("DELETE", f"/premium-delegates/{delegate_id}")

# Istanza singleton del client API
api_client = APIClient()