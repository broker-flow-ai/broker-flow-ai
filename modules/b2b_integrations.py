import requests
import json
from modules.db import get_db_connection

# Simulazione di integrazioni con sistemi esterni

def integrate_with_sga_system(policy_data, sga_credentials):
    """
    Integra con sistemi gestionali assicurativi
    """
    try:
        # URL dell'API del SGA (simulato)
        sga_api_url = sga_credentials.get('api_url', 'https://sga.example.com/api/v1')
        api_key = sga_credentials.get('api_key')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Prepara i dati per l'invio al SGA
        sga_data = {
            "policy_number": policy_data.get('policy_number'),
            "client": {
                "name": policy_data.get('client_name'),
                "company": policy_data.get('client_company'),
                "email": policy_data.get('client_email')
            },
            "risk": {
                "type": policy_data.get('risk_type'),
                "details": policy_data.get('risk_details')
            },
            "premium": policy_data.get('premium_amount'),
            "coverages": policy_data.get('coverages')
        }
        
        # Invia i dati al SGA
        response = requests.post(
            f"{sga_api_url}/policies",
            headers=headers,
            json=sga_data,
            timeout=30
        )
        
        if response.status_code == 201:
            return {
                "success": True,
                "sga_policy_id": response.json().get('policy_id'),
                "message": "Polizza registrata con successo nel SGA"
            }
        else:
            return {
                "success": False,
                "error": f"Errore SGA: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Integrazione SGA fallita: {str(e)}"
        }

def sync_with_broker_portal(policy_data, portal_credentials):
    """
    Sincronizza con portali broker
    """
    try:
        portal_url = portal_credentials.get('portal_url')
        username = portal_credentials.get('username')
        password = portal_credentials.get('password')
        
        # Login al portale (simulato)
        login_data = {
            "username": username,
            "password": password
        }
        
        login_response = requests.post(
            f"{portal_url}/login",
            json=login_data
        )
        
        if login_response.status_code != 200:
            return {
                "success": False,
                "error": "Autenticazione al portale fallita"
            }
        
        # Recupera token di sessione
        session_token = login_response.json().get('token')
        
        # Invia polizza al portale
        headers = {
            'Authorization': f'Bearer {session_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{portal_url}/policies",
            headers=headers,
            json=policy_data
        )
        
        if response.status_code == 201:
            return {
                "success": True,
                "portal_policy_id": response.json().get('policy_id'),
                "message": "Polizza sincronizzata con il portale broker"
            }
        else:
            return {
                "success": False,
                "error": f"Errore portale: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Sincronizzazione portale fallita: {str(e)}"
        }

def process_payment(payment_data, payment_gateway):
    """
    Processa pagamenti attraverso gateway di pagamento
    """
    try:
        gateway_url = payment_gateway.get('url')
        api_key = payment_gateway.get('api_key')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{gateway_url}/payments",
            headers=headers,
            json=payment_data
        )
        
        if response.status_code == 200:
            payment_result = response.json()
            return {
                "success": True,
                "transaction_id": payment_result.get('transaction_id'),
                "status": payment_result.get('status'),
                "amount": payment_result.get('amount')
            }
        else:
            return {
                "success": False,
                "error": f"Pagamento fallito: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Processamento pagamento fallito: {str(e)}"
        }

def get_sga_policy_status(policy_number, sga_credentials):
    """
    Recupera lo stato di una polizza dal SGA
    """
    try:
        sga_api_url = sga_credentials.get('api_url')
        api_key = sga_credentials.get('api_key')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{sga_api_url}/policies/{policy_number}",
            headers=headers
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "policy_data": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"Errore recupero stato: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Recupero stato SGA fallito: {str(e)}"
        }