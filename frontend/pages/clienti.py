import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, Any, List

# Import moduli locali
from utils.api_client import api_client
from utils.data_formatter import DataFormatter
from utils.validators import Validators
from utils.auth_decorator import require_role, has_delete_permission
from components.client_card import render_client_card, render_client_details, render_client_form
from components.filters import render_client_filters

@require_role(allowed_roles=["admin", "broker", "customer_service"])
def clients_page():
    """Pagina principale gestione clienti"""
    st.title("👥 Gestione Clienti")
    
    # Controlla se dobbiamo mostrare la vista dettagliata
    if 'selected_client' in st.session_state:
        render_client_detail_view()
        return
    
    # Controlla se dobbiamo mostrare il form di modifica
    if 'editing_client' in st.session_state:
        render_new_client_form()
        return
    
    # Tabs per diverse funzionalità
    tab1, tab2, tab3 = st.tabs(["📋 Lista Clienti", "➕ Nuovo Cliente", "📊 Analisi Clienti"])
    
    with tab1:
        render_clients_list()
    
    with tab2:
        render_new_client_form()
    
    with tab3:
        render_clients_analysis()

def render_clients_list():
    """Renderizza la lista dei clienti con filtri"""
    st.subheader("Lista Clienti")
    
    # Applica filtri
    filters = render_client_filters()
    
    try:
        # Recupera clienti dal backend
        clients_data = api_client.get_clients(filters)
        
        if not clients_data:
            st.info(" Nessun cliente trovato con i filtri selezionati")
            return
        
        # Converti in DataFrame per facilitare la gestione
        df = pd.DataFrame(clients_data)
        
        # Formatta i dati per la visualizzazione
        if 'created_at' in df.columns:
            df['created_at_formatted'] = df['created_at'].apply(DataFormatter.format_date)
        
        if 'sector' in df.columns:
            df['sector_formatted'] = df['sector'].apply(DataFormatter.format_sector)
        
        # Visualizza i clienti come cards
        st.subheader(f"Clienti ({len(df)} trovati)")
        
        # Pagination
        items_per_page = 10
        total_pages = (len(df) - 1) // items_per_page + 1
        current_page = st.session_state.get('client_page', 1)
        
        # Controlli di navigazione
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⏮ Prima") and current_page > 1:
                current_page = 1
                st.session_state.client_page = current_page
        
        with col2:
            # Solo mostra lo slider se ci sono più pagine
            if total_pages > 1:
                page_selection = st.slider(
                    "Pagina",
                    min_value=1,
                    max_value=total_pages,
                    value=current_page,
                    key="client_page_slider"
                )
                current_page = page_selection
                st.session_state.client_page = current_page
            else:
                st.write(f"Pagina {current_page} di {total_pages}")
        
        with col3:
            if st.button("Ultima ⏭") and current_page < total_pages:
                current_page = total_pages
                st.session_state.client_page = current_page
        
        # Calcola indici per la pagina corrente
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(df))
        
        # Visualizza clienti della pagina corrente
        page_clients = df.iloc[start_idx:end_idx]
        
        for _, client in page_clients.iterrows():
            render_client_card(client.to_dict())
            
            # Pulsanti di azione per ogni cliente
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"👁 Dettagli #{client['id']}", key=f"view_{client['id']}"):
                    st.session_state.selected_client = client['id']
                    st.rerun()
            with col2:
                if st.button(f"✏ Modifica #{client['id']}", key=f"edit_{client['id']}"):
                    st.session_state.editing_client = client['id']
                    st.rerun()
            with col3:
                if has_delete_permission() and st.button(f"🗑 Elimina #{client['id']}", key=f"delete_{client['id']}"):
                    st.warning(f"Eliminazione cliente #{client['id']} non ancora implementata")
            
            st.markdown("---")
        
        # Informazioni paginazione
        st.caption(f"Visualizzati clienti {start_idx + 1}-{end_idx} di {len(df)} totali")
        
    except Exception as e:
        st.error(f"Errore nel caricamento dei clienti: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_new_client_form():
    """Renderizza il form per creare un nuovo cliente"""
    st.subheader("Nuovo Cliente")
    
    # Recupera dati esistenti se si sta modificando
    client_data = None
    if 'editing_client' in st.session_state:
        try:
            client_data = api_client.get_client(st.session_state.editing_client)
        except Exception as e:
            st.error(f"Errore nel caricamento cliente: {str(e)}")
            del st.session_state.editing_client
    
    # Renderizza form cliente
    form_data = render_client_form(client_data)
    
    # Pulsanti di azione
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Salva Cliente"):
            # Validazione dati
            is_valid, errors = Validators.validate_client_data(form_data)
            
            if not is_valid:
                for error in errors:
                    st.error(error)
            else:
                try:
                    if client_data:
                        # Aggiorna cliente esistente
                        result = api_client.update_client(st.session_state.editing_client, form_data)
                        st.success(f"Cliente aggiornato con successo! ID: {result.get('client_id', 'N/A')}")
                        del st.session_state.editing_client
                    else:
                        # Crea nuovo cliente
                        result = api_client.create_client(form_data)
                        st.success(f"Cliente creato con successo! ID: {result.get('client_id', 'N/A')}")
                    
                    # Reset form
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Errore nel salvataggio del cliente: {str(e)}")
    
    with col2:
        if st.button("❌ Annulla"):
            if 'editing_client' in st.session_state:
                del st.session_state.editing_client
            st.rerun()
    
    with col3:
        st.write("")  # Spazio vuoto per allineamento

def render_clients_analysis():
    """Renderizza l'analisi dei clienti"""
    st.subheader("Analisi Clienti")
    
    try:
        # Recupera tutti i clienti per l'analisi
        clients_data = api_client.get_clients()
        
        if not clients_data:
            st.info(" Nessun cliente disponibile per l'analisi")
            return
        
        df = pd.DataFrame(clients_data)
        
        # Analisi per settore
        if 'sector' in df.columns:
            sector_counts = df['sector'].value_counts()
            
            st.subheader("Distribuzione Clienti per Settore")
            fig_sector = px.pie(
                values=sector_counts.values,
                names=sector_counts.index,
                title="Clienti per Settore"
            )
            st.plotly_chart(fig_sector, use_container_width=True)
        
        # Analisi per azienda
        if 'company' in df.columns:
            company_counts = df['company'].value_counts().head(10)
            
            st.subheader("Top 10 Aziende per Numero Clienti")
            fig_company = px.bar(
                x=company_counts.index,
                y=company_counts.values,
                labels={'x': 'Azienda', 'y': 'Numero Clienti'},
                title="Top Aziende Clienti"
            )
            st.plotly_chart(fig_company, use_container_width=True)
        
        # Analisi temporale
        if 'created_at' in df.columns:
            df['created_month'] = pd.to_datetime(df['created_at']).dt.to_period('M')
            monthly_counts = df['created_month'].value_counts().sort_index()
            
            st.subheader("Andamento Registrazione Clienti")
            fig_timeline = px.line(
                x=monthly_counts.index.astype(str),
                y=monthly_counts.values,
                labels={'x': 'Mese', 'y': 'Nuovi Clienti'},
                title="Registrazione Clienti Mensile"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Statistiche generali
        st.subheader("Statistiche Generali")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Totale Clienti", len(df))
        col2.metric("Settori Unici", df['sector'].nunique() if 'sector' in df.columns else 0)
        col3.metric("Aziende Uniche", df['company'].nunique() if 'company' in df.columns else 0)
        col4.metric("Email Validi", df['email'].notna().sum() if 'email' in df.columns else 0)
        
    except Exception as e:
        st.error(f"Errore nell'analisi dei clienti: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_client_detail_view():
    """Renderizza la vista dettagliata di un cliente"""
    if 'selected_client' not in st.session_state:
        return
    
    try:
        client_id = st.session_state.selected_client
        client_data = api_client.get_client(client_id)
        
        st.subheader(f"Dettagli Cliente #{client_id}")
        
        if st.button("⬅ Torna alla Lista"):
                    del st.session_state.selected_client
                    st.rerun()
        
        # Visualizza dettagli cliente
        render_client_details(client_data)
        
        # Sezione polizze del cliente
        st.subheader("Polizze Associate")
        try:
            policies_data = api_client.get_policies({"client_id": client_id})
            
            if policies_data:
                df_policies = pd.DataFrame(policies_data)
                
                # Formatta i dati per visualizzazione
                if 'start_date' in df_policies.columns:
                    df_policies['start_date_formatted'] = df_policies['start_date'].apply(DataFormatter.format_date)
                if 'end_date' in df_policies.columns:
                    df_policies['end_date_formatted'] = df_policies['end_date'].apply(DataFormatter.format_date)
                if 'amount' in df_policies.columns:
                    df_policies['amount_formatted'] = df_policies['amount'].apply(DataFormatter.format_currency)
                
                # Visualizza tabella polizze
                st.dataframe(
                    df_policies[['risk_type', 'company', 'policy_number', 'start_date_formatted', 
                               'end_date_formatted', 'amount_formatted', 'status']],
                    use_container_width=True
                )
            else:
                st.info(" Nessuna polizza associata a questo cliente")
                
        except Exception as e:
            st.error(f"Errore nel caricamento polizze: {str(e)}")
        
        # Sezione sinistri del cliente
        st.subheader("Sinistri Registrati")
        try:
            claims_data = api_client.get_claims({"client_id": client_id})
            
            if claims_data:
                df_claims = pd.DataFrame(claims_data)
                
                # Formatta i dati per visualizzazione
                if 'claim_date' in df_claims.columns:
                    df_claims['claim_date_formatted'] = df_claims['claim_date'].apply(DataFormatter.format_date)
                if 'amount' in df_claims.columns:
                    df_claims['amount_formatted'] = df_claims['amount'].apply(DataFormatter.format_currency)
                
                # Visualizza tabella sinistri
                st.dataframe(
                    df_claims[['claim_date_formatted', 'amount_formatted', 'status', 'description']],
                    use_container_width=True
                )
            else:
                st.info(" Nessun sinistro registrato per questo cliente")
                
        except Exception as e:
            st.error(f"Errore nel caricamento sinistri: {str(e)}")
        
        # Sezione delegati pagamento
        st.subheader("Delegati al Pagamento")
        try:
            delegates_data = api_client.get_premium_delegates(client_id)
            
            if delegates_data:
                df_delegates = pd.DataFrame(delegates_data)
                
                # Formatta i dati per visualizzazione
                if 'created_at' in df_delegates.columns:
                    df_delegates['created_at_formatted'] = df_delegates['created_at'].apply(DataFormatter.format_date)
                
                # Visualizza tabella delegati
                st.dataframe(
                    df_delegates[['first_name', 'last_name', 'company_name', 'email', 'mobile', 'created_at_formatted', 'is_active']],
                    use_container_width=True
                )
            else:
                st.info(" Nessun delegato al pagamento registrato per questo cliente")
                
        except Exception as e:
            st.error(f"Errore nel caricamento delegati: {str(e)}")
        
    except Exception as e:
        st.error(f"Errore nel caricamento dettagli cliente: {str(e)}")
        if st.button("⬅ Torna alla Lista"):
            del st.session_state.selected_client
            st.rerun()

# Esportazioni
__all__ = ['clients_page', 'render_client_detail_view']

# Esegui la pagina se richiamata direttamente
if __name__ == "__main__":
    clients_page()