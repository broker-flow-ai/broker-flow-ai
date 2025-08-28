import streamlit as st
from datetime import datetime
from typing import Dict, Any
from utils.api_client import api_client

def render_client_card(client_data: Dict[str, Any]):
    """Renderizza una card cliente stilizzata"""
    
    # Estrai i dati del cliente
    client_id = client_data.get('id', 'N/A')
    name = client_data.get('name', 'N/A')
    company = client_data.get('company', 'N/A')
    client_type = client_data.get('client_type', 'individual')
    email = client_data.get('email', 'N/A')
    phone = client_data.get('phone', 'N/A')
    mobile = client_data.get('mobile', 'N/A')
    sector = client_data.get('sector', 'N/A')
    city = client_data.get('city', 'N/A')
    province = client_data.get('province', 'N/A')
    fiscal_code = client_data.get('fiscal_code', 'N/A')
    vat_number = client_data.get('vat_number', 'N/A')
    customer_status = client_data.get('customer_status', 'active')
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
    
    # Determina il colore dello status
    status_colors = {
        'active': '#4CAF50',      # Verde
        'inactive': '#FF9800',    # Arancione
        'prospect': '#2196F3'     # Blu
    }
    status_color = status_colors.get(customer_status.lower(), '#9E9E9E')  # Grigio default
    
    # Determina l'icona in base al tipo di cliente
    client_type_icons = {
        'individual': '👤',
        'company': '🏢',
        'freelance': '💼',
        'public_entity': '🏛️'
    }
    client_icon = client_type_icons.get(client_type, '👤')
    
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
                    <h3 style="margin: 0 0 10px 0; color: var(--primary-color);">{client_icon} {name}</h3>
                    <p style="margin: 5px 0; font-weight: bold;">{company}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">📧 {email}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">📞 {phone} | 📱 {mobile}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">🏢 Settore: {sector}</p>
                    <p style="margin: 5px 0; color: var(--text-color);">📍 {city} ({province})</p>
                    <p style="margin: 5px 0; color: var(--text-color);">💳 CF: {fiscal_code} | 📋 P.IVA: {vat_number}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0 0 5px 0; font-size: 0.9em; color: var(--text-color);">ID: {client_id}</p>
                    <span style="
                        background-color: {status_color};
                        color: white;
                        padding: 4px 8px;
                        border-radius: 12px;
                        font-size: 0.8em;
                        font-weight: bold;
                    ">{customer_status.title()}</span>
                    <p style="margin: 5px 0 0 0; font-size: 0.8em; color: var(--text-color);">Creato: {formatted_date}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_client_details(client_data: Dict[str, Any]):
    """Renderizza i dettagli completi di un cliente"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informazioni Generali")
        st.write(f"**Nome Completo:** {client_data.get('name', 'N/A')}")
        st.write(f"**Azienda:** {client_data.get('company', 'N/A')}")
        st.write(f"**Tipo Cliente:** {client_data.get('client_type', 'N/A').title()}")
        st.write(f"**Settore:** {client_data.get('sector', 'N/A')}")
        st.write(f"**Segmento:** {client_data.get('customer_segment', 'N/A')}")
        st.write(f"**Stato:** {client_data.get('customer_status', 'N/A').title()}")
        st.write(f"**Fonte Acquisizione:** {client_data.get('referred_by', 'N/A')}")
        
        # Date importanti
        if client_data.get('birth_date'):
            try:
                birth_date = datetime.fromisoformat(client_data['birth_date'].replace('Z', '+00:00'))
                st.write(f"**Data di Nascita:** {birth_date.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Data di Nascita:** {client_data.get('birth_date', 'N/A')}")
        
        if client_data.get('birth_place'):
            st.write(f"**Luogo di Nascita:** {client_data.get('birth_place', 'N/A')}")
        
        if client_data.get('establishment_date'):
            try:
                est_date = datetime.fromisoformat(client_data['establishment_date'].replace('Z', '+00:00'))
                st.write(f"**Data Costituzione:** {est_date.strftime('%d/%m/%Y')}")
            except:
                st.write(f"**Data Costituzione:** {client_data.get('establishment_date', 'N/A')}")
    
    with col2:
        st.subheader("Contatti")
        st.write(f"**Email:** {client_data.get('email', 'N/A')}")
        st.write(f"**Email PEC:** {client_data.get('pec_email', 'N/A')}")
        st.write(f"**Telefono:** {client_data.get('phone', 'N/A')}")
        st.write(f"**Cellulare:** {client_data.get('mobile', 'N/A')}")
        st.write(f"**Fax:** {client_data.get('fax', 'N/A')}")
        
        st.subheader("Preferenze")
        st.write(f"**Canale Comunicazione:** {client_data.get('preferred_communication', 'N/A').title()}")
        st.write(f"**Lingua:** {client_data.get('language', 'N/A')}")
    
    # Indirizzo
    st.subheader("Indirizzo")
    address_parts = []
    if client_data.get('address'):
        address_parts.append(client_data['address'])
    if client_data.get('city'):
        address_parts.append(client_data['city'])
    if client_data.get('province'):
        address_parts.append(f"({client_data['province']})")
    if client_data.get('postal_code'):
        address_parts.append(client_data['postal_code'])
    if client_data.get('country'):
        address_parts.append(client_data['country'])
    
    if address_parts:
        st.write("**Indirizzo Principale:** " + ", ".join(address_parts))
    else:
        st.write("**Indirizzo Principale:** N/A")
    
    # Dati fiscali
    st.subheader("Dati Fiscali")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Codice Fiscale:** {client_data.get('fiscal_code', 'N/A')}")
        st.write(f"**Partita IVA:** {client_data.get('vat_number', 'N/A')}")
        st.write(f"**Codice SDI:** {client_data.get('sdi_code', 'N/A')}")
        st.write(f"**Regime Fiscale:** {client_data.get('tax_regime', 'N/A')}")
    with col2:
        st.write(f"**Forma Giuridica:** {client_data.get('legal_form', 'N/A')}")
        st.write(f"**Num. Registro Imprese:** {client_data.get('company_registration_number', 'N/A')}")
        st.write(f"**REA Office:** {client_data.get('rea_office', 'N/A')}")
        st.write(f"**REA Number:** {client_data.get('rea_number', 'N/A')}")
        if client_data.get('share_capital'):
            st.write(f"**Capitale Sociale:** €{float(client_data['share_capital']):,.2f}")
        st.write(f"**Periodicità IVA:** {client_data.get('vat_settlement', 'N/A').title()}")
    
    # Dati bancari
    st.subheader("Dati Bancari")
    st.write(f"**IBAN:** {client_data.get('iban', 'N/A')}")
    st.write(f"**Nome Banca:** {client_data.get('bank_name', 'N/A')}")
    st.write(f"**IBAN Alternativo:** {client_data.get('bank_iban', 'N/A')}")
    
    # Note
    if client_data.get('notes'):
        st.subheader("Note")
        st.text_area("", value=client_data['notes'], height=100, disabled=True)
    
    # Informazioni di sistema
    st.subheader("Informazioni di Sistema")
    if client_data.get('created_at'):
        try:
            created_date = datetime.fromisoformat(client_data['created_at'].replace('Z', '+00:00'))
            st.write(f"**Creato il:** {created_date.strftime('%d/%m/%Y %H:%M')}")
        except:
            st.write(f"**Creato il:** {client_data.get('created_at', 'N/A')}")
    
    if client_data.get('updated_at'):
        try:
            updated_date = datetime.fromisoformat(client_data['updated_at'].replace('Z', '+00:00'))
            st.write(f"**Ultimo Aggiornamento:** {updated_date.strftime('%d/%m/%Y %H:%M')}")
        except:
            st.write(f"**Ultimo Aggiornamento:** {client_data.get('updated_at', 'N/A')}")

def render_client_form(client_data: Dict[str, Any] = None):
    """Renderizza un form per creare/modificare un cliente"""
    
    # Valori di default
    default_data = {
        # Informazioni di base
        'name': '',
        'company': '',
        'client_type': 'individual',  # individual, company, freelance, public_entity
        
        # Contatti
        'email': '',
        'phone': '',
        'mobile': '',
        'fax': '',
        
        # Indirizzi
        'address': '',
        'city': '',
        'province': '',
        'postal_code': '',
        'country': 'Italy',
        
        # Dati fiscali
        'fiscal_code': '',
        'vat_number': '',
        'tax_regime': '',
        'sdi_code': '',
        'pec_email': '',
        
        # Dati legali per società
        'legal_form': '',
        'company_registration_number': '',
        'rea_office': '',
        'rea_number': '',
        'share_capital': 0.0,
        'vat_settlement': 'monthly',  # monthly, quarterly, annual
        
        # Dati bancari
        'iban': '',
        'bank_name': '',
        'bank_iban': '',
        
        # Classificazioni
        'sector': '',
        'customer_segment': '',
        'customer_status': 'active',  # active, inactive, prospect
        'referred_by': '',
        
        # Date importanti
        'birth_date': '',
        'birth_place': '',
        'establishment_date': '',
        
        # Note e preferenze
        'notes': '',
        'preferred_communication': 'email',  # email, phone, mail, pec
        'language': 'it'
    }
    
    if client_data:
        default_data.update(client_data)
    
    # Tabs per organizzare i campi
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Informazioni Base", 
        "📍 Contatti e Indirizzi", 
        "💳 Dati Fiscali", 
        "🏦 Dati Bancari",
        "📊 Classificazioni"
    ])
    
    form_data = {}
    
    with tab1:
        st.subheader("Informazioni Generali")
        
        col1, col2 = st.columns(2)
        with col1:
            form_data['name'] = st.text_input("Nome Completo *", value=default_data['name'], key="client_name")
            form_data['email'] = st.text_input("Email", value=default_data['email'], key="client_email")
            form_data['phone'] = st.text_input("Telefono", value=default_data['phone'], key="client_phone")
            form_data['mobile'] = st.text_input("Cellulare", value=default_data['mobile'], key="client_mobile")
        
        with col2:
            form_data['client_type'] = st.selectbox(
                "Tipo Cliente *", 
                ["individual", "company", "freelance", "public_entity"],
                index=["individual", "company", "freelance", "public_entity"].index(default_data['client_type']) if default_data['client_type'] in ["individual", "company", "freelance", "public_entity"] else 0,
                key="client_type"
            )
            form_data['company'] = st.text_input("Azienda", value=default_data['company'], key="client_company")
            form_data['sector'] = st.selectbox(
                "Settore", 
                ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", 
                 "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"],
                index=0 if not default_data['sector'] else 
                      ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", 
                       "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"].index(default_data['sector']) if default_data['sector'] in ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", "Commercio", "Logistica", "Noleggio", "Assicurativo", "Altro"] else 0,
                key="client_sector"
            )
            form_data['fax'] = st.text_input("Fax", value=default_data['fax'], key="client_fax")
        
        # Campi condizionali basati sul tipo di cliente
        if form_data['client_type'] in ['company', 'freelance', 'public_entity']:
            st.subheader("Dati Aziendali")
            col1, col2, col3 = st.columns(3)
            with col1:
                form_data['legal_form'] = st.text_input("Forma Giuridica", value=default_data['legal_form'], key="client_legal_form")
            with col2:
                form_data['vat_number'] = st.text_input("Partita IVA", value=default_data['vat_number'], key="client_vat_number")
            with col3:
                form_data['company_registration_number'] = st.text_input("Num. Registro Imprese", value=default_data['company_registration_number'], key="client_company_registration_number")
            
            col1, col2 = st.columns(2)
            with col1:
                form_data['rea_office'] = st.text_input("Ufficio REA", value=default_data['rea_office'], key="client_rea_office")
            with col2:
                form_data['rea_number'] = st.text_input("Numero REA", value=default_data['rea_number'], key="client_rea_number")
            
            form_data['share_capital'] = st.number_input("Capitale Sociale (€)", min_value=0.0, value=float(default_data['share_capital']) if default_data['share_capital'] else 0.0, step=1000.0, key="client_share_capital")
            form_data['establishment_date'] = st.date_input("Data Costituzione", value=datetime.strptime(default_data['establishment_date'], '%Y-%m-%d').date() if default_data['establishment_date'] else None, key="client_establishment_date") if default_data['establishment_date'] else None
        else:
            st.subheader("Dati Personali")
            col1, col2 = st.columns(2)
            with col1:
                form_data['fiscal_code'] = st.text_input("Codice Fiscale", value=default_data['fiscal_code'], key="client_fiscal_code")
                form_data['birth_date'] = st.date_input("Data di Nascita", value=datetime.strptime(default_data['birth_date'], '%Y-%m-%d').date() if default_data['birth_date'] else None, key="client_birth_date") if default_data['birth_date'] else None
            with col2:
                form_data['birth_place'] = st.text_input("Luogo di Nascita", value=default_data['birth_place'], key="client_birth_place")
    
    with tab2:
        st.subheader("Indirizzo Principale")
        form_data['address'] = st.text_area("Indirizzo", value=default_data['address'], key="client_address")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            form_data['city'] = st.text_input("Città", value=default_data['city'], key="client_city")
        with col2:
            form_data['province'] = st.text_input("Provincia", value=default_data['province'], key="client_province")
        with col3:
            form_data['postal_code'] = st.text_input("CAP", value=default_data['postal_code'], key="client_postal_code")
        with col4:
            form_data['country'] = st.text_input("Nazione", value=default_data['country'], key="client_country")
    
    with tab3:
        st.subheader("Dati Fiscali")
        col1, col2 = st.columns(2)
        with col1:
            form_data['fiscal_code'] = st.text_input("Codice Fiscale", value=default_data['fiscal_code'], key="client_fiscal_code_tab3")
            form_data['sdi_code'] = st.text_input("Codice SDI", value=default_data['sdi_code'], key="client_sdi_code")
        with col2:
            form_data['vat_number'] = st.text_input("Partita IVA", value=default_data['vat_number'], key="client_vat_number_tab3")
            form_data['pec_email'] = st.text_input("Email PEC", value=default_data['pec_email'], key="client_pec_email")
        
        col1, col2 = st.columns(2)
        with col1:
            form_data['tax_regime'] = st.text_input("Regime Fiscale", value=default_data['tax_regime'], key="client_tax_regime")
        with col2:
            form_data['vat_settlement'] = st.selectbox(
                "Periodicità Liquidazione IVA",
                ["monthly", "quarterly", "annual"],
                index=["monthly", "quarterly", "annual"].index(default_data['vat_settlement']) if default_data['vat_settlement'] in ["monthly", "quarterly", "annual"] else 0,
                key="client_vat_settlement"
            )
    
    with tab4:
        st.subheader("Dati Bancari")
        form_data['iban'] = st.text_input("IBAN", value=default_data['iban'], key="client_iban")
        form_data['bank_name'] = st.text_input("Nome Banca", value=default_data['bank_name'], key="client_bank_name")
        form_data['bank_iban'] = st.text_input("IBAN Alternativo", value=default_data['bank_iban'], key="client_bank_iban")
    
    with tab5:
        st.subheader("Classificazioni")
        col1, col2, col3 = st.columns(3)
        with col1:
            form_data['customer_segment'] = st.text_input("Segmento Cliente", value=default_data['customer_segment'], key="client_customer_segment")
        with col2:
            form_data['customer_status'] = st.selectbox(
                "Stato Cliente",
                ["active", "inactive", "prospect"],
                index=["active", "inactive", "prospect"].index(default_data['customer_status']) if default_data['customer_status'] in ["active", "inactive", "prospect"] else 0,
                key="client_customer_status"
            )
        with col3:
            form_data['preferred_communication'] = st.selectbox(
                "Canale Comunicazione Preferito",
                ["email", "phone", "mail", "pec"],
                index=["email", "phone", "mail", "pec"].index(default_data['preferred_communication']) if default_data['preferred_communication'] in ["email", "phone", "mail", "pec"] else 0,
                key="client_preferred_communication"
            )
        
        form_data['referred_by'] = st.text_input("Fonte di Acquisizione", value=default_data['referred_by'], key="client_referred_by")
        form_data['notes'] = st.text_area("Note", value=default_data['notes'], key="client_notes")
        form_data['language'] = st.selectbox(
            "Lingua Preferita",
            ["it", "en", "es", "fr", "de"],
            index=["it", "en", "es", "fr", "de"].index(default_data['language']) if default_data['language'] in ["it", "en", "es", "fr", "de"] else 0,
            key="client_language"
        )
    
    return form_data