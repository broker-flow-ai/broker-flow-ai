import streamlit as st
import sys
import os

# Aggiungi il path per gli import relativi
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.api_client import api_client

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
    
    # Se l'utente è già autenticato, mostriamo un messaggio
    if st.session_state.authenticated:
        st.success(f"Sei già autenticato come {st.session_state.user.get('username', 'utente')}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.show_2fa = False
            st.session_state.username_2fa = None
            api_client.logout()
            st.rerun()  # Cambiato da experimental_rerun a rerun
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
                            st.session_state.authenticated = True
                            st.session_state.user = {"username": username}
                            st.success("Accesso effettuato con successo!")
                            st.rerun()  # Cambiato da experimental_rerun a rerun
                        else:
                            st.error("Credenziali non valide")
                    except Exception as e:
                        st.error(f"Errore durante il login: {str(e)}")
                        st.info("Verifica che il servizio API sia attivo e raggiungibile")
    
    # Form 2FA
    if st.session_state.show_2fa:
        with st.form("2fa_form"):
            st.subheader("Verifica a Due Fattori")
            st.info(f"Codice inviato all'email associata all'utente {st.session_state.username_2fa}")
            token = st.text_input("Codice 2FA", key="2fa_token", max_chars=6)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted_2fa = st.form_submit_button("Verifica")
            with col2:
                if st.form_submit_button("Invia nuovo codice"):
                    try:
                        # Questo endpoint va implementato nell'API auth
                        st.info("Funzionalità di invio nuovo codice in fase di implementazione")
                    except Exception as e:
                        st.error(f"Errore nell'invio del codice: {str(e)}")
            
            if submitted_2fa:
                if not token:
                    st.error("Per favore inserisci il codice 2FA")
                else:
                    try:
                        # Questo endpoint va implementato nell'API auth
                        st.info("Funzionalità di verifica 2FA in fase di implementazione")
                    except Exception as e:
                        st.error(f"Errore nella verifica 2FA: {str(e)}")
        
        # Opzione per tornare al login
        if st.button("Torna al login"):
            st.session_state.show_2fa = False
            st.session_state.username_2fa = None
            st.rerun()  # Cambiato da experimental_rerun a rerun

if __name__ == "__main__":
    login_page()