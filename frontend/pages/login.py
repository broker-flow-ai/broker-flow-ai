import streamlit as st
import sys
import os
import base64
import json
from typing import Optional, Dict, Any

# Aggiungi il path per gli import relativi
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.api_client import api_client
from utils.cookie_manager import CookieManager

def decode_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodifica un token JWT per ottenere le informazioni dell'utente"""
    try:
        # Il token JWT è formato da tre parti separate da punti: header.payload.signature
        token_parts = token.split('.')
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

def login_page():
    st.title("🔐 Accesso BrokerFlow AI")
    
    # Inizializza lo stato della sessione
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'show_2fa' not in st.session_state:
        st.session_state.show_2fa = False
    if 'username_2fa' not in st.session_state:
        st.session_state.username_2fa = None
    if 'temp_password' not in st.session_state:
        st.session_state.temp_password = None
    
    # Se l'utente è già autenticato, mostriamo un messaggio
    if st.session_state.authenticated:
        st.success(f"Sei già autenticato come {st.session_state.user.get('username', 'utente')}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.show_2fa = False
            st.session_state.username_2fa = None
            st.session_state.temp_password = None
            api_client.logout()
            
            # Clear the auth data from URL parameters
            cookie_manager = CookieManager()
            cookie_manager.clear_auth_cookie()
            
            st.rerun()
        return
    
    # Form di login
    if not st.session_state.show_2fa:
        with st.form("login_form"):
            st.subheader("Accedi al sistema")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            submitted = st.form_submit_button("Accedi")
            
            if submitted:
                if not username or not password:
                    st.error("Per favore inserisci username e password")
                else:
                    try:
                        # Tentativo di login
                        result = api_client.login(username, password)
                        
                        # Se il login ha successo, otteniamo il token
                        if result and "access_token" in result:
                            # Decodifica il token per ottenere il ruolo
                            user_info = decode_jwt_token(result["access_token"])
                            if user_info:
                                st.session_state.authenticated = True
                                st.session_state.user = user_info
                                # Salva il token nell'API client
                                api_client.access_token = result["access_token"]
                                
                                # Salva i dati di autenticazione nei parametri URL
                                cookie_manager = CookieManager()
                                cookie_manager.save_auth_cookie(result["access_token"], user_info)
                                
                                st.success("Accesso effettuato con successo!")
                                st.rerun()
                            else:
                                st.error("Errore nel recupero delle informazioni utente")
                        else:
                            st.error("Credenziali non valide")
                    except Exception as e:
                        # Gestione del 2FA
                        error_message = str(e)
                        if "2FA_REQUIRED" in error_message:
                            st.session_state.show_2fa = True
                            st.session_state.username_2fa = username
                            st.session_state.temp_password = password
                            st.info("🔒 Autenticazione a due fattori richiesta")
                            st.info("📧 Controlla la tua email per il codice OTP")
                            st.rerun()
                        else:
                            st.error(f"Errore durante il login: {str(e)}")
                            st.info("🔧 Verifica che il servizio API sia attivo e raggiungibile")
    
    # Form 2FA
    if st.session_state.show_2fa:
        st.subheader("🔐 Verifica a Due Fattori")
        st.info(f"📧 Codice OTP inviato all'email associata all'utente {st.session_state.username_2fa}")
        
        with st.form("2fa_form"):
            token = st.text_input("Codice OTP (6 cifre)", key="2fa_token", max_chars=6, placeholder="123456")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted_2fa = st.form_submit_button("✅ Verifica Codice", type="primary")
            with col2:
                if st.form_submit_button("🔄 Invia Nuovo Codice"):
                    try:
                        # Richiedi un nuovo codice OTP
                        api_client._make_request("POST", "/auth/two-factor/request", json={
                            "username": st.session_state.username_2fa,
                            "password": st.session_state.temp_password
                        })
                        st.info("📤 Nuovo codice OTP inviato all'email")
                    except Exception as e:
                        st.error(f"Errore nell'invio del codice: {str(e)}")
            
            if submitted_2fa:
                if not token:
                    st.error("Per favore inserisci il codice OTP")
                else:
                    try:
                        result = api_client._make_request("POST", "/auth/two-factor/verify", json={
                            "username": st.session_state.username_2fa,
                            "token": token
                        })
                        
                        if "access_token" in result:
                            st.session_state.authenticated = True
                            # Decodifica il token per ottenere il ruolo
                            user_info = decode_jwt_token(result["access_token"])
                            if user_info:
                                st.session_state.user = user_info
                            else:
                                st.session_state.user = {"username": st.session_state.username_2fa, "role": "viewer"}
                            # Salva il token nell'API client
                            api_client.access_token = result["access_token"]
                            
                            # Salva i dati di autenticazione nei parametri URL
                            cookie_manager = CookieManager()
                            cookie_manager.save_auth_cookie(result["access_token"], st.session_state.user)
                            
                            st.session_state.show_2fa = False
                            st.session_state.username_2fa = None
                            st.session_state.temp_password = None
                            st.success("🎉 Accesso effettuato con successo!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Codice OTP non valido o scaduto")
                    except Exception as e:
                        st.error(f"Errore nella verifica OTP: {str(e)}")
        
        # Opzione per tornare al login
        if st.button("🔙 Torna al login"):
            st.session_state.show_2fa = False
            st.session_state.username_2fa = None
            st.session_state.temp_password = None
            st.rerun()

if __name__ == "__main__":
    login_page()