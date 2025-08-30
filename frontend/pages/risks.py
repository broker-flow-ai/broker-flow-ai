import streamlit as st
import pandas as pd
import sys
import os
import json

# Aggiungi il path per gli import relativi
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.api_client import api_client
from utils.auth_decorator import require_role

@require_role(allowed_roles=["admin", "broker", "underwriter"])
def risks_page():
    st.title("🛡️ Gestione Rischi")
    
    # Tabs per diverse operazioni
    tab1, tab2, tab3 = st.tabs(["📋 Elenco Rischi", "➕ Nuovo Rischio", "🔍 Dettagli Rischio"])
    
    with tab1:
        st.subheader("Elenco Rischi")
        
        # Filtri
        col1, col2 = st.columns(2)
        with col1:
            risk_type_filter = st.selectbox("Tipo Rischio", ["", "Auto", "Casa", "Salute", "Viaggio", "Attività Professionale"])
        with col2:
            client_filter = st.text_input("Cliente (nome o azienda)")
        
        # Recupera i rischi
        try:
            risks = api_client.get_risks()
            if risks:
                # Applica filtri
                if risk_type_filter:
                    risks = [r for r in risks if r.get('risk_type') == risk_type_filter]
                
                if client_filter:
                    risks = [r for r in risks if client_filter.lower() in (r.get('client_name', '') or '').lower() or client_filter.lower() in (r.get('client_company', '') or '').lower()]
                
                if risks:
                    # Converti in DataFrame per visualizzazione
                    df = pd.DataFrame(risks)
                    
                    # Seleziona colonne da mostrare
                    display_columns = ['id', 'client_name', 'client_company', 'risk_type', 'created_at']
                    df_display = df[display_columns].rename(columns={
                        'id': 'ID',
                        'client_name': 'Cliente',
                        'client_company': 'Azienda',
                        'risk_type': 'Tipo Rischio',
                        'created_at': 'Creato il'
                    })
                    
                    # Mostra la tabella
                    st.dataframe(df_display, use_container_width=True)
                    
                    # Seleziona un rischio per visualizzare dettagli
                    selected_risk_id = st.selectbox("Seleziona un rischio per visualizzare dettagli", 
                                                   [r['id'] for r in risks], 
                                                   format_func=lambda x: f"Rischio {x}")
                    
                    if selected_risk_id:
                        selected_risk = next((r for r in risks if r['id'] == selected_risk_id), None)
                        if selected_risk:
                            st.subheader(f"Dettagli Rischio {selected_risk_id}")
                            st.json(selected_risk)
                else:
                    st.info("Nessun rischio trovato con i filtri selezionati")
            else:
                st.info("Nessun rischio disponibile")
        except Exception as e:
            st.error(f"Errore nel recupero dei rischi: {str(e)}")
    
    with tab2:
        st.subheader("Nuovo Rischio")
        
        # Prima, otteniamo la lista dei clienti per una selezione più user-friendly
        try:
            clients = api_client.get_clients()
            if clients:
                # Crea un dizionario per la selezione con nome descrittivo
                client_options = {}
                client_names = []
                for client in clients:
                    # Crea un nome descrittivo per il cliente
                    if client.get('company'):
                        client_name = f"{client['company']} (ID: {client['id']})"
                        client_options[client_name] = client['id']
                        client_names.append(client_name)
                    else:
                        client_name = f"{client.get('name', 'N/A')} (ID: {client['id']})"
                        client_options[client_name] = client['id']
                        client_names.append(client_name)
                
                # Form per creare un nuovo rischio
                with st.form("new_risk_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        selected_client_name = st.selectbox("Seleziona Cliente", options=client_names)
                        client_id = client_options[selected_client_name] if selected_client_name else None
                        risk_type = st.selectbox("Tipo Rischio", ["Auto", "Casa", "Salute", "Viaggio", "Attività Professionale"])
                    with col2:
                        st.write("### Dettagli Rischio")
                        # Campi per i dettagli del rischio
                        coverage_limit = st.number_input("Limite di Copertura (€)", min_value=0.0, value=100000.0, step=1000.0)
                        deductible = st.number_input("Franchigia (€)", min_value=0.0, value=500.0, step=100.0)
                        description = st.text_area("Descrizione", "Descrizione del rischio")
                    
                    submitted = st.form_submit_button("Crea Rischio")
                    
                    if submitted and client_id:
                        try:
                            # Prepara i dati per la creazione
                            risk_data = {
                                "client_id": client_id,
                                "risk_type": risk_type,
                                "details": {
                                    "description": description,
                                    "coverage_limit": coverage_limit,
                                    "deductible": deductible
                                }
                            }
                            
                            # Crea il rischio
                            result = api_client.create_risk(risk_data)
                            if result and "risk_id" in result:
                                st.success(f"Rischio creato con successo! ID: {result['risk_id']}")
                                st.balloons()
                                st.rerun()  # Cambiato da experimental_rerun a rerun
                            else:
                                st.error("Errore nella creazione del rischio")
                        except Exception as e:
                            st.error(f"Errore nella creazione del rischio: {str(e)}")
                    elif submitted:
                        st.warning("Per favore seleziona un cliente")
            else:
                st.warning("Nessun cliente disponibile. È necessario creare prima un cliente.")
        except Exception as e:
            st.error(f"Errore nel recupero dei clienti: {str(e)}")
    
    with tab3:
        st.subheader("Dettagli Rischio Specifico")
        
        risk_id = st.number_input("ID Rischio", min_value=1)
        
        if st.button("Carica Dettagli") and risk_id:
            try:
                risk = api_client.get_risk(risk_id)
                if risk:
                    st.json(risk)
                    
                    # Mostra polizze associate
                    st.subheader("Polizze Associate")
                    try:
                        policies_response = api_client._make_request("GET", f"/risks/{risk_id}/policies")
                        policies = policies_response.get("policies", [])
                        if policies:
                            df_policies = pd.DataFrame(policies)
                            st.dataframe(df_policies, use_container_width=True)
                        else:
                            st.info("Nessuna polizza associata a questo rischio")
                    except Exception as e:
                        st.warning(f"Impossibile recuperare le polizze: {str(e)}")
                else:
                    st.warning("Rischio non trovato")
            except Exception as e:
                st.error(f"Errore nel recupero del rischio: {str(e)}")

if __name__ == "__main__":
    risks_page()