import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# Configurazione della pagina
st.set_page_config(
    page_title="BrokerFlow AI - Dashboard Assicurativa",
    page_icon="📊",
    layout="wide"
)

# URL base dell'API
API_BASE_URL = "http://localhost:8000/api/v1"

# Funzioni di utilità per chiamate API
def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Errore nella chiamata API: {str(e)}")
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
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
    
    # Metriche principali
    st.subheader("Metriche di Sistema")
    metrics = api_get("/metrics")
    if metrics:
        cols = st.columns(4)
        cols[0].metric("Clienti", metrics["database_metrics"]["clients"])
        cols[1].metric("Polizze", metrics["database_metrics"]["policies"])
        cols[2].metric("Sinistri", metrics["database_metrics"]["claims"])
        cols[3].metric("Premi", metrics["database_metrics"]["premiums"])
    
    # Analisi portafoglio
    st.subheader("Analisi Portafoglio")
    portfolio_data = api_get("/insurance/portfolio-analytics")
    if portfolio_data and portfolio_data["portfolio_summary"]:
        df = pd.DataFrame(portfolio_data["portfolio_summary"])
        st.dataframe(df)
        
        # Grafico distribuzione tipi di rischio
        fig = create_pie_chart(
            portfolio_data["portfolio_summary"],
            "policy_count",
            "risk_type",
            "Distribuzione Tipi di Rischio"
        )
        if fig:
            st.plotly_chart(fig)
    
    # Trend temporale
    if portfolio_data and portfolio_data["trend_analysis"]:
        fig = create_line_chart(
            portfolio_data["trend_analysis"],
            "month",
            "policies_issued",
            "Trend Emissione Polizze"
        )
        if fig:
            st.plotly_chart(fig)

# Pagina analisi rischio
def risk_analysis_page():
    st.title("🔬 Analisi Rischio Avanzata")
    
    # Selezione cliente
    client_id = st.number_input("ID Cliente", min_value=1, value=1)
    
    if st.button("Analizza Rischio"):
        with st.spinner("Analisi in corso..."):
            result = api_post("/insurance/risk-analysis", {"client_id": client_id})
            if result:
                st.success("Analisi completata!")
                
                # Mostra risultati
                analysis = result["analysis"]
                st.subheader("Risultati Analisi")
                
                col1, col2 = st.columns(2)
                col1.metric("Score Rischio", analysis.get("risk_score", "N/A"))
                col2.metric("Livello Raccomandazione", analysis.get("recommendation_level", "N/A"))
                
                st.subheader("Analisi Settore")
                st.write(analysis.get("sector_analysis", "N/A"))
                
                st.subheader("Raccomandazioni Pricing")
                st.write(analysis.get("pricing_recommendation", "N/A"))
                
                st.subheader("Note Underwriting")
                st.write(analysis.get("underwriting_notes", "N/A"))

# Pagina dashboard compagnia
def company_dashboard_page():
    st.title("🏢 Dashboard Compagnia Assicurativa")
    
    company_id = st.number_input("ID Compagnia", min_value=1, value=1)
    
    if st.button("Carica Dashboard"):
        with st.spinner("Caricamento dashboard..."):
            # Performance compagnia
            performance = api_get(f"/insurance/company-performance?company_id={company_id}")
            if performance:
                st.subheader("KPI Principali")
                kpi = performance["kpi"]
                cols = st.columns(4)
                cols[0].metric("Totale Polizze", kpi["total_policies"])
                cols[1].metric("Polizze Attive", kpi["active_policies"])
                cols[2].metric("Premi Totali", f"€{kpi['total_premium']:,.2f}")
                cols[3].metric("Ratio Sinistri", f"{kpi['loss_ratio']:.2f}%")
                
                # Confronto con mercato
                st.subheader("Confronto con Mercato")
                market_pos = performance["market_position"]
                cols = st.columns(2)
                cols[0].metric(
                    "Ratio Sinistri vs Mercato", 
                    f"{market_pos['loss_ratio_vs_market']:+.2f}%",
                    "Meglio" if market_pos['loss_ratio_vs_market'] < 0 else "Peggio"
                )
                cols[1].metric(
                    "Premio Medio vs Mercato", 
                    f"€{market_pos['premium_vs_market']:+.2f}",
                    "Meglio" if market_pos['premium_vs_market'] > 0 else "Peggio"
                )

# Pagina compliance
def compliance_page():
    st.title("📋 Report Compliance")
    
    # Generazione nuovo report
    st.subheader("Genera Nuovo Report")
    col1, col2, col3 = st.columns(3)
    report_type = col1.selectbox("Tipo Report", ["GDPR", "SOX", "IVASS"])
    period_start = col2.date_input("Data Inizio", date(2025, 1, 1))
    period_end = col3.date_input("Data Fine", date(2025, 12, 31))
    
    if st.button("Genera Report"):
        with st.spinner("Generazione report..."):
            result = api_post("/insurance/compliance-report", {
                "report_type": report_type,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat()
            })
            if result:
                st.success("Report generato con successo!")
                st.subheader(result.get("title", "Report"))
                st.write("### Riepilogo Esecutivo")
                st.write(result.get("executive_summary", ""))
                
                st.write("### Dettagli Tecnici")
                st.write(result.get("technical_details", ""))
                
                st.write("### Conclusioni")
                st.write(result.get("conclusions", ""))
    
    # Lista report esistenti
    st.subheader("Report Esistenti")
    reports = api_get("/insurance/compliance-reports")
    if reports and reports["reports"]:
        df = pd.DataFrame(reports["reports"])
        st.dataframe(df[["report_type", "period_start", "period_end", "generated_at"]])

# Pagina gestione sconti
def discounts_page():
    st.title("💰 Programmi Sconto e Fedeltà")
    
    # Creazione nuovo sconto
    st.subheader("Crea Nuovo Sconto")
    col1, col2, col3 = st.columns(3)
    company_id = col1.number_input("ID Compagnia", min_value=1)
    broker_id = col2.number_input("ID Broker", min_value=1)
    discount_type = col3.selectbox("Tipo Sconto", ["Volume", "Performance", "Fidelizzazione"])
    
    col1, col2, col3 = st.columns(3)
    percentage = col1.number_input("Percentuale (%)", min_value=0.0, max_value=100.0, step=0.1)
    start_date = col2.date_input("Data Inizio")
    end_date = col3.date_input("Data Fine")
    
    if st.button("Crea Sconto"):
        result = api_post("/insurance/discounts", {
            "company_id": company_id,
            "broker_id": broker_id,
            "discount_type": discount_type,
            "percentage": percentage,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        if result:
            st.success("Sconto creato con successo!")
    
    # Lista sconti attivi
    st.subheader("Sconti Attivi")
    discounts = api_get("/insurance/discounts")
    if discounts and discounts["discounts"]:
        df = pd.DataFrame(discounts["discounts"])
        st.dataframe(df[["company_name", "broker_name", "discount_type", "discount_percentage", "start_date", "end_date"]])

# Pagina metriche broker
def broker_metrics_page():
    st.title("🏆 Metriche Performance Broker")
    
    broker_id = st.number_input("ID Broker", min_value=1, value=1)
    
    if st.button("Calcola Metriche"):
        with st.spinner("Calcolo metriche..."):
            metrics = api_get(f"/insurance/broker-metrics?broker_id={broker_id}")
            if metrics:
                st.subheader("Performance Score")
                st.metric("Punteggio Totale", f"{metrics['performance_score']:.1f}/100")
                st.metric("Livello", metrics['tier'])
                
                st.subheader("Metriche di Volume")
                vol = metrics['volume_metrics']
                cols = st.columns(2)
                cols[0].metric("Polizze Emesse", vol['policies_count'])
                cols[1].metric("Premi Totali", f"€{vol['total_premium']:,.2f}")
                
                st.subheader("Metriche Sinistri")
                claims = metrics['claims_metrics']
                cols = st.columns(2)
                cols[0].metric("Sinistri Registrati", claims['claims_count'])
                cols[1].metric("Importo Sinistri", f"€{claims['total_claims']:,.2f}")

# Menu di navigazione
def main():
    st.sidebar.title(" BrokerFlow AI")
    st.sidebar.markdown("### Dashboard Assicurativa B2B2B")
    
    pages = {
        "Dashboard Principale": main_dashboard,
        "Analisi Rischio": risk_analysis_page,
        "Dashboard Compagnia": company_dashboard_page,
        "Compliance": compliance_page,
        "Programmi Sconto": discounts_page,
        "Metriche Broker": broker_metrics_page
    }
    
    selection = st.sidebar.radio("Vai a", list(pages.keys()))
    page = pages[selection]
    
    with st.spinner(f"Caricamento {selection}..."):
        page()

if __name__ == "__main__":
    main()