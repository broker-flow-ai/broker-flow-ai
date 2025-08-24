import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any

def render_policy_card(policy_data: Dict[str, Any]):
    """Renderizza una card polizza stilizzata"""
    
    # Estrai i dati della polizza
    policy_id = policy_data.get('id', 'N/A')
    company = policy_data.get('company', 'N/A')
    status = policy_data.get('status', 'N/A')
    start_date = policy_data.get('start_date', '')
    end_date = policy_data.get('end_date', '')
    policy_number = policy_data.get('policy_number', 'N/A')
    
    # Formatta le date
    def format_date(date_str):
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime('%d/%m/%Y')
            except:
                return date_str
        return 'N/A'
    
    formatted_start = format_date(start_date)
    formatted_end = format_date(end_date)
    
    # Determina il colore dello status
    status_colors = {
        'active': '#4CAF50',      # Verde
        'expired': '#FF9800',     # Arancione
        'cancelled': '#F44336',   # Rosso
        'pending': '#2196F3'      # Blu
    }
    status_color = status_colors.get(status.lower(), '#9E9E9E')  # Grigio default
    
    # Crea la card polizza
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
                    <h3 style="margin: 0 0 10px 0; color: var(--primary-color);">{company}</h3>
                    <p style="margin: 5px 0; font-weight: bold;">N. Polizza: {policy_number}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">📅 Validità: {formatted_start} - {formatted_end}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0 0 5px 0; font-size: 0.9em; color: var(--text-color);">ID: {policy_id}</p>
                    <span style="
                        background-color: {status_color};
                        color: white;
                        padding: 4px 8px;
                        border-radius: 12px;
                        font-size: 0.8em;
                        font-weight: bold;
                    ">{status.title()}</span>
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

def render_policy_details(policy_data: Dict[str, Any]):
    """Renderizza i dettagli completi di una polizza"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informazioni Polizza")
        st.write(f"**Compagnia:** {policy_data.get('company', 'N/A')}")
        st.write(f"**Numero Polizza:** {policy_data.get('policy_number', 'N/A')}")
        
        # Date di validità
        start_date = policy_data.get('start_date', '')
        end_date = policy_data.get('end_date', '')
        
        if start_date:
            try:
                start_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                st.write(f"**Inizio:** {start_obj.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Inizio:** {start_date}")
        
        if end_date:
            try:
                end_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                st.write(f"**Fine:** {end_obj.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Fine:** {end_date}")
    
    with col2:
        st.subheader("Stato e Dettagli")
        st.write(f"**Stato:** {policy_data.get('status', 'N/A')}")
        
        # Informazioni aggiuntive se disponibili
        if 'policy_pdf_path' in policy_data:
            st.write(f"**PDF:** {policy_data['policy_pdf_path']}")
        
        # Mostra informazioni sul cliente se disponibili
        if 'client_info' in policy_data:
            client_info = policy_data['client_info']
            st.write(f"**Cliente:** {client_info.get('name', 'N/A')}")
            st.write(f"**Azienda:** {client_info.get('company', 'N/A')}")

def render_policy_form(policy_data: Dict[str, Any] = None):
    """Renderizza un form per creare/modificare una polizza"""
    
    # Valori di default
    default_data = {
        'risk_id': '',
        'company_id': '',
        'company': '',
        'policy_number': '',
        'start_date': '',
        'end_date': '',
        'status': 'active'
    }
    
    if policy_data:
        default_data.update(policy_data)
    
    # Campi del form con chiavi uniche
    risk_id = st.number_input("ID Rischio", min_value=1, value=int(default_data['risk_id']) if default_data['risk_id'] else 1, key="policy_risk_id")
    company_id = st.number_input("ID Compagnia", min_value=1, value=int(default_data['company_id']) if default_data['company_id'] else 1, key="policy_company_id")
    company = st.text_input("Compagnia Assicurativa", value=default_data['company'], key="policy_company")
    policy_number = st.text_input("Numero Polizza", value=default_data['policy_number'], key="policy_number")
    
    # Date picker per le date di validità
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Inizio", value=datetime.today() if not default_data['start_date'] else datetime.fromisoformat(default_data['start_date'].split('T')[0]) if default_data['start_date'] else datetime.today(), key="policy_start_date")
    with col2:
        end_date = st.date_input("Data Fine", value=datetime.today() + timedelta(days=365) if not default_data['end_date'] else datetime.fromisoformat(default_data['end_date'].split('T')[0]) if default_data['end_date'] else datetime.today() + timedelta(days=365), key="policy_end_date")
    
    status = st.selectbox(
        "Stato", 
        ["active", "expired", "cancelled", "pending"],
        index=["active", "expired", "cancelled", "pending"].index(default_data['status']) if default_data['status'] in ["active", "expired", "cancelled", "pending"] else 0,
        key="policy_status"
    )
    
    return {
        'risk_id': risk_id,
        'company_id': company_id,
        'company': company,
        'policy_number': policy_number,
        'start_date': start_date.isoformat() if start_date else '',
        'end_date': end_date.isoformat() if end_date else '',
        'status': status
    }