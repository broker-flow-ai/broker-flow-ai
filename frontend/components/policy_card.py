import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any
from utils.api_client import api_client

def render_policy_card(policy_data: Dict[str, Any]):
    """Renderizza una card polizza stilizzata"""
    
    # Estrai i dati della polizza
    policy_id = policy_data.get('id', 'N/A')
    company = policy_data.get('company', 'N/A')
    status = policy_data.get('status', 'N/A')
    start_date = policy_data.get('start_date', '')
    end_date = policy_data.get('end_date', '')
    policy_number = policy_data.get('policy_number', 'N/A')
    client_name = policy_data.get('client_name', 'N/A')
    client_company = policy_data.get('client_company', 'N/A')
    
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
                    <p style="margin: 5px 0; color: var(--text-color);">👤 Cliente: {client_name} ({client_company})</p>
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
        """, unsafe_allow_html=True)

def render_policy_details(policy_data: Dict[str, Any]):
    """Renderizza i dettagli completi di una polizza"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informazioni Polizza")
        st.write(f"**Compagnia:** {policy_data.get('company', 'N/A')}")
        st.write(f"**Numero Polizza:** {policy_data.get('policy_number', 'N/A')}")
        
        # Mostra informazioni sul cliente se disponibili
        if 'client_name' in policy_data and 'client_company' in policy_data:
            st.write(f"**Cliente:** {policy_data.get('client_name', 'N/A')}")
            st.write(f"**Azienda Cliente:** {policy_data.get('client_company', 'N/A')}")
        elif 'client_info' in policy_data:
            client_info = policy_data['client_info']
            st.write(f"**Cliente:** {client_info.get('name', 'N/A')}")
            st.write(f"**Azienda Cliente:** {client_info.get('company', 'N/A')}")
        
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
        if 'client_name' in policy_data and 'client_company' in policy_data:
            st.write(f"**Cliente:** {policy_data.get('client_name', 'N/A')}")
            st.write(f"**Azienda Cliente:** {policy_data.get('client_company', 'N/A')}")
        elif 'client_info' in policy_data:
            client_info = policy_data['client_info']
            st.write(f"**Cliente:** {client_info.get('name', 'N/A')}")
            st.write(f"**Azienda Cliente:** {client_info.get('company', 'N/A')}")

    # Sezione Relazioni
    st.subheader("🔗 Relazioni")
    
    # Recupera sinistri associati alla polizza
    try:
        claims_data = api_client.get_policy_claims(policy_data.get('id'))
        
        if claims_data:
            st.markdown("### 🚨 Sinistri Associati")
            total_claims = sum(claim.get('amount', 0) for claim in claims_data)
            
            # Mostra riepilogo sinistri
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Totale Sinistri", len(claims_data))
            with col2:
                st.metric("Importo Totale", f"€{total_claims:,.2f}")
            with col3:
                avg_claim = total_claims / len(claims_data) if claims_data else 0
                st.metric("Importo Medio", f"€{avg_claim:,.2f}")
            
            # Mostra dettagli di ogni sinistro
            for claim in claims_data:
                with st.expander(f"🚨 Sinistro #{claim.get('id')} - {claim.get('claim_date', '')[:10] if claim.get('claim_date') else 'N/A'}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Importo:** €{claim.get('amount', 0):,.2f}")
                    with col2:
                        st.write(f"**Stato:** {claim.get('status', 'N/A').title()}")
                    with col3:
                        st.write(f"**Data:** {claim.get('claim_date', '')[:10] if claim.get('claim_date') else 'N/A'}")
                    
                    st.write(f"**Descrizione:** {claim.get('description', 'N/A')}")
        else:
            st.info(" Nessun sinistro registrato per questa polizza")
            
    except Exception as e:
        st.warning(f"Impossibile recuperare i sinistri: {str(e)}")
    
    # Recupera premi associati alla polizza
    try:
        premiums_data = api_client.get_policy_premiums(policy_data.get('id'))
        
        if premiums_data:
            st.markdown("### 💰 Premi Associati")
            total_premiums = sum(premium.get('amount', 0) for premium in premiums_data)
            
            # Mostra riepilogo premi
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Totale Premi", f"€{total_premiums:,.2f}")
            with col2:
                st.metric("Numero Premi", len(premiums_data))
            
            # Mostra dettagli di ogni premio
            for premium in premiums_data:
                with st.expander(f"💰 Premio - Scadenza: {premium.get('due_date', '')[:10] if premium.get('due_date') else 'N/A'}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Importo:** €{premium.get('amount', 0):,.2f}")
                    with col2:
                        st.write(f"**Stato Pagamento:** {premium.get('payment_status', 'N/A').title()}")
                    with col3:
                        st.write(f"**Scadenza:** {premium.get('due_date', '')[:10] if premium.get('due_date') else 'N/A'}")
                    
                    # Data pagamento se disponibile
                    if premium.get('payment_date'):
                        st.write(f"**Data Pagamento:** {premium.get('payment_date', '')[:10] if premium.get('payment_date') else 'N/A'}")
        else:
            st.info(" Nessun premio registrato per questa polizza")
            
    except Exception as e:
        st.warning(f"Errore nel caricamento premi: {str(e)}")

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
    
    # Recupera i rischi disponibili per la selezione
    try:
        risks_data = api_client.get_risks()
        if risks_data:
            # Crea un dizionario per la selezione con nome descrittivo
            risk_options = {}
            risk_names = []
            for risk in risks_data:
                # Crea un nome descrittivo per il rischio
                client_name = risk.get('client_name', f"Cliente {risk.get('client_id', 'N/A')}")
                client_company = risk.get('client_company', '')
                client_display = f"{client_name} ({client_company})" if client_company else client_name
                risk_name = f"{client_display} - {risk.get('risk_type', 'N/A')} (ID: {risk.get('id')})"
                risk_options[risk_name] = risk['id']
                risk_names.append(risk_name)
            
            # Selezione del rischio con dropdown
            st.subheader("Seleziona Rischio")
            selected_risk_name = st.selectbox(
                "Rischio Associato", 
                options=risk_names,
                index=risk_names.index([name for name, id in risk_options.items() if id == default_data.get('risk_id')][0]) if default_data.get('risk_id') and any(id == default_data.get('risk_id') for id in risk_options.values()) else 0,
                key="policy_risk_selection"
            )
            
            # Mostra informazioni sul cliente associato al rischio selezionato
            if selected_risk_name in risk_options:
                selected_risk_id = risk_options[selected_risk_name]
                selected_risk = next((risk for risk in risks_data if risk['id'] == selected_risk_id), None)
                if selected_risk:
                    st.info(f"_cliente: {selected_risk.get('client_name', 'N/A')} - {selected_risk.get('client_company', 'N/A')}_")
            
            # Recupera l'ID del rischio selezionato
            risk_id = risk_options[selected_risk_name] if selected_risk_name in risk_options else ''
        else:
            # Fallback al campo numerico se non ci sono rischi
            risk_id = st.number_input("ID Rischio", min_value=1, value=int(default_data['risk_id']) if default_data['risk_id'] else 1, key="policy_risk_id")
    except Exception as e:
        st.warning("Impossibile caricare i rischi disponibili")
        risk_id = st.number_input("ID Rischio", min_value=1, value=int(default_data['risk_id']) if default_data['risk_id'] else 1, key="policy_risk_id")
    
    # Recupera le compagnie disponibili
    try:
        companies_data = api_client.get_clients()
        if companies_data:
            # Filtra solo le compagnie assicurative
            insurance_companies = [client for client in companies_data if client.get('sector') == 'Assicurativo']
            
            company_options = {}
            company_names = []
            for company in insurance_companies:
                company_name = f"{company.get('company', company.get('name', 'N/A'))} (ID: {company.get('id')})"
                company_options[company_name] = company['id']
                company_names.append(company_name)
            
            # Selezione della compagnia con dropdown
            st.subheader("Seleziona Compagnia")
            selected_company_name = st.selectbox(
                "Compagnia Assicurativa", 
                options=company_names,
                index=company_names.index([name for name, id in company_options.items() if id == default_data.get('company_id')][0]) if default_data.get('company_id') and any(id == default_data.get('company_id') for id in company_options.values()) else 0,
                key="policy_company_selection"
            )
            
            # Recupera l'ID della compagnia selezionata
            company_id = company_options[selected_company_name] if selected_company_name in company_options else ''
            company_name_selected = selected_company_name.split(' (ID:')[0] if ' (ID:' in selected_company_name else selected_company_name
        else:
            # Fallback ai campi originali
            company_id = st.number_input("ID Compagnia", min_value=1, value=int(default_data['company_id']) if default_data['company_id'] else 1, key="policy_company_id")
            company_name_selected = st.text_input("Compagnia Assicurativa", value=default_data['company'], key="policy_company")
    except Exception as e:
        st.warning("Impossibile caricare le compagnie disponibili")
        company_id = st.number_input("ID Compagnia", min_value=1, value=int(default_data['company_id']) if default_data['company_id'] else 1, key="policy_company_id")
        company_name_selected = st.text_input("Compagnia Assicurativa", value=default_data['company'], key="policy_company")
    
    st.subheader("Dettagli Polizza")
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
        'company': company_name_selected,
        'policy_number': policy_number,
        'start_date': start_date.isoformat() if start_date else '',
        'end_date': end_date.isoformat() if end_date else '',
        'status': status
    }