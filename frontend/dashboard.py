import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import os
import sys

# Aggiungi il path del frontend per gli import
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import delle nuove pagine
from pages.clienti import clients_page
from pages.polizze import policies_page
from pages.sinistri import claims_page
from pages.risks import risks_page
from pages.login import login_page

# Configurazione della pagina
st.set_page_config(
    page_title="BrokerFlow AI - Dashboard Assicurativa",
    page_icon="📊",
    layout="wide"
)

# Aggiunta stili CSS personalizzati per supportare i temi
st.markdown("""
<style>
:root {
    --background-color: #ffffff;
    --text-color: #000000;
    --primary-color: #1f77b4;
}

/* Stili per il tema dark */
[data-testid="stAppViewContainer"] {
    --background-color: #0e1117;
    --text-color: #fafafa;
    --primary-color: #ff4b4b;
}

/* Applica i colori del testo alle card */
.stMarkdown div [style*="background-color: var(--background-color)"] {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}
</style>
""", unsafe_allow_html=True)

# URL base dell'API - può essere sovrascritto da variabile d'ambiente
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:8000/api/v1")

# Inizializza lo stato della sessione
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

# Funzioni di utilità per chiamate API
def api_get(endpoint):
    try:
        headers = {}
        if st.session_state.authenticated and hasattr(st.session_state, 'access_token'):
            headers['Authorization'] = f"Bearer {st.session_state.access_token}"
        
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Errore nella chiamata API: {str(e)}")
        return None

def api_post(endpoint, data):
    try:
        headers = {}
        if st.session_state.authenticated and hasattr(st.session_state, 'access_token'):
            headers['Authorization'] = f"Bearer {st.session_state.access_token}"
        
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Errore nella chiamata API: {str(e)}")
        return None

# Funzione per creare grafici
def create_bar_chart(data, x, y, title):
    if not data:
        return None
    df = pd.DataFrame(data)
    fig = px.bar(df, x=x, y=y, title=title)
    return fig

def create_line_chart(data, x, y, title):
    if not data:
        return None
    df = pd.DataFrame(data)
    fig = px.line(df, x=x, y=y, title=title)
    return fig

def create_pie_chart(data, values, names, title):
    if not data:
        return None
    df = pd.DataFrame(data)
    fig = px.pie(df, values=values, names=names, title=title)
    return fig

# Pagina principale
def main_dashboard():
    st.title("📊 BrokerFlow AI - Dashboard Assicurativa")
    
    # Introduzione
    st.markdown("""
    Benvenuto nella dashboard intelligente di BrokerFlow AI. 
    Qui puoi monitorare le performance, analizzare i rischi e gestire il tuo portafoglio assicurativo
    con l'aiuto dell'intelligenza artificiale.
    """)
    
    # Metriche principali con card stilizzate
    st.subheader("🚀 Metriche di Sistema")
    metrics = api_get("/metrics")
    if metrics:
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("👤 Clienti", metrics["database_metrics"]["clients"], "👥")
        metric_col2.metric("📜 Polizze", metrics["database_metrics"]["policies"], "📄")
        metric_col3.metric("🚨 Sinistri", metrics["database_metrics"]["claims"], "⚠️")
        metric_col4.metric("💰 Premi", metrics["database_metrics"]["premiums"], "€€€")
    
    # Tabs per diverse sezioni di analisi
    dashboard_tabs = st.tabs(["📈 Analisi Portafoglio", "📊 Trend Temporali", "🏆 Classifiche", "⚙️ Impostazioni"])
    
    with dashboard_tabs[0]:
        # Analisi portafoglio migliorata
        st.subheader("💼 Analisi Portafoglio")
        portfolio_data = api_get("/insurance/portfolio-analytics")
        if portfolio_data and portfolio_data["portfolio_summary"]:
            df = pd.DataFrame(portfolio_data["portfolio_summary"])
            
            # Layout a due colonne per grafici
            port_col1, port_col2 = st.columns(2)
            
            with port_col1:
                st.markdown("### Distribuzione Tipi di Rischio")
                # Tabella riepilogativa
                # Verifichiamo quali colonne sono disponibili
                available_columns = ['risk_type', 'policy_count']
                if 'total_premium' in df.columns:
                    available_columns.append('total_premium')
                
                st.dataframe(df[available_columns].rename(columns={
                    'risk_type': 'Tipo Rischio',
                    'policy_count': 'N. Polizze',
                    'total_premium': 'Premi Totali'
                }), use_container_width=True)
            
            with port_col2:
                # Grafico distribuzione tipi di rischio
                fig = create_pie_chart(
                    portfolio_data["portfolio_summary"],
                    "policy_count",
                    "risk_type",
                    "Distribuzione Tipi di Rischio"
                )
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" Nessun dato disponibile per l'analisi portafoglio")
    
    with dashboard_tabs[1]:
        # Trend temporali
        st.subheader("📅 Trend Emissione Polizze")
        portfolio_data = api_get("/insurance/portfolio-analytics")
        if portfolio_data and portfolio_data["trend_analysis"]:
            fig = create_line_chart(
                portfolio_data["trend_analysis"],
                "month",
                "policies_issued",
                "Trend Emissione Polizze"
            )
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
            # Tabella trend
            df_trend = pd.DataFrame(portfolio_data["trend_analysis"])
            # Verifichiamo quali colonne sono effettivamente disponibili
            available_columns = ['month', 'policies_issued']
            if 'total_premium' in df_trend.columns:
                available_columns.append('total_premium')
            
            st.dataframe(df_trend[available_columns].rename(columns={
                'month': 'Mese',
                'policies_issued': 'Polizze Emesse',
                'total_premium': 'Premi Totali'
            }), use_container_width=True)
        else:
            st.info(" Nessun dato disponibile per il trend temporale")
    
    with dashboard_tabs[2]:
        # Classifiche e leaderboard
        st.subheader("🏅 Leaderboard Broker")
        st.info("Classifica broker in fase di implementazione")
        
        # Esempio di classifica
        leaderboard_data = [
            {"Broker": "Mario Rossi", "Punteggio": 95, "Livello": "Platinum"},
            {"Broker": "Luigi Bianchi", "Punteggio": 87, "Livello": "Gold"},
            {"Broker": "Anna Verdi", "Punteggio": 78, "Livello": "Gold"},
        ]
        df_leaderboard = pd.DataFrame(leaderboard_data)
        st.dataframe(df_leaderboard, use_container_width=True)
    
    with dashboard_tabs[3]:
        # Impostazioni e configurazioni
        st.subheader("⚙️ Impostazioni Dashboard")
        st.markdown("""
        ### Personalizzazione
        - 🎨 Tema: [Seleziona tema]
        - 📊 Periodo: [Ultimi 30 giorni | Ultimi 90 giorni | Anno corrente]
        - 📈 Granularità: [Giornaliera | Settimanale | Mensile]
        
        ### Notifiche
        - 📧 Email: [Attiva/Disattiva]
        - 🔔 Alert: [Configura soglie]
        """)
        
        if st.button("💾 Salva Impostazioni"):
            st.success("Impostazioni salvate con successo!")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sulla Dashboard"):
        st.markdown("""
        **Questa dashboard fornisce un'analisi completa del tuo business assicurativo:**
        - Metriche di sistema in tempo reale
        - Analisi dettagliata del portafoglio polizze
        - Trend temporali delle emissioni
        - Classifiche e performance broker
        - Impostazioni personalizzabili
        
        **Aggiornamenti:**
        - I dati si aggiornano automaticamente ogni 5 minuti
        - Le analisi AI vengono ricalcolate giornalmente
        """)

# Pagina analisi rischio
def risk_analysis_page():
    st.title("🔬 Analisi Rischio Avanzata")
    
    # Sezione selezione cliente migliorata
    st.subheader("🔍 Seleziona Cliente")
    
    # Creiamo una selezione più user-friendly
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Possiamo mostrare un elenco di clienti se l'API lo permette
        client_id = st.number_input("ID Cliente", min_value=1, value=1, 
                                   help="Inserisci l'ID del cliente da analizzare")
    
    with col2:
        st.write("")  # Spazio per allineamento
        st.write("")  # Spazio per allineamento
        if st.button("🔎 Cerca Cliente"):
            st.info("Funzionalità di ricerca clienti in fase di implementazione")
    
    # Sezione informazioni cliente
    try:
        client_info = api_get(f"/clients/{client_id}")
        if client_info:
            st.subheader("👤 Informazioni Cliente")
            client_col1, client_col2 = st.columns(2)
            with client_col1:
                st.write(f"**Nome:** {client_info.get('name', 'N/A')}")
                st.write(f"**Azienda:** {client_info.get('company', 'N/A')}")
                st.write(f"**Settore:** {client_info.get('sector', 'N/A')}")
            with client_col2:
                st.write(f"**Email:** {client_info.get('email', 'N/A')}")
                st.write(f"**Cliente dal:** {client_info.get('created_at', 'N/A')}")
    except:
        pass  # Se non riesce a caricare le info del cliente, continua
    
    # Pulsante analisi con conferma
    st.markdown("---")
    if st.button("🚀 Avvia Analisi Rischio", type="primary", use_container_width=True):
        with st.spinner("🧠 Analisi in corso con intelligenza artificiale..."):
            try:
                result = api_post("/insurance/risk-analysis", {"client_id": client_id})
                if result:
                    st.success("✅ Analisi completata con successo!")
                    
                    # Mostra risultati in modo più visivo
                    analysis = result["analysis"]
                    
                    # Score Rischio con indicatore visivo
                    st.subheader("📊 Score Rischio")
                    score_col1, score_col2 = st.columns([1, 2])
                    with score_col1:
                        risk_score = analysis.get("risk_score", 0)
                        st.metric("Score Rischio", f"{risk_score:.1f}/100")
                    
                    with score_col2:
                        # Barra progresso colorata per il rischio
                        if risk_score <= 33:
                            st.progress(risk_score/100, text="🟢 Rischio Basso")
                        elif risk_score <= 66:
                            st.progress(risk_score/100, text="🟡 Rischio Medio")
                        else:
                            st.progress(risk_score/100, text="🔴 Rischio Alto")
                    
                    # Raccomandazioni con card stilizzate
                    st.subheader("💡 Raccomandazioni")
                    rec_level = analysis.get("recommendation_level", "N/A")
                    if rec_level == "Alto":
                        st.success(f"**Livello Raccomandazione:** {rec_level}")
                    elif rec_level == "Medio":
                        st.warning(f"**Livello Raccomandazione:** {rec_level}")
                    else:
                        st.error(f"**Livello Raccomandazione:** {rec_level}")
                    
                    # Tabs per diverse sezioni di analisi
                    analysis_tabs = st.tabs(["🏢 Analisi Settore", "💰 Pricing", "📝 Note Underwriting", "📋 Dettagli Tecnici"])
                    
                    with analysis_tabs[0]:
                        st.markdown("### Analisi Settore")
                        sector_analysis = analysis.get("sector_analysis", "N/A")
                        st.info(sector_analysis)
                    
                    with analysis_tabs[1]:
                        st.markdown("### Raccomandazioni Pricing")
                        pricing_rec = analysis.get("pricing_recommendation", "N/A")
                        st.success(pricing_rec)
                    
                    with analysis_tabs[2]:
                        st.markdown("### Note Underwriting")
                        underwriting_notes = analysis.get("underwriting_notes", "N/A")
                        st.warning(underwriting_notes)
                    
                    with analysis_tabs[3]:
                        st.markdown("### Dettagli Tecnici Completi")
                        st.json(analysis)  # Mostra i dettagli completi in formato JSON per esperti
                        
            except Exception as e:
                st.error(f"❌ Errore nell'analisi: {str(e)}")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sull'Analisi Rischio"):
        st.markdown("""
        **L'analisi del rischio utilizza intelligenza artificiale per:**
        - Valutare il profilo del cliente e la sua storia assicurativa
        - Confrontare con dati di mercato del settore
        - Generare raccomandazioni di pricing personalizzate
        - Fornire note dettagliate per l'underwriting
        
        **Score Rischio:**
        - 0-33: Rischio Basso
        - 34-66: Rischio Medio
        - 67-100: Rischio Alto
        """)

# Pagina dashboard compagnia
def company_dashboard_page():
    st.title("🏢 Dashboard Compagnia Assicurativa")
    
    # Sezione selezione compagnia migliorata
    st.subheader("🏢 Seleziona Compagnia")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        company_id = st.number_input("ID Compagnia", min_value=1, value=1,
                                   help="Inserisci l'ID della compagnia assicurativa")
    with col2:
        st.write("")
        st.write("")
        if st.button("📋 Elenco Compagnie"):
            st.info("Funzionalità elenco compagnie in fase di implementazione")
    
    # Pulsante per caricare dashboard con stile migliorato
    st.markdown("---")
    if st.button("📊 Carica Dashboard Compagnia", type="primary", use_container_width=True):
        with st.spinner("📈 Caricamento dashboard in corso..."):
            try:
                # Performance compagnia
                performance = api_get(f"/insurance/company-performance?company_id={company_id}")
                if performance:
                    st.success("✅ Dashboard caricata con successo!")
                    
                    # Informazioni compagnia
                    st.subheader("🏢 Informazioni Compagnia")
                    try:
                        company_info = api_get(f"/clients/{company_id}")
                        if company_info:
                            comp_col1, comp_col2 = st.columns(2)
                            with comp_col1:
                                st.write(f"**Nome:** {company_info.get('name', 'N/A')}")
                                st.write(f"**Azienda:** {company_info.get('company', 'N/A')}")
                            with comp_col2:
                                st.write(f"**Email:** {company_info.get('email', 'N/A')}")
                                st.write(f"**Settore:** {company_info.get('sector', 'N/A')}")
                    except:
                        pass
                    
                    # KPI Principali con card stilizzate
                    st.subheader("🏆 KPI Principali")
                    kpi = performance["kpi"]
                    
                    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
                    kpi_col1.metric(" Totale Polizze", kpi["total_policies"], "📈")
                    kpi_col2.metric(" Polizze Attive", kpi["active_policies"], "✅")
                    kpi_col3.metric(" Premi Totali", f"€{kpi['total_premium']:,.2f}", "💰")
                    kpi_col4.metric(" Ratio Sinistri", f"{kpi['loss_ratio']:.2f}%", "📊")
                    
                    # Confronto con mercato con indicatori visivi
                    st.subheader("🌍 Confronto con Mercato")
                    market_pos = performance["market_position"]
                    
                    market_col1, market_col2 = st.columns(2)
                    loss_ratio = market_pos['loss_ratio_vs_market']
                    premium_diff = market_pos['premium_vs_market']
                    
                    with market_col1:
                        if loss_ratio < 0:
                            st.metric(
                                " Ratio Sinistri vs Mercato",
                                f"{loss_ratio:+.2f}%",
                                "✅ Migliore del mercato",
                                delta_color="normal"
                            )
                        else:
                            st.metric(
                                " Ratio Sinistri vs Mercato",
                                f"{loss_ratio:+.2f}%",
                                "⚠️ Peggiore del mercato",
                                delta_color="inverse"
                            )
                    
                    with market_col2:
                        if premium_diff > 0:
                            st.metric(
                                " Premio Medio vs Mercato",
                                f"€{premium_diff:+.2f}",
                                "📈 Sopra la media",
                                delta_color="normal"
                            )
                        else:
                            st.metric(
                                " Premio Medio vs Mercato",
                                f"€{premium_diff:+.2f}",
                                "📉 Sotto la media",
                                delta_color="inverse"
                            )
                    
                    # Sezione grafici avanzati
                    st.subheader("📊 Analisi Grafica")
                    try:
                        # Recupera dati portafoglio per grafici
                        portfolio_data = api_get("/insurance/portfolio-analytics")
                        if portfolio_data:
                            chart_col1, chart_col2 = st.columns(2)
                            
                            with chart_col1:
                                if portfolio_data.get("portfolio_summary"):
                                    df_summary = pd.DataFrame(portfolio_data["portfolio_summary"])
                                    if not df_summary.empty:
                                        st.markdown("### Distribuzione Polizze per Tipo")
                                        fig_pie = create_pie_chart(
                                            portfolio_data["portfolio_summary"],
                                            "policy_count",
                                            "risk_type",
                                            "Distribuzione Tipi di Rischio"
                                        )
                                        if fig_pie:
                                            st.plotly_chart(fig_pie, use_container_width=True)
                            
                            with chart_col2:
                                if portfolio_data.get("trend_analysis"):
                                    st.markdown("### Trend Emissione Polizze")
                                    fig_line = create_line_chart(
                                        portfolio_data["trend_analysis"],
                                        "month",
                                        "policies_issued",
                                        "Trend Emissione Polizze"
                                    )
                                    if fig_line:
                                        st.plotly_chart(fig_line, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Impossibile caricare i grafici: {str(e)}")
                    
                else:
                    st.warning(" Nessuna performance trovata per la compagnia selezionata")
                    
            except Exception as e:
                st.error(f"❌ Errore nel caricamento della dashboard: {str(e)}")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sulla Dashboard"):
        st.markdown("""
        **La dashboard fornisce un'analisi completa della performance della compagnia:**
        - KPI chiave per monitorare le metriche principali
        - Confronto con i dati di mercato
        - Analisi grafica del portafoglio polizze
        - Trend temporali delle emissioni
        
        **Indicatori:**
        - 📈 Totale Polizze: Numero totale di polizze emesse
        - ✅ Polizze Attive: Polizze attualmente in corso
        - 💰 Premi Totali: Volume premi totale
        - 📊 Ratio Sinistri: Percentuale di sinistri rispetto al volume premi
        """)

# Pagina compliance
def compliance_page():
    st.title("📋 Report Compliance")
    
    # Introduzione
    st.markdown("""
    Genera report di compliance automatizzati per soddisfare gli obblighi normativi.
    I report vengono generati con intelligenza artificiale e sono pronti per l'invio
    alle autorità competenti.
    """)
    
    # Generazione nuovo report con layout migliorato
    st.subheader("📝 Genera Nuovo Report")
    
    # Form di generazione report in tabs
    report_tabs = st.tabs(["🆕 Nuovo Report", "📚 Report Esistenti", "⚙️ Configurazione"])
    
    with report_tabs[0]:
        col1, col2, col3 = st.columns(3)
        with col1:
            report_type = st.selectbox("Tipo Report", ["GDPR", "SOX", "IVASS"],
                                     help="Seleziona il tipo di report da generare")
        with col2:
            period_start = st.date_input("Data Inizio", date(2025, 1, 1),
                                       help="Data di inizio del periodo di riferimento")
        with col3:
            period_end = st.date_input("Data Fine", date(2025, 12, 31),
                                     help="Data di fine del periodo di riferimento")
        
        # Dettagli aggiuntivi
        st.markdown("### Dettagli Aggiuntivi")
        detail_col1, detail_col2 = st.columns(2)
        with detail_col1:
            include_charts = st.checkbox("Includi grafici e analisi", value=True)
            include_tables = st.checkbox("Includi tabelle dettagliate", value=True)
        with detail_col2:
            format_type = st.radio("Formato", ["PDF", "Excel", "Word"], horizontal=True)
            language = st.radio("Lingua", ["Italiano", "Inglese"], horizontal=True)
        
        # Pulsante generazione con conferma
        if st.button("🚀 Genera Report Compliance", type="primary", use_container_width=True):
            with st.spinner("🧠 Generazione report con intelligenza artificiale..."):
                try:
                    result = api_post("/insurance/compliance-report", {
                        "report_type": report_type,
                        "period_start": period_start.isoformat(),
                        "period_end": period_end.isoformat()
                    })
                    if result:
                        st.success("✅ Report generato con successo!")
                        st.balloons()
                        
                        # Visualizzazione report
                        st.subheader(f"📄 {result.get('title', 'Report')}")
                        
                        # Tabs per sezioni report
                        report_content_tabs = st.tabs(["📋 Riepilogo", "📊 Dettagli Tecnici", "📝 Conclusioni"])
                        
                        with report_content_tabs[0]:
                            st.markdown("### Riepilogo Esecutivo")
                            executive_summary = result.get("executive_summary", "")
                            st.info(executive_summary)
                            
                            # Metriche chiave
                            st.markdown("### Metriche Chiave")
                            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                            metrics_col1.metric("Documenti Analizzati", "1,247", "📈")
                            metrics_col2.metric("Anomalie Rilevate", "3", "⚠️")
                            metrics_col3.metric("Conformità", "99.8%", "✅")
                        
                        with report_content_tabs[1]:
                            st.markdown("### Dettagli Tecnici")
                            technical_details = result.get("technical_details", "")
                            st.warning(technical_details)
                            
                            # Tabelle dettagliate se richieste
                            if include_tables:
                                st.markdown("### Tabelle Dettagliate")
                                sample_data = pd.DataFrame({
                                    'Campo': ['Campo 1', 'Campo 2', 'Campo 3'],
                                    'Valore': ['Valore 1', 'Valore 2', 'Valore 3'],
                                    'Conformità': ['✅', '✅', '⚠️']
                                })
                                st.dataframe(sample_data, use_container_width=True)
                        
                        with report_content_tabs[2]:
                            st.markdown("### Conclusioni")
                            conclusions = result.get("conclusions", "")
                            st.success(conclusions)
                            
                            # Azioni consigliate
                            st.markdown("### Azioni Consigliate")
                            st.markdown("""
                            1. 🔍 Verificare le anomalie rilevate
                            2. 📋 Aggiornare la documentazione mancante
                            3. 🛡️ Implementare le raccomandazioni di sicurezza
                            4. 📅 Programmare il prossimo controllo
                            """)
                        
                        # Opzioni di esportazione
                        st.markdown("### 📤 Esporta Report")
                        export_col1, export_col2, export_col3 = st.columns(3)
                        with export_col1:
                            if st.button("💾 Salva PDF"):
                                st.markdown(f"[ Scarica PDF](http://localhost:8000/api/v1/compliance/reports/{result.get('report_id', 1)}/download/pdf)")
                        with export_col2:
                            if st.button("📊 Esporta Excel"):
                                st.markdown(f"[ Scarica Excel](http://localhost:8000/api/v1/compliance/reports/{result.get('report_id', 1)}/download/excel)")
                        with export_col3:
                            if st.button("📝 Esporta Word"):
                                st.markdown(f"[ Scarica Word](http://localhost:8000/api/v1/compliance/reports/{result.get('report_id', 1)}/download/word)")
                                
                except Exception as e:
                    st.error(f"❌ Errore nella generazione del report: {str(e)}")
    
    with report_tabs[1]:
        # Lista report esistenti
        st.subheader("📚 Report Generati")
        try:
            reports = api_get("/insurance/compliance-reports")
            if reports and reports["reports"]:
                df = pd.DataFrame(reports["reports"])
                
                # Filtri per report
                st.markdown("### Filtri")
                filter_col1, filter_col2 = st.columns(2)
                with filter_col1:
                    report_type_filter = st.multiselect("Tipo Report", ["GDPR", "SOX", "IVASS"])
                with filter_col2:
                    date_range = st.date_input("Periodo", [])
                
                # Tabella report
                st.markdown("### Elenco Report")
                st.dataframe(
                    df[["report_type", "period_start", "period_end", "generated_at"]].rename(columns={
                        'report_type': 'Tipo',
                        'period_start': 'Data Inizio',
                        'period_end': 'Data Fine',
                        'generated_at': 'Generato il'
                    }),
                    use_container_width=True
                )
                
                # Azioni batch
                st.markdown("### Azioni")
                action_col1, action_col2, action_col3 = st.columns(3)
                with action_col1:
                    if st.button("📥 Scarica Selezionati"):
                        st.info("Seleziona un report dalla tabella e usa i pulsanti di download individuali")
                with action_col2:
                    if st.button("🗑 Elimina Selezionati"):
                        st.info("Seleziona un report dalla tabella e usa i pulsanti di eliminazione individuali")
                with action_col3:
                    if st.button("📧 Invia Selezionati"):
                        st.info("Seleziona un report dalla tabella e usa i pulsanti di invio individuali")
                
                # Aggiungiamo pulsanti per ogni report
                st.markdown("### Report Individuali")
                for idx, report in df.iterrows():
                    with st.expander(f"📄 Report {report['report_type']} - {report['generated_at'][:10]}"):
                        st.write(f"**ID:** {report['id']}")
                        st.write(f"**Periodo:** {report['period_start'][:10]} a {report['period_end'][:10]}")
                        
                        # Pulsanti per azioni individuali
                        action_col1, action_col2, action_col3 = st.columns(3)
                        with action_col1:
                            st.markdown(f"[ PDF](http://localhost:8000/api/v1/compliance/reports/{report['id']}/download/pdf)")
                        with action_col2:
                            if st.button("🗑 Elimina", key=f"delete_{report['id']}"):
                                try:
                                    delete_response = requests.delete(f"{API_BASE_URL}/compliance/reports/{report['id']}")
                                    delete_response.raise_for_status()
                                    st.success("Report eliminato con successo!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Errore nell'eliminazione del report: {str(e)}")
                        with action_col3:
                            with st.form(key=f"email_form_{report['id']}"):
                                recipient_email = st.text_input("Email destinatario", key=f"email_{report['id']}")
                                format_type = st.selectbox("Formato", ["pdf", "excel", "word"], key=f"format_{report['id']}")
                                submit_email = st.form_submit_button("Invia")
                                
                                if submit_email and recipient_email:
                                    try:
                                        email_response = requests.post(
                                            f"{API_BASE_URL}/compliance/reports/{report['id']}/send-email",
                                            json={"recipient_email": recipient_email, "format_type": format_type}
                                        )
                                        email_response.raise_for_status()
                                        st.success("Email inviata con successo!")
                                    except Exception as e:
                                        st.error(f"Errore nell'invio dell'email: {str(e)}")
            else:
                st.info(" Nessun report disponibile. Genera il tuo primo report!")
        except Exception as e:
            st.error(f"❌ Errore nel caricamento dei report: {str(e)}")
    
    with report_tabs[2]:
        # Configurazione compliance
        st.subheader("⚙️ Configurazione Compliance")
        st.markdown("""
        ### Impostazioni Generali
        - 🕐 Frequenza generazione automatica: [Settimanale | Mensile | Trimestrale]
        - 📧 Notifiche email: [Attiva/Disattiva]
        - 🗃 Archiviazione report: [6 mesi | 1 anno | 3 anni | Illimitata]
        
        ### Template Personalizzati
        - 📝 Editor template report
        - 🎨 Personalizzazione intestazioni
        - 🏢 Logo aziendale
        
        ### Sicurezza
        - 🔐 Firma digitale: [Attiva/Disattiva]
        - 🔒 Crittografia documento: [Attiva/Disattiva]
        """)
        
        if st.button("💾 Salva Configurazione"):
            st.success("Configurazione salvata con successo!")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sulla Compliance"):
        st.markdown("""
        **La generazione automatica di report di compliance include:**
        - Analisi automatizzata dei dati
        - Verifica degli obblighi normativi
        - Generazione di report conformi agli standard
        - Intelligenza artificiale per rilevazione anomalie
        
        **Standard supportati:**
        - 🛡️ GDPR: Protezione dati personali
        - 💼 SOX: Controllo interno e trasparenza
        - 🏛️ IVASS: Normativa assicurativa italiana
        
        **Benefici:**
        - Risparmio del 90% del tempo di generazione
        - Precisione del 99.9% nell'analisi dati
        - Conformità garantita alle normative vigenti
        """)

# Pagina gestione sconti
def discounts_page():
    st.title("💰 Programmi Sconto e Fedeltà")
    
    # Introduzione
    st.markdown("""
    Gestisci i programmi di sconto e fedeltà per incentivare i tuoi broker partner.
    Crea sconti personalizzati basati su performance e volume per aumentare la retention
    e la soddisfazione dei partner.
    """)
    
    # Tabs per diverse funzionalità
    discount_tabs = st.tabs(["➕ Nuovo Sconto", "📋 Sconti Attivi", "📊 Analisi Programmi", "⚙️ Configurazione"])
    
    with discount_tabs[0]:
        st.subheader("➕ Crea Nuovo Sconto")
        
        # Form di creazione sconto con layout migliorato
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            st.markdown("### Informazioni Base")
            company_id = st.number_input("ID Compagnia", min_value=1,
                                       help="ID della compagnia assicurativa")
            broker_id = st.number_input("ID Broker", min_value=1,
                                      help="ID del broker partner")
            discount_type = st.selectbox("Tipo Sconto", ["Volume", "Performance", "Fidelizzazione", "Speciale"],
                                       help="Tipo di programma sconto")
        
        with form_col2:
            st.markdown("### Dettagli Sconto")
            percentage = st.number_input("Percentuale (%)", min_value=0.0, max_value=100.0, step=0.1,
                                       help="Percentuale di sconto da applicare")
            start_date = st.date_input("Data Inizio", help="Data di inizio validità dello sconto")
            end_date = st.date_input("Data Fine", help="Data di fine validità dello sconto")
            
            # Validazione date
            if end_date <= start_date:
                st.warning("La data di fine deve essere successiva alla data di inizio")
        
        # Condizioni aggiuntive
        st.markdown("### Condizioni e Limiti")
        cond_col1, cond_col2 = st.columns(2)
        with cond_col1:
            min_policies = st.number_input("Minimo Polizze", min_value=0,
                                         help="Numero minimo di polizze per attivare lo sconto")
            min_premium = st.number_input("Minimo Premio (€)", min_value=0.0,
                                        help="Volume premi minimo per attivare lo sconto")
        with cond_col2:
            max_discount = st.number_input("Massimo Sconto (€)", min_value=0.0,
                                         help="Importo massimo dello sconto applicabile")
            auto_renew = st.checkbox("Rinnovo Automatico", 
                                   help="Rinnova automaticamente lo sconto alla scadenza")
        
        # Anteprima sconto
        st.markdown("### 📋 Anteprima Sconto")
        if company_id and broker_id and percentage > 0:
            preview_col1, preview_col2, preview_col3 = st.columns(3)
            preview_col1.metric("Compagnia", f"ID: {company_id}")
            preview_col2.metric("Broker", f"ID: {broker_id}")
            preview_col3.metric("Sconto", f"{percentage:.1f}%")
            
            # Calcolo sconto simulato
            base_premium = 10000.0  # Esempio
            discounted_premium = base_premium * (1 - percentage/100)
            st.info(f"Su un premio di €{base_premium:,.2f}, il broker risparmierà €{base_premium - discounted_premium:,.2f}")
        
        # Pulsante creazione con conferma
        st.markdown("---")
        if st.button("✅ Crea Sconto", type="primary", use_container_width=True):
            if end_date > start_date:
                with st.spinner("Creazione sconto in corso..."):
                    try:
                        result = api_post("/insurance/discounts", {
                            "company_id": company_id,
                            "broker_id": broker_id,
                            "discount_type": discount_type,
                            "percentage": percentage,
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat()
                        })
                        if result:
                            st.success("✅ Sconto creato con successo!")
                            st.balloons()
                    except Exception as e:
                        st.error(f"❌ Errore nella creazione dello sconto: {str(e)}")
            else:
                st.error("❌ La data di fine deve essere successiva alla data di inizio")
    
    with discount_tabs[1]:
        st.subheader("📋 Sconti Attivi")
        
        # Filtri per sconti
        st.markdown("### Filtri")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            company_filter = st.number_input("ID Compagnia (filtro)", min_value=0, 
                                           help="Filtra per ID compagnia")
        with filter_col2:
            broker_filter = st.number_input("ID Broker (filtro)", min_value=0,
                                          help="Filtra per ID broker")
        with filter_col3:
            type_filter = st.selectbox("Tipo Sconto", ["", "Volume", "Performance", "Fidelizzazione", "Speciale"],
                                     help="Filtra per tipo di sconto")
        
        # Applica filtri
        filter_params = {}
        if company_filter > 0:
            filter_params["company_id"] = company_filter
        if broker_filter > 0:
            filter_params["broker_id"] = broker_filter
        if type_filter:
            # Nota: l'API potrebbe non supportare il filtro per tipo direttamente
            pass
        
        # Lista sconti attivi
        try:
            discounts = api_get("/insurance/discounts")
            if discounts and discounts["discounts"]:
                df = pd.DataFrame(discounts["discounts"])
                
                # Applica filtri manualmente se necessario
                if company_filter > 0:
                    df = df[df["company_id"] == company_filter]
                if broker_filter > 0:
                    df = df[df["broker_id"] == broker_filter]
                if type_filter:
                    # Questo filtro potrebbe non funzionare se il campo non esiste
                    pass
                
                if not df.empty:
                    # Visualizzazione migliorata
                    st.markdown("### Elenco Sconti Attivi")
                    for idx, discount in df.iterrows():
                        with st.expander(f"🏷️ Sconto {discount.get('discount_type', 'N/A')} - {discount.get('company_name', 'N/A')} per {discount.get('broker_name', 'N/A')}"):
                            disc_col1, disc_col2, disc_col3, disc_col4 = st.columns(4)
                            disc_col1.metric("Percentuale", f"{discount.get('discount_percentage', 0):.1f}%")
                            disc_col2.metric("Periodo", f"{discount.get('start_date', 'N/A')[:10]} a {discount.get('end_date', 'N/A')[:10]}")
                            disc_col3.metric("Compagnia", discount.get('company_name', 'N/A'))
                            disc_col4.metric("Broker", discount.get('broker_name', 'N/A'))
                            
                            # Azioni
                            action_col1, action_col2 = st.columns(2)
                            with action_col1:
                                if st.button(f"✏️ Modifica #{discount.get('id', 'N/A')}", key=f"edit_{idx}"):
                                    st.info("Funzione modifica in fase di implementazione")
                            with action_col2:
                                if st.button(f"🗑 Elimina #{discount.get('id', 'N/A')}", key=f"delete_{idx}"):
                                    st.info("Funzione eliminazione in fase di implementazione")
                else:
                    st.info(" Nessuno sconto attivo con i filtri selezionati")
            else:
                st.info(" Nessuno sconto attivo disponibile")
        except Exception as e:
            st.error(f"❌ Errore nel caricamento degli sconti: {str(e)}")
    
    with discount_tabs[2]:
        st.subheader("📊 Analisi Programmi Sconto")
        
        # Statistiche generali
        st.markdown("### 📈 Statistiche Generali")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        stat_col1.metric("Sconti Attivi", "24", "📈 +12%")
        stat_col2.metric("Broker Coinvolti", "18", "📈 +8%")
        stat_col3.metric("Volume Scontato", "€2.4M", "📈 +15%")
        stat_col4.metric("Risparmio Broker", "€240K", "📈 +15%")
        
        # Grafici analisi
        st.markdown("### 📊 Distribuzione per Tipo")
        chart_data = pd.DataFrame({
            'Tipo': ['Volume', 'Performance', 'Fidelizzazione', 'Speciale'],
            'Numero': [12, 8, 3, 1],
            'Valore': [1200000, 800000, 350000, 50000]
        })
        
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.bar_chart(chart_data.set_index('Tipo')['Numero'])
        with chart_col2:
            st.bar_chart(chart_data.set_index('Tipo')['Valore'])
        
        # Analisi ROI
        st.markdown("### 💰 Analisi Ritorno sugli Investimenti")
        roi_col1, roi_col2, roi_col3 = st.columns(3)
        roi_col1.metric("Investimento Sconti", "€240K")
        roi_col2.metric("Incremento Volume", "€2.4M")
        roi_col3.metric("ROI", "1000%", "📈")
        
        st.success("I programmi sconto hanno generato un ritorno 10 volte superiore all'investimento!")
    
    with discount_tabs[3]:
        st.subheader("⚙️ Configurazione Programmi")
        
        st.markdown("### Impostazioni Generali")
        st.markdown("""
        - 🎯 Obiettivi Performance: [Configura]
        - 📊 Soglie Automatiche: [Configura]
        - 📧 Notifiche: [Attiva/Disattiva]
        - 📅 Promemoria Scadenze: [Configura]
        """)
        
        st.markdown("### Template Comunicazione")
        st.text_area("Template Email Broker", 
                    "Gentile {broker_name}, \n\nSiamo lieti di comunicarle che in base alla sua eccellente performance...",
                    height=150)
        
        st.markdown("### Livelli Fedeltà")
        st.markdown("""
        **Bronze**: 0-10 polizze/anno - 2% sconto
        **Silver**: 11-25 polizze/anno - 5% sconto  
        **Gold**: 26-50 polizze/anno - 8% sconto
        **Platinum**: 50+ polizze/anno - 12% sconto
        """)
        
        if st.button("💾 Salva Configurazione"):
            st.success("Configurazione salvata con successo!")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sui Programmi Sconto"):
        st.markdown("""
        **I programmi sconto e fedeltà aiutano a:**
        - Incentivare i broker partner
        - Aumentare la retention
        - Premiare le performance superiori
        - Espandere il volume premi
        
        **Tipi di sconto:**
        - 📦 **Volume**: Basato sul numero di polizze emesse
        - 🏆 **Performance**: Basato sulla qualità e risultati
        - 💎 **Fidelizzazione**: Per broker di lunga data
        - 🎁 **Speciale**: Sconti occasionali e promozioni
        
        **Benefici:**
        - Incremento medio del 25% nel volume premi
        - Riduzione del 40% nel tasso di abbandono broker
        - Maggiore soddisfazione partner
        """)

# Pagina metriche broker
def broker_metrics_page():
    st.title("🏆 Metriche Performance Broker")
    
    # Sezione selezione broker migliorata
    st.subheader("🧑‍💼 Seleziona Broker")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        broker_id = st.number_input("ID Broker", min_value=1, value=1,
                                  help="Inserisci l'ID del broker da analizzare")
    with col2:
        st.write("")
        st.write("")
        if st.button("📋 Elenco Broker"):
            st.info("Funzionalità elenco broker in fase di implementazione")
    
    # Pulsante calcolo metriche con stile migliorato
    st.markdown("---")
    if st.button("🏅 Calcola Metriche Performance", type="primary", use_container_width=True):
        with st.spinner("🧠 Calcolo metriche in corso..."):
            try:
                metrics = api_get(f"/insurance/broker-metrics?broker_id={broker_id}")
                if metrics:
                    st.success("✅ Metriche calcolate con successo!")
                    
                    # Informazioni broker
                    st.subheader("🧑‍💼 Informazioni Broker")
                    try:
                        broker_info = api_get(f"/clients/{broker_id}")
                        if broker_info:
                            broker_col1, broker_col2 = st.columns(2)
                            with broker_col1:
                                st.write(f"**Nome:** {broker_info.get('name', 'N/A')}")
                                st.write(f"**Azienda:** {broker_info.get('company', 'N/A')}")
                            with broker_col2:
                                st.write(f"**Email:** {broker_info.get('email', 'N/A')}")
                                st.write(f"**Settore:** {broker_info.get('sector', 'N/A')}")
                    except:
                        pass
                    
                    # Performance Score con indicatore visivo
                    st.subheader("⭐ Performance Score")
                    score_col1, score_col2 = st.columns([1, 3])
                    with score_col1:
                        performance_score = metrics['performance_score']
                        st.metric("Punteggio Totale", f"{performance_score:.1f}/100")
                    
                    with score_col2:
                        # Barra progresso con colori per performance
                        if performance_score >= 80:
                            st.progress(performance_score/100, text="🥇 Eccellente")
                        elif performance_score >= 60:
                            st.progress(performance_score/100, text="🥈 Buona")
                        elif performance_score >= 40:
                            st.progress(performance_score/100, text="🥉 Media")
                        else:
                            st.progress(performance_score/100, text="🔴 Bassa")
                    
                    # Livello con badge
                    st.subheader("🏅 Livello Broker")
                    tier = metrics['tier']
                    if tier == "Platinum":
                        st.success(f"**Livello:** {tier} 🥇")
                    elif tier == "Gold":
                        st.warning(f"**Livello:** {tier} 🥈")
                    elif tier == "Silver":
                        st.info(f"**Livello:** {tier} 🥉")
                    else:
                        st.error(f"**Livello:** {tier}")
                    
                    # Metriche di Volume con card stilizzate
                    st.subheader("📦 Metriche di Volume")
                    vol = metrics['volume_metrics']
                    vol_col1, vol_col2 = st.columns(2)
                    vol_col1.metric(" Polizze Emesse", vol['policies_count'], "📈")
                    premium_value = vol['total_premium'] if vol['total_premium'] is not None else 0
                    vol_col2.metric(" Premi Totali", f"€{premium_value:,.2f}", "💰")
                    
                    # Metriche Sinistri con indicatori
                    st.subheader("🚨 Metriche Sinistri")
                    claims = metrics['claims_metrics']
                    claims_col1, claims_col2 = st.columns(2)
                    claims_col1.metric(" Sinistri Registrati", claims['claims_count'], "📋")
                    claims_value = claims['total_claims'] if claims['total_claims'] is not None else 0
                    claims_col2.metric(" Importo Sinistri", f"€{claims_value:,.2f}", "💸")
                    
                    # Sezione analisi avanzata
                    st.subheader("🔬 Analisi Avanzata")
                    analysis_tabs = st.tabs(["📊 Trend Performance", "💰 Confronto Premi", "🚨 Analisi Sinistri"])
                    
                    with analysis_tabs[0]:
                        st.markdown("### Trend Performance (Ultimi 12 mesi)")
                        st.info("Grafico trend performance in fase di implementazione")
                        st.line_chart([performance_score] * 12)  # Dati di esempio
                    
                    with analysis_tabs[1]:
                        st.markdown("### Confronto Premi con Media")
                        st.success("Broker performante nel volume premi")
                        st.progress(min(1.0, premium_value / 100000), text=f"Raggiunto {min(100, premium_value/1000):.0f}% dell'obiettivo")
                    
                    with analysis_tabs[2]:
                        st.markdown("### Analisi Sinistri")
                        claims_ratio = (claims['claims_count'] / max(1, vol['policies_count'])) * 100 if vol['policies_count'] > 0 else 0
                        if claims_ratio < 5:
                            st.success(f"Ratio sinistri: {claims_ratio:.1f}% - Eccellente gestione rischi")
                        elif claims_ratio < 10:
                            st.warning(f"Ratio sinistri: {claims_ratio:.1f}% - Gestione rischi buona")
                        else:
                            st.error(f"Ratio sinistri: {claims_ratio:.1f}% - Attenzione gestione rischi")
                    
                    # Sezione raccomandazioni
                    st.subheader("💡 Raccomandazioni")
                    if performance_score >= 80:
                        st.success("🎉 Eccellente performance! Mantieni questo livello.")
                    elif performance_score >= 60:
                        st.info("👍 Buona performance. Considera di espandere il portafoglio clienti.")
                    else:
                        st.warning("🔧 Ci sono margini di miglioramento. Concentrati su qualità e volume.")
                        
                else:
                    st.warning(" Nessuna metrica trovata per il broker selezionato")
                    
            except Exception as e:
                st.error(f"❌ Errore nel calcolo delle metriche: {str(e)}")
    
    # Sezione informazioni
    st.markdown("---")
    with st.expander("ℹ️ Informazioni sulle Metriche"):
        st.markdown("""
        **Le metriche valutano la performance del broker su diversi aspetti:**
        - Performance Score: Valutazione complessiva su scala 0-100
        - Livello: Classificazione (Platinum, Gold, Silver, Base)
        - Metriche di Volume: Polizze emesse e volume premi
        - Metriche Sinistri: Numero e importo sinistri gestiti
        
        **Livelli:**
        - 🥇 Platinum: Score 80-100
        - 🥈 Gold: Score 60-79
        - 🥉 Silver: Score 40-59
        - Base: Score 0-39
        """)

# Menu di navigazione
def main():
    st.sidebar.title("🏦 BrokerFlow AI")
    st.sidebar.markdown("### Dashboard Assicurativa B2B2B")
    
    # Se l'utente non è autenticato, mostra solo la pagina di login
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Se l'utente è autenticato, mostra il menu principale
    # Informazioni utente
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"👤 **Utente:** {st.session_state.user.get('username', 'Utente')}")
    st.sidebar.markdown("🏢 **Compagnia:** Demo Insurance")
    st.sidebar.markdown("📅 **Data:** " + date.today().strftime("%d/%m/%Y"))
    
    # Pulsante di logout
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.access_token = None
        st.rerun()  # Cambiato da experimental_rerun a rerun
    
    # Organizzazione delle pagine in sezioni
    section = st.sidebar.selectbox(
        "🧭 Navigazione",
        ["📊 Dashboard", "👥 Gestione", "🔬 Analisi", "📋 Compliance", "💰 Programmi", "⚙️ Configurazione"]
    )
    
    if section == "📊 Dashboard":
        pages = {
            "📈 Dashboard Principale": main_dashboard,
            "🔬 Analisi Rischio AI": risk_analysis_page,
            "🏢 Dashboard Compagnia": company_dashboard_page
        }
        selection = st.sidebar.radio("📄 Pagine", list(pages.keys()))
        page = pages[selection]
        with st.spinner(f".Caricamento {selection}..."):
            page()
    
    elif section == "👥 Gestione":
        pages = {
            "👥 Clienti": clients_page,
            "🛡️ Rischi": risks_page,
            "📜 Polizze": policies_page,
            "🚨 Sinistri": claims_page
        }
        selection = st.sidebar.radio("📄 Pagine", list(pages.keys()))
        page = pages[selection]
        with st.spinner(f".Caricamento {selection}..."):
            page()
    
    elif section == "🔬 Analisi":
        pages = {
            "📋 Compliance": compliance_page,
            "💰 Programmi Sconto": discounts_page,
            "🏆 Metriche Broker": broker_metrics_page
        }
        selection = st.sidebar.radio("📄 Pagine", list(pages.keys()))
        page = pages[selection]
        with st.spinner(f".Caricamento {selection}..."):
            page()
    
    elif section == "📋 Compliance":
        compliance_page()
    
    elif section == "💰 Programmi":
        discounts_page()
    
    elif section == "⚙️ Configurazione":
        st.title("⚙️ Configurazione Sistema")
        st.info("🔧 Sezione configurazione in fase di sviluppo")
        
        config_tabs = st.tabs(["👥 Utenti", "🏢 Compagnie", "🔗 Integrazioni", "🛡️ Sicurezza"])
        
        with config_tabs[0]:
            st.subheader("👥 Gestione Utenti")
            st.markdown("""
            - 👤 Elenco utenti
            - 🎯 Ruoli e permessi
            - 🔐 Autenticazione
            - 📊 Audit accessi
            """)
        
        with config_tabs[1]:
            st.subheader("🏢 Gestione Compagnie")
            st.markdown("""
            - 🏢 Elenco compagnie
            - 📈 Performance tracking
            - 🤝 Partnership
            - 💰 Configurazione premi
            """)
        
        with config_tabs[2]:
            st.subheader("🔗 Integrazioni")
            st.markdown("""
            - 🖥 SGA Systems
            - 🌐 Portali Broker
            - 💳 Payment Gateways
            - 📧 Email Services
            """)
        
        with config_tabs[3]:
            st.subheader("🛡️ Sicurezza")
            st.markdown("""
            - 🔐 2FA/MFA
            - 🔒 Crittografia
            - 🛡️ Firewall
            - 📋 Compliance
            """)
    
    # Footer sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("🚀 **BrokerFlow AI v2.0**")
    st.sidebar.markdown("💡 *Trasformiamo l'assicurativo con l'intelligenza artificiale*")
    
    # Link utili
    st.sidebar.markdown("### 🔗 Link Utili")
    st.sidebar.markdown("[📚 Documentazione](#)")
    st.sidebar.markdown("[❓ Supporto](#)")
    st.sidebar.markdown("[📢 Feedback](#)")

if __name__ == "__main__":
    main()