import streamlit as st
from datetime import datetime
from typing import Dict, Any

def render_client_card(client_data: Dict[str, Any]):
    """Renderizza una card cliente stilizzata"""
    
    # Estrai i dati del cliente
    client_id = client_data.get('id', 'N/A')
    name = client_data.get('name', 'N/A')
    company = client_data.get('company', 'N/A')
    email = client_data.get('email', 'N/A')
    sector = client_data.get('sector', 'N/A')
    created_at = client_data.get('created_at', '')
    
    # Formatta la data di creazione
    if created_at:
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            formatted_date = created_date.strftime('%d/%m/%Y')
        except:
            formatted_date = created_at
    else:
        formatted_date = 'N/A'
    
    # Crea la card cliente
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: var(--background-color);
            color: var(--text-color);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0 0 10px 0; color: var(--primary-color);">{name}</h3>
                    <p style="margin: 5px 0; font-weight: bold;">{company}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">📧 {email}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">🏢 Settore: {sector}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0 0 5px 0; font-size: 0.9em; color: var(--text-color);">ID: {client_id}</p>
                    <p style="margin: 0; font-size: 0.8em; color: var(--text-color);">Creato: {formatted_date}</p>
                </div>
            </div>
        </div>
        <style>
        :root {{
            --background-color: #ffffff;
            --text-color: #000000;
            --primary-color: #1f77b4;
        }}
        
        /* Stili per il tema dark */
        [data-testid="stAppViewContainer"] {{
            --background-color: #0e1117;
            --text-color: #fafafa;
            --primary-color: #ff4b4b;
        }}
        
        /* Applica i colori del testo alle card */
        .stMarkdown > div > div {{
            background-color: var(--background-color) !important;
            color: var(--text-color) !important;
        }}
        </style>
        """, unsafe_allow_html=True)

def render_client_details(client_data: Dict[str, Any]):
    """Renderizza i dettagli completi di un cliente"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informazioni Anagrafiche")
        st.write(f"**Nome:** {client_data.get('name', 'N/A')}")
        st.write(f"**Azienda:** {client_data.get('company', 'N/A')}")
        st.write(f"**Email:** {client_data.get('email', 'N/A')}")
        st.write(f"**Settore:** {client_data.get('sector', 'N/A')}")
        
        # Mostra data creazione se disponibile
        created_at = client_data.get('created_at', '')
        if created_at:
            try:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                st.write(f"**Cliente dal:** {created_date.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Cliente dal:** {created_at}")
    
    with col2:
        st.subheader("Statistiche Cliente")
        # Qui andranno aggiunte le statistiche quando saranno disponibili
        st.info("📊 Statistiche in fase di implementazione")

def render_client_form(client_data: Dict[str, Any] = None):
    """Renderizza un form per creare/modificare un cliente"""
    
    # Valori di default
    default_data = {
        'name': '',
        'company': '',
        'email': '',
        'sector': ''
    }
    
    if client_data:
        default_data.update(client_data)
    
    # Campi del form con chiavi uniche
    name = st.text_input("Nome Cliente", value=default_data['name'], key="client_name")
    company = st.text_input("Azienda", value=default_data['company'], key="client_company")
    email = st.text_input("Email", value=default_data['email'], key="client_email")
    sector = st.selectbox(
        "Settore", 
        ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", 
         "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"],
        index=0 if not default_data['sector'] else 
              ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", 
               "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"].index(default_data['sector']) if default_data['sector'] in ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"] else 0,
        key="client_sector"
    )
    
    return {
        'name': name,
        'company': company,
        'email': email,
        'sector': sector
    }