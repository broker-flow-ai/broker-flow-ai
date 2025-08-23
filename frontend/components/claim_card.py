import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any

def render_claim_card(claim_data: Dict[str, Any]):
    """Renderizza una card sinistro stilizzata"""
    
    # Estrai i dati del sinistro
    claim_id = claim_data.get('id', 'N/A')
    policy_id = claim_data.get('policy_id', 'N/A')
    claim_date = claim_data.get('claim_date', '')
    amount = claim_data.get('amount', 0)
    status = claim_data.get('status', 'N/A')
    description = claim_data.get('description', 'N/A')
    
    # Formatta la data del sinistro
    def format_date(date_str):
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime('%d/%m/%Y')
            except:
                return date_str
        return 'N/A'
    
    formatted_date = format_date(claim_date)
    
    # Formatta l'importo
    formatted_amount = f"€{float(amount):,.2f}" if amount else '€0.00'
    
    # Determina il colore dello status
    status_colors = {
        'open': '#2196F3',        # Blu
        'in_review': '#FF9800',   # Arancione
        'approved': '#4CAF50',    # Verde
        'rejected': '#F44336'     # Rosso
    }
    status_color = status_colors.get(status.lower(), '#9E9E9E')  # Grigio default
    
    # Crea la card sinistro
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="margin: 0 0 10px 0; color: #1f77b4;">Sinistro #{claim_id}</h3>
                    <p style="margin: 5px 0; font-weight: bold;">Polizza: #{policy_id}</p>
                    <p style="margin: 5px 0; color: #666;">📅 Data: {formatted_date}</p>
                    <p style="margin: 5px 0; color: #666;">💰 Importo: {formatted_amount}</p>
                    <p style="margin: 5px 0; color: #666;">📝 {description[:100]}{'...' if len(description) > 100 else ''}</p>
                </div>
                <div style="text-align: right;">
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
        """, unsafe_allow_html=True)

def render_claim_details(claim_data: Dict[str, Any]):
    """Renderizza i dettagli completi di un sinistro"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informazioni Sinistro")
        st.write(f"**ID Sinistro:** #{claim_data.get('id', 'N/A')}")
        st.write(f"**ID Polizza:** #{claim_data.get('policy_id', 'N/A')}")
        
        # Data sinistro
        claim_date = claim_data.get('claim_date', '')
        if claim_date:
            try:
                date_obj = datetime.fromisoformat(claim_date.replace('Z', '+00:00'))
                st.write(f"**Data Sinistro:** {date_obj.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Data Sinistro:** {claim_date}")
        
        # Importo sinistro
        amount = claim_data.get('amount', 0)
        st.write(f"**Importo:** €{float(amount):,.2f}" if amount else "**Importo:** €0.00")
        
        # Stato sinistro
        st.write(f"**Stato:** {claim_data.get('status', 'N/A')}")
    
    with col2:
        st.subheader("Descrizione")
        description = claim_data.get('description', 'N/A')
        st.text_area("Dettagli Sinistro", value=description, height=150, disabled=True)
        
        # Informazioni aggiuntive se disponibili
        if 'policy_info' in claim_data:
            policy_info = claim_data['policy_info']
            st.subheader("Informazioni Polizza")
            st.write(f"**Tipo Rischio:** {policy_info.get('risk_type', 'N/A')}")
            st.write(f"**Compagnia:** {policy_info.get('company', 'N/A')}")

def render_claim_form(claim_data: Dict[str, Any] = None):
    """Renderizza un form per creare/modificare un sinistro"""
    
    # Valori di default
    default_data = {
        'policy_id': '',
        'claim_date': '',
        'amount': 0,
        'status': 'open',
        'description': ''
    }
    
    if claim_data:
        default_data.update(claim_data)
    
    # Campi del form con chiavi uniche
    policy_id = st.number_input(
        "ID Polizza", 
        min_value=1, 
        value=int(default_data['policy_id']) if default_data['policy_id'] else 1,
        help="Inserisci l'ID della polizza associata al sinistro",
        key="claim_policy_id"
    )
    
    # Date picker per la data del sinistro
    claim_date = st.date_input(
        "Data Sinistro", 
        value=datetime.today() if not default_data['claim_date'] else 
              datetime.fromisoformat(default_data['claim_date'].split('T')[0]) if default_data['claim_date'] else datetime.today(),
        key="claim_date"
    )
    
    amount = st.number_input(
        "Importo Sinistro (€)", 
        min_value=0.0, 
        value=float(default_data['amount']) if default_data['amount'] else 0.0,
        step=100.0,
        format="%.2f",
        key="claim_amount"
    )
    
    status = st.selectbox(
        "Stato Sinistro", 
        ["open", "in_review", "approved", "rejected"],
        index=["open", "in_review", "approved", "rejected"].index(default_data['status']) if default_data['status'] in ["open", "in_review", "approved", "rejected"] else 0,
        key="claim_status"
    )
    
    description = st.text_area(
        "Descrizione Sinistro", 
        value=default_data['description'],
        height=100,
        help="Inserisci una descrizione dettagliata del sinistro",
        key="claim_description"
    )
    
    return {
        'policy_id': policy_id,
        'claim_date': claim_date.isoformat() if claim_date else '',
        'amount': amount,
        'status': status,
        'description': description
    }