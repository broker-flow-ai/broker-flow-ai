import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, Any, List

# Import moduli locali
from utils.api_client import api_client
from utils.data_formatter import DataFormatter
from utils.validators import Validators
from components.policy_card import render_policy_card, render_policy_details, render_policy_form
from components.filters import render_policy_filters

def policies_page():
    """Pagina principale gestione polizze"""
    st.title("📜 Gestione Polizze")
    
    # Controlla se dobbiamo mostrare la vista dettagliata
    if 'selected_policy' in st.session_state:
        render_policy_detail_view()
        return
    
    # Controlla se dobbiamo mostrare il form di modifica
    if 'editing_policy' in st.session_state:
        render_new_policy_form()
        return
    
    # Tabs per diverse funzionalità
    tab1, tab2, tab3 = st.tabs(["📋 Lista Polizze", "➕ Nuova Polizza", "📊 Analisi Polizze"])
    
    with tab1:
        render_policies_list()
    
    with tab2:
        render_new_policy_form()
    
    with tab3:
        render_policies_analysis()

def render_policies_list():
    """Renderizza la lista delle polizze con filtri"""
    st.subheader("Lista Polizze")
    
    # Applica filtri
    filters = render_policy_filters()
    
    try:
        # Recupera polizze dal backend
        policies_data = api_client.get_policies(filters)
        
        if not policies_data:
            st.info(" Nessuna polizza trovata con i filtri selezionati")
            return
        
        # Converti in DataFrame per facilitare la gestione
        df = pd.DataFrame(policies_data)
        
        # Formatta i dati per la visualizzazione
        if 'start_date' in df.columns:
            df['start_date_formatted'] = df['start_date'].apply(DataFormatter.format_date)
        if 'end_date' in df.columns:
            df['end_date_formatted'] = df['end_date'].apply(DataFormatter.format_date)
        
        # Visualizza le polizze come cards
        st.subheader(f"Polizze ({len(df)} trovate)")
        
        # Pagination
        items_per_page = 10
        total_pages = (len(df) - 1) // items_per_page + 1
        current_page = st.session_state.get('policy_page', 1)
        
        # Controlli di navigazione
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⏮ Prima") and current_page > 1:
                current_page = 1
                st.session_state.policy_page = current_page
        
        with col2:
            # Solo mostra lo slider se ci sono più pagine
            if total_pages > 1:
                page_selection = st.slider(
                    "Pagina",
                    min_value=1,
                    max_value=total_pages,
                    value=current_page,
                    key="policy_page_slider"
                )
                current_page = page_selection
                st.session_state.policy_page = current_page
            else:
                st.write(f"Pagina {current_page} di {total_pages}")
        
        with col3:
            if st.button("Ultima ⏭") and current_page < total_pages:
                current_page = total_pages
                st.session_state.policy_page = current_page
        
        # Calcola indici per la pagina corrente
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(df))
        
        # Visualizza polizze della pagina corrente
        page_policies = df.iloc[start_idx:end_idx]
        
        for _, policy in page_policies.iterrows():
            render_policy_card(policy.to_dict())
            
            # Pulsanti di azione per ogni polizza
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"👁 Dettagli #{policy['id']}", key=f"view_policy_{policy['id']}"):
                    st.session_state.selected_policy = policy['id']
                    st.rerun()
            with col2:
                if st.button(f"✏ Modifica #{policy['id']}", key=f"edit_policy_{policy['id']}"):
                    st.session_state.editing_policy = policy['id']
                    st.rerun()
            with col3:
                if st.button(f"🗑 Elimina #{policy['id']}", key=f"delete_policy_{policy['id']}"):
                    st.warning(f"Eliminazione polizza #{policy['id']} non ancora implementata")
            
            st.markdown("---")
        
        # Informazioni paginazione
        st.caption(f"Visualizzate polizze {start_idx + 1}-{end_idx} di {len(df)} totali")
        
    except Exception as e:
        st.error(f"Errore nel caricamento delle polizze: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_new_policy_form():
    """Renderizza il form per creare una nuova polizza"""
    st.subheader("Nuova Polizza")
    
    # Recupera dati esistenti se si sta modificando
    policy_data = None
    if 'editing_policy' in st.session_state:
        try:
            policy_data = api_client.get_policy(st.session_state.editing_policy)
        except Exception as e:
            st.error(f"Errore nel caricamento polizza: {str(e)}")
            del st.session_state.editing_policy
    
    # Renderizza form polizza
    form_data = render_policy_form(policy_data)
    
    # Pulsanti di azione
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Salva Polizza"):
            # Validazione dati
            is_valid, errors = Validators.validate_policy_data(form_data)
            
            if not is_valid:
                for error in errors:
                    st.error(error)
            else:
                try:
                    if policy_data:
                        # Aggiorna polizza esistente
                        result = api_client.update_policy(st.session_state.editing_policy, form_data)
                        st.success(f"Polizza aggiornata con successo! ID: {result.get('policy_id', 'N/A')}")
                        del st.session_state.editing_policy
                    else:
                        # Crea nuova polizza
                        result = api_client.create_policy(form_data)
                        st.success(f"Polizza creata con successo! ID: {result.get('policy_id', 'N/A')}")
                    
                    # Reset form
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Errore nel salvataggio della polizza: {str(e)}")
    
    with col2:
        if st.button("❌ Annulla"):
            if 'editing_policy' in st.session_state:
                del st.session_state.editing_policy
            st.rerun()
    
    with col3:
        st.write("")  # Spazio vuoto per allineamento

def render_policies_analysis():
    """Renderizza l'analisi delle polizze"""
    st.subheader("Analisi Polizze")
    
    try:
        # Recupera tutte le polizze per l'analisi
        policies_data = api_client.get_policies()
        
        if not policies_data:
            st.info(" Nessuna polizza disponibile per l'analisi")
            return
        
        df = pd.DataFrame(policies_data)
        
        # Analisi per compagnia
        if 'company' in df.columns:
            company_counts = df['company'].value_counts()
            
            st.subheader("Distribuzione Polizze per Compagnia")
            fig_company = px.pie(
                values=company_counts.values,
                names=company_counts.index,
                title="Polizze per Compagnia"
            )
            st.plotly_chart(fig_company, use_container_width=True)
        
        # Analisi per stato
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            
            st.subheader("Distribuzione Polizze per Stato")
            fig_status = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                labels={'x': 'Stato', 'y': 'Numero Polizze'},
                title="Polizze per Stato"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Analisi temporale
        if 'start_date' in df.columns:
            df['start_year_month'] = pd.to_datetime(df['start_date']).dt.to_period('M')
            monthly_counts = df['start_year_month'].value_counts().sort_index()
            
            st.subheader("Andamento Emissione Polizze")
            fig_timeline = px.line(
                x=monthly_counts.index.astype(str),
                y=monthly_counts.values,
                labels={'x': 'Mese', 'y': 'Polizze Emesse'},
                title="Emissione Polizze Mensile"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Analisi per compagnia
        if 'company' in df.columns:
            company_counts = df['company'].value_counts().head(10)
            
            st.subheader("Top 10 Compagnie per Numero Polizze")
            fig_company = px.bar(
                x=company_counts.index,
                y=company_counts.values,
                labels={'x': 'Compagnia', 'y': 'Numero Polizze'},
                title="Polizze per Compagnia"
            )
            st.plotly_chart(fig_company, use_container_width=True)
        
        # Statistiche generali
        st.subheader("Statistiche Generali")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Totale Polizze", len(df))
        col2.metric("Compagnie Uniche", df['company'].nunique() if 'company' in df.columns else 0)
        col3.metric("Polizze Attive", len(df[df['status'] == 'active']) if 'status' in df.columns else 0)
        col4.metric("ID Rischio Min", df['risk_id'].min() if 'risk_id' in df.columns else 0)
        
    except Exception as e:
        st.error(f"Errore nell'analisi delle polizze: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_policy_detail_view():
    """Renderizza la vista dettagliata di una polizza"""
    if 'selected_policy' not in st.session_state:
        return
    
    try:
        policy_id = st.session_state.selected_policy
        policy_data = api_client.get_policy(policy_id)
        
        st.subheader(f"Dettagli Polizza #{policy_id}")
        
        # Pulsante per tornare alla lista
        if st.button("⬅ Torna alla Lista"):
            del st.session_state.selected_policy
            st.rerun()
        
        # Visualizza dettagli polizza
        render_policy_details(policy_data)
        
        # Sezione sinistri della polizza
        st.subheader("Sinistri Associati")
        try:
            claims_data = api_client.get_claims({"policy_id": policy_id})
            
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
                st.info(" Nessun sinistro registrato per questa polizza")
                
        except Exception as e:
            st.error(f"Errore nel caricamento sinistri: {str(e)}")
        
        # Sezione premi della polizza
        st.subheader("Premi Associati")
        try:
            premiums_data = api_client.get_policy_premiums(policy_id)
            
            if premiums_data:
                df_premiums = pd.DataFrame(premiums_data)
                
                # Formatta i dati per visualizzazione
                if 'due_date' in df_premiums.columns:
                    df_premiums['due_date_formatted'] = df_premiums['due_date'].apply(DataFormatter.format_date)
                if 'payment_date' in df_premiums.columns:
                    df_premiums['payment_date_formatted'] = df_premiums['payment_date'].apply(DataFormatter.format_date)
                if 'amount' in df_premiums.columns:
                    df_premiums['amount_formatted'] = df_premiums['amount'].apply(DataFormatter.format_currency)
                
                # Visualizza tabella premi
                st.dataframe(
                    df_premiums[['amount_formatted', 'due_date_formatted', 'payment_date_formatted', 
                               'payment_status']],
                    use_container_width=True
                )
            else:
                st.info(" Nessun premio registrato per questa polizza")
                
        except Exception as e:
            st.error(f"Errore nel caricamento premi: {str(e)}")
        
        # Sezione sottoscrittori
        st.subheader("Sottoscrittori")
        try:
            if policy_data.get('primary_subscriber_id'):
                subscriber_data = api_client.get_policy_subscriber(policy_data['primary_subscriber_id'])
                
                if subscriber_data:
                    st.write("**Sottoscrittore Principale:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        if subscriber_data.get('entity_type') == 'company':
                            st.write(f"**Azienda:** {subscriber_data.get('company_name', 'N/A')}")
                            st.write(f"**Partita IVA:** {subscriber_data.get('vat_number', 'N/A')}")
                        else:
                            st.write(f"**Nome:** {subscriber_data.get('first_name', 'N/A')} {subscriber_data.get('last_name', 'N/A')}")
                            st.write(f"**Codice Fiscale:** {subscriber_data.get('fiscal_code', 'N/A')}")
                    with col2:
                        st.write(f"**Email:** {subscriber_data.get('email', 'N/A')}")
                        st.write(f"**Telefono:** {subscriber_data.get('phone', 'N/A')}")
                        st.write(f"**Cellulare:** {subscriber_data.get('mobile', 'N/A')}")
                else:
                    st.info(" Sottoscrittore principale non trovato")
            else:
                st.info(" Nessun sottoscrittore principale associato a questa polizza")
                
        except Exception as e:
            st.error(f"Errore nel caricamento sottoscrittori: {str(e)}")
        
        # Sezione delegati pagamento
        st.subheader("Delegati al Pagamento")
        try:
            if policy_data.get('premium_delegate_id'):
                delegate_data = api_client.get_premium_delegate(policy_data['premium_delegate_id'])
                
                if delegate_data:
                    st.write("**Delegato al Pagamento:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        if delegate_data.get('delegate_type') == 'company':
                            st.write(f"**Azienda:** {delegate_data.get('company_name', 'N/A')}")
                            st.write(f"**Partita IVA:** {delegate_data.get('vat_number', 'N/A')}")
                        else:
                            st.write(f"**Nome:** {delegate_data.get('first_name', 'N/A')} {delegate_data.get('last_name', 'N/A')}")
                            st.write(f"**Codice Fiscale:** {delegate_data.get('fiscal_code', 'N/A')}")
                    with col2:
                        st.write(f"**Email:** {delegate_data.get('email', 'N/A')}")
                        st.write(f"**Telefono:** {delegate_data.get('phone', 'N/A')}")
                        st.write(f"**Cellulare:** {delegate_data.get('mobile', 'N/A')}")
                        
                        # Informazioni autorizzazione
                        if delegate_data.get('authorization_start'):
                            try:
                                auth_start = datetime.fromisoformat(delegate_data['authorization_start'].replace('Z', '+00:00'))
                                st.write(f"**Autorizzazione Da:** {auth_start.strftime('%d/%m/%Y')}")
                            except:
                                st.write(f"**Autorizzazione Da:** {delegate_data.get('authorization_start', 'N/A')}")
                        
                        if delegate_data.get('authorization_end'):
                            try:
                                auth_end = datetime.fromisoformat(delegate_data['authorization_end'].replace('Z', '+00:00'))
                                st.write(f"**Autorizzazione A:** {auth_end.strftime('%d/%m/%Y')}")
                            except:
                                st.write(f"**Autorizzazione A:** {delegate_data.get('authorization_end', 'N/A')}")
                        
                        st.write(f"**Attivo:** {'Sì' if delegate_data.get('is_active', False) else 'No'}")
                else:
                    st.info(" Delegato al pagamento non trovato")
            else:
                st.info(" Nessun delegato al pagamento associato a questa polizza")
                
        except Exception as e:
            st.error(f"Errore nel caricamento delegati: {str(e)}")
        
    except Exception as e:
        st.error(f"Errore nel caricamento dettagli polizza: {str(e)}")
        if st.button("⬅ Torna alla Lista"):
            del st.session_state.selected_policy
            st.rerun()

# Esportazioni
__all__ = ['policies_page', 'render_policy_detail_view']

# Esegui la pagina se richiamata direttamente
if __name__ == "__main__":
    policies_page()