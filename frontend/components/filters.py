import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, List, Optional

def render_client_filters() -> Dict[str, Any]:
    """Renderizza i filtri per la lista clienti"""
    
    with st.expander("🔍 Filtri Clienti", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            name_filter = st.text_input("Nome Cliente", "")
            company_filter = st.text_input("Azienda", "")
            client_type_filter = st.multiselect(
                "Tipo Cliente",
                ["individual", "company", "freelance", "public_entity"],
                default=[]
            )
        
        with col2:
            sector_filter = st.multiselect(
                "Settore",
                ["", "Trasporti", "Sanità", "Edilizia", "Legalità", "Ingegneria", 
                 "Commercio", "Logistica", "Noleggio", "Assicurativo"],
                default=[]
            )
            customer_status_filter = st.multiselect(
                "Stato Cliente",
                ["active", "inactive", "prospect"],
                default=[]
            )
        
        with col3:
            email_filter = st.text_input("Email", "")
            fiscal_code_filter = st.text_input("Codice Fiscale", "")
            vat_number_filter = st.text_input("Partita IVA", "")
        
        with col4:
            # Filtro per data creazione
            st.write("Data Creazione")
            date_from = st.date_input("Da", value=None, key="client_date_from")
            date_to = st.date_input("A", value=None, key="client_date_to")
            
            # Filtro per città e provincia
            city_filter = st.text_input("Città", "")
            province_filter = st.text_input("Provincia", "")
        
        # Pulsanti di azione
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            apply_filters = st.button("Applica Filtri", key="apply_client_filters")
        with col_btn2:
            clear_filters = st.button("Pulisci Filtri", key="clear_client_filters")
        with col_btn3:
            st.write("")  # Spazio vuoto per allineamento
        
        # Ritorna i filtri selezionati
        filters = {
            'name': name_filter,
            'company': company_filter,
            'client_type': client_type_filter,
            'sector': sector_filter,
            'customer_status': customer_status_filter,
            'email': email_filter,
            'fiscal_code': fiscal_code_filter,
            'vat_number': vat_number_filter,
            'city': city_filter,
            'province': province_filter,
            'date_from': date_from,
            'date_to': date_to,
            'apply': apply_filters,
            'clear': clear_filters
        }
        
        return filters

def render_policy_filters() -> Dict[str, Any]:
    """Renderizza i filtri per la lista polizze"""
    
    with st.expander("🔍 Filtri Polizze", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Filtro per cliente
            client_filter = st.text_input("Cliente", "")
            company_filter = st.text_input("Compagnia", "")
            policy_number_filter = st.text_input("Numero Polizza", "")
        
        with col2:
            risk_type_filter = st.multiselect(
                "Tipo Rischio",
                ["", "Flotta Auto", "RC Professionale", "Fabbricato", "Rischi Tecnici", "Altro"],
                default=[]
            )
            status_filter = st.multiselect(
                "Stato",
                ["active", "expired", "cancelled", "pending"],
                default=[]
            )
        
        with col3:
            # Filtro per date di sottoscrizione
            st.write("Data Sottoscrizione")
            subscription_from = st.date_input("Da", value=None, key="policy_subscription_from")
            subscription_to = st.date_input("A", value=None, key="policy_subscription_to")
            
            # Filtro per date di validità
            st.write("Validità Polizza")
            validity_from = st.date_input("Da", value=None, key="policy_validity_from")
            validity_to = st.date_input("A", value=None, key="policy_validity_to")
        
        with col4:
            # Filtro per importo premio
            st.write("Importo Premio")
            premium_min = st.number_input("Min (€)", min_value=0.0, value=0.0, step=100.0, key="policy_premium_min")
            premium_max = st.number_input("Max (€)", min_value=0.0, value=0.0, step=1000.0, key="policy_premium_max")
            
            # Filtro per metodo di sottoscrizione e pagamento
            subscription_method_filter = st.multiselect(
                "Metodo Sottoscrizione",
                ["digital", "paper", "agent"],
                default=[]
            )
            payment_method_filter = st.multiselect(
                "Metodo Pagamento",
                ["direct_debit", "bank_transfer", "credit_card", "cash", "check"],
                default=[]
            )
        
        # Pulsanti di azione
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            apply_filters = st.button("Applica Filtri", key="apply_policy_filters")
        with col_btn2:
            clear_filters = st.button("Pulisci Filtri", key="clear_policy_filters")
        with col_btn3:
            st.write("")  # Spazio vuoto per allineamento
        
        # Ritorna i filtri selezionati
        filters = {
            'client': client_filter,
            'company': company_filter,
            'policy_number': policy_number_filter,
            'risk_type': risk_type_filter,
            'status': status_filter,
            'subscription_from': subscription_from,
            'subscription_to': subscription_to,
            'start_date_from': validity_from,
            'start_date_to': validity_to,
            'premium_min': premium_min if premium_min > 0 else None,
            'premium_max': premium_max if premium_max > 0 else None,
            'subscription_method': subscription_method_filter,
            'payment_method': payment_method_filter,
            'apply': apply_filters,
            'clear': clear_filters
        }
        
        return filters

def render_claim_filters() -> Dict[str, Any]:
    """Renderizza i filtri per la lista sinistri"""
    
    with st.expander("🔍 Filtri Sinistri", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            policy_id_filter = st.number_input("ID Polizza", min_value=0, value=0, step=1, key="claim_policy_id_filter")
            status_filter = st.multiselect(
                "Stato",
                ["open", "in_review", "approved", "rejected"],
                default=[]
            )
        
        with col2:
            # Filtro per date sinistro
            st.write("Data Sinistro")
            claim_date_from = st.date_input("Da", value=None, key="claim_date_from")
            claim_date_to = st.date_input("A", value=None, key="claim_date_to")
        
        with col3:
            # Filtro per importo sinistro
            st.write("Importo Sinistro")
            amount_min = st.number_input("Min (€)", min_value=0.0, value=0.0, step=100.0, key="claim_amount_min")
            amount_max = st.number_input("Max (€)", min_value=0.0, value=0.0, step=1000.0, key="claim_amount_max")
        
        with col4:
            description_filter = st.text_input("Descrizione", "")
        
        # Pulsanti di azione
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            apply_filters = st.button("Applica Filtri", key="apply_claim_filters")
        with col_btn2:
            clear_filters = st.button("Pulisci Filtri", key="clear_claim_filters")
        with col_btn3:
            st.write("")  # Spazio vuoto per allineamento
        
        # Ritorna i filtri selezionati
        filters = {
            'policy_id': policy_id_filter if policy_id_filter > 0 else None,
            'status': status_filter,
            'claim_date_from': claim_date_from,
            'claim_date_to': claim_date_to,
            'amount_min': amount_min,
            'amount_max': amount_max,
            'description': description_filter,
            'apply': apply_filters,
            'clear': clear_filters
        }
        
        return filters

def render_date_range_selector(label: str = "Seleziona Periodo") -> tuple:
    """Renderizza un selettore di intervallo date"""
    
    st.subheader(label)
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Data Inizio", value=date.today().replace(day=1))
    
    with col2:
        end_date = st.date_input("Data Fine", value=date.today())
    
    return start_date, end_date

def render_sorting_options(options: List[str], default_option: str = None) -> str:
    """Renderizza opzioni di ordinamento"""
    
    st.subheader("Ordinamento")
    selected_option = st.selectbox(
        "Ordina per",
        options,
        index=options.index(default_option) if default_option and default_option in options else 0
    )
    
    sort_direction = st.radio(
        "Direzione",
        [" Crescente", " Decrescente"],
        horizontal=True
    )
    
    return selected_option, sort_direction.strip()

def render_pagination_controls(current_page: int, total_pages: int, items_per_page: int = 10) -> int:
    """Renderizza controlli di paginazione"""
    
    st.subheader("Navigazione")
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col1:
        if st.button("⏮ Prima") and current_page > 1:
            current_page = 1
    
    with col2:
        if st.button("◀ Prec") and current_page > 1:
            current_page -= 1
    
    with col3:
        if st.button(" Succ ▶") and current_page < total_pages:
            current_page += 1
    
    with col4:
        if st.button("Ultima ⏭") and current_page < total_pages:
            current_page = total_pages
    
    # Mostra informazioni paginazione
    st.caption(f"Pagina {current_page} di {total_pages}")
    
    return current_page

def render_export_options(export_types: List[str] = ["CSV", "Excel", "PDF"]) -> str:
    """Renderizza opzioni di esportazione"""
    
    st.subheader("Esporta Dati")
    selected_export = st.selectbox(
        "Formato Esportazione",
        export_types,
        index=0
    )
    
    if st.button("Esporta"):
        return selected_export
    
    return None