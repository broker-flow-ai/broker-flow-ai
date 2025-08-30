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
from components.claim_card import render_claim_card, render_claim_details, render_claim_form
from components.filters import render_claim_filters

@require_role(allowed_roles=["admin", "broker", "claims_adjuster", "customer_service"])
def claims_page():
    """Pagina principale gestione sinistri"""
    st.title("🚨 Gestione Sinistri")
    
    # Controlla se dobbiamo mostrare la vista dettagliata
    if 'selected_claim' in st.session_state:
        render_claim_detail_view()
        return
    
    # Controlla se dobbiamo mostrare il form di modifica
    if 'editing_claim' in st.session_state:
        render_new_claim_form()
        return
    
    # Tabs per diverse funzionalità
    tab1, tab2, tab3 = st.tabs(["📋 Lista Sinistri", "➕ Nuovo Sinistro", "📊 Analisi Sinistri"])
    
    with tab1:
        render_claims_list()
    
    with tab2:
        render_new_claim_form()
    
    with tab3:
        render_claims_analysis()

def render_claims_list():
    """Renderizza la lista dei sinistri con filtri"""
    st.subheader("Lista Sinistri")
    
    # Applica filtri
    filters = render_claim_filters()
    
    try:
        # Recupera sinistri dal backend
        claims_data = api_client.get_claims(filters)
        
        if not claims_data:
            st.info(" Nessun sinistro trovato con i filtri selezionati")
            return
        
        # Converti in DataFrame per facilitare la gestione
        df = pd.DataFrame(claims_data)
        
        # Formatta i dati per la visualizzazione
        if 'claim_date' in df.columns:
            df['claim_date_formatted'] = df['claim_date'].apply(DataFormatter.format_date)
        if 'amount' in df.columns:
            df['amount_formatted'] = df['amount'].apply(DataFormatter.format_currency)
        
        # Visualizza i sinistri come cards
        st.subheader(f"Sinistri ({len(df)} trovati)")
        
        # Pagination
        items_per_page = 10
        total_pages = (len(df) - 1) // items_per_page + 1
        current_page = st.session_state.get('claim_page', 1)
        
        # Controlli di navigazione
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⏮ Prima") and current_page > 1:
                current_page = 1
                st.session_state.claim_page = current_page
        
        with col2:
            # Solo mostra lo slider se ci sono più pagine
            if total_pages > 1:
                page_selection = st.slider(
                    "Pagina",
                    min_value=1,
                    max_value=total_pages,
                    value=current_page,
                    key="claim_page_slider"
                )
                current_page = page_selection
                st.session_state.claim_page = current_page
            else:
                st.write(f"Pagina {current_page} di {total_pages}")
        
        with col3:
            if st.button("Ultima ⏭") and current_page < total_pages:
                current_page = total_pages
                st.session_state.claim_page = current_page
        
        # Calcola indici per la pagina corrente
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(df))
        
        # Visualizza sinistri della pagina corrente
        page_claims = df.iloc[start_idx:end_idx]
        
        for _, claim in page_claims.iterrows():
            render_claim_card(claim.to_dict())
            
            # Pulsanti di azione per ogni sinistro
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"👁 Dettagli #{claim['id']}", key=f"view_claim_{claim['id']}"):
                    st.session_state.selected_claim = claim['id']
                    st.rerun()
            with col2:
                if st.button(f"✏ Modifica #{claim['id']}", key=f"edit_claim_{claim['id']}"):
                    st.session_state.editing_claim = claim['id']
                    st.rerun()
            with col3:
                if has_delete_permission() and st.button(f"🗑 Elimina #{claim['id']}", key=f"delete_claim_{claim['id']}"):
                    st.warning(f"Eliminazione sinistro #{claim['id']} non ancora implementata")
            
            st.markdown("---")
        
        # Informazioni paginazione
        st.caption(f"Visualizzati sinistri {start_idx + 1}-{end_idx} di {len(df)} totali")
        
    except Exception as e:
        st.error(f"Errore nel caricamento dei sinistri: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_new_claim_form():
    """Renderizza il form per creare un nuovo sinistro"""
    st.subheader("Nuovo Sinistro")
    
    # Recupera dati esistenti se si sta modificando
    claim_data = None
    if 'editing_claim' in st.session_state:
        try:
            claim_data = api_client.get_claim(st.session_state.editing_claim)
        except Exception as e:
            st.error(f"Errore nel caricamento sinistro: {str(e)}")
            del st.session_state.editing_claim
    
    # Renderizza form sinistro
    form_data = render_claim_form(claim_data)
    
    # Pulsanti di azione
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Salva Sinistro"):
            # Validazione dati
            is_valid, errors = Validators.validate_claim_data(form_data)
            
            if not is_valid:
                for error in errors:
                    st.error(error)
            else:
                try:
                    if claim_data:
                        # Aggiorna sinistro esistente
                        result = api_client.update_claim(st.session_state.editing_claim, form_data)
                        st.success(f"Sinistro aggiornato con successo! ID: {result.get('claim_id', 'N/A')}")
                        del st.session_state.editing_claim
                    else:
                        # Crea nuovo sinistro
                        result = api_client.create_claim(form_data)
                        st.success(f"Sinistro creato con successo! ID: {result.get('claim_id', 'N/A')}")
                    
                    # Reset form
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Errore nel salvataggio del sinistro: {str(e)}")
    
    with col2:
        if st.button("❌ Annulla"):
            if 'editing_claim' in st.session_state:
                del st.session_state.editing_claim
            st.rerun()
    
    with col3:
        st.write("")  # Spazio vuoto per allineamento

def render_claims_analysis():
    """Renderizza l'analisi dei sinistri"""
    st.subheader("Analisi Sinistri")
    
    try:
        # Recupera tutti i sinistri per l'analisi
        claims_data = api_client.get_claims()
        
        if not claims_data:
            st.info(" Nessun sinistro disponibile per l'analisi")
            return
        
        df = pd.DataFrame(claims_data)
        
        # Analisi per stato sinistro
        if 'status' in df.columns:
            status_counts = df['status'].value_counts()
            
            st.subheader("Distribuzione Sinistri per Stato")
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Sinistri per Stato"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Analisi per importo sinistro
        if 'amount' in df.columns:
            df['amount_float'] = pd.to_numeric(df['amount'], errors='coerce')
            df_amount = df.dropna(subset=['amount_float'])
            
            if not df_amount.empty:
                st.subheader("Distribuzione Importi Sinistri")
                fig_amount = px.histogram(
                    df_amount,
                    x='amount_float',
                    nbins=20,
                    title="Distribuzione Importi Sinistri",
                    labels={'amount_float': 'Importo (€)', 'count': 'Numero Sinistri'}
                )
                st.plotly_chart(fig_amount, use_container_width=True)
        
        # Analisi temporale
        if 'claim_date' in df.columns:
            df['claim_date_parsed'] = pd.to_datetime(df['claim_date'], errors='coerce')
            df_temporal = df.dropna(subset=['claim_date_parsed'])
            
            if not df_temporal.empty:
                df_temporal['claim_month'] = df_temporal['claim_date_parsed'].dt.to_period('M')
                monthly_counts = df_temporal['claim_month'].value_counts().sort_index()
                
                st.subheader("Andamento Sinistri nel Tempo")
                fig_timeline = px.line(
                    x=monthly_counts.index.astype(str),
                    y=monthly_counts.values,
                    labels={'x': 'Mese', 'y': 'Numero Sinistri'},
                    title="Sinistri Mensili"
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Analisi per tipo polizza
        if 'policy_info' in df.columns:
            # Estrai tipo rischio dalle informazioni polizza
            df['risk_type'] = df['policy_info'].apply(
                lambda x: x.get('risk_type', 'N/A') if isinstance(x, dict) else 'N/A'
            )
            
            risk_counts = df['risk_type'].value_counts()
            
            st.subheader("Sinistri per Tipo Rischio")
            fig_risk = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                labels={'x': 'Tipo Rischio', 'y': 'Numero Sinistri'},
                title="Sinistri per Tipo Rischio"
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        
        # Statistiche generali
        st.subheader("Statistiche Generali")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Totale Sinistri", len(df))
        col2.metric("Sinistri Aperti", len(df[df['status'] == 'open']) if 'status' in df.columns else 0)
        col3.metric("Importo Totale", f"€{df['amount'].sum():,.2f}" if 'amount' in df.columns else "€0.00")
        col4.metric("Sinistri Approvati", len(df[df['status'] == 'approved']) if 'status' in df.columns else 0)
        
    except Exception as e:
        st.error(f"Errore nell'analisi dei sinistri: {str(e)}")
        import traceback
        st.error(f"Dettagli errore: {traceback.format_exc()}")

def render_claim_detail_view():
    """Renderizza la vista dettagliata di un sinistro"""
    if 'selected_claim' not in st.session_state:
        return
    
    try:
        claim_id = st.session_state.selected_claim
        claim_data = api_client.get_claim(claim_id)
        
        st.subheader(f"Dettagli Sinistro #{claim_id}")
        
        # Pulsante per tornare alla lista
        if st.button("⬅ Torna alla Lista"):
            del st.session_state.selected_claim
            st.rerun()
        
        # Visualizza dettagli sinistro
        render_claim_details(claim_data)
        
        # Sezione documentazione sinistro
        st.subheader("Documentazione Sinistro")
        try:
            documents_data = api_client.get_claim_documents(claim_id)
            
            if documents_data:
                df_docs = pd.DataFrame(documents_data)
                
                # Formatta i dati per visualizzazione
                if 'uploaded_at' in df_docs.columns:
                    df_docs['uploaded_at_formatted'] = df_docs['uploaded_at'].apply(DataFormatter.format_datetime)
                
                # Visualizza tabella documenti
                st.dataframe(
                    df_docs[['document_name', 'document_type', 'uploaded_at_formatted', 'file_size']],
                    use_container_width=True
                )
                
                # Pulsanti per scaricare documenti
                for _, doc in df_docs.iterrows():
                    if st.button(f"📥 Scarica {doc['document_name']}", key=f"download_doc_{doc['id']}"):
                        st.info(f"Download di {doc['document_name']} non ancora implementato")
            else:
                st.info(" Nessun documento associato a questo sinistro")
                
        except Exception as e:
            st.error(f"Errore nel caricamento documenti: {str(e)}")
        
        # Sezione comunicazioni sinistro
        st.subheader("Comunicazioni Sinistro")
        try:
            communications_data = api_client.get_claim_communications(claim_id)
            
            if communications_data:
                df_comms = pd.DataFrame(communications_data)
                
                # Formatta i dati per visualizzazione
                if 'sent_at' in df_comms.columns:
                    df_comms['sent_at_formatted'] = df_comms['sent_at'].apply(DataFormatter.format_datetime)
                
                # Visualizza tabella comunicazioni
                st.dataframe(
                    df_comms[['sender', 'recipient', 'subject', 'sent_at_formatted', 'status']],
                    use_container_width=True
                )
                
                # Pulsante per inviare nuova comunicazione
                if st.button("✉ Nuova Comunicazione"):
                    st.info("Invio comunicazione non ancora implementato")
            else:
                st.info(" Nessuna comunicazione registrata per questo sinistro")
                
                # Pulsante per inviare prima comunicazione
                if st.button("✉ Invia Prima Comunicazione"):
                    st.info("Invio comunicazione non ancora implementato")
                
        except Exception as e:
            st.error(f"Errore nel caricamento comunicazioni: {str(e)}")
        
    except Exception as e:
        st.error(f"Errore nel caricamento dettagli sinistro: {str(e)}")
        if st.button("⬅ Torna alla Lista"):
            del st.session_state.selected_claim
            st.rerun()

# Esportazioni
__all__ = ['claims_page', 'render_claim_detail_view']

# Esegui la pagina se richiamata direttamente
if __name__ == "__main__":
    claims_page()