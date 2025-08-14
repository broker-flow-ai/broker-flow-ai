# BrokerFlow AI - Moduli Core Estesi

## Moduli Implementati

### 1. Analisi Rischio Avanzata
- `modules/risk_analyzer.py`: Modulo per analisi dettagliata del rischio con AI
- Classificazione score di rischio (0-100)
- Analisi settoriale e comparativa
- Raccomandazioni di pricing
- Note underwriting

### 2. Dashboard Analytics
- `modules/dashboard_analytics.py`: Modulo per analisi aggregata
- Portfolio analytics per tipologia rischio
- Trend temporali di emissione
- Analisi per settore economico
- KPI performance compagnie

### 3. Compliance Reporting
- `modules/compliance_reporting.py`: Generazione automatica report
- Report GDPR, SOX, IVASS
- Audit trail automatizzato
- Firme digitali simulate

### 4. AI Pricing & Underwriting
- `modules/ai_underwriting.py`: Modulo AI per pricing e underwriting
- Suggerimenti premi basati su dati
- Predizione sinistri futuri
- Processo underwriting automatizzato

### 5. Integrazioni B2B
- `modules/b2b_integrations.py`: Connettori per sistemi esterni
- Integrazione SGA (Sistemi Gestionali Assicurativi)
- Sincronizzazione portali broker
- Processamento pagamenti

### 6. Programmi Sconto & Fedeltà
- `modules/discount_program.py`: Gestione convenzioni
- Creazione sconti volume/performance
- Calcolo premi scontati
- Metriche performance broker

### 7. API B2B2B Enterprise
- `api_b2b.py`: API REST completa per integrazioni
- Endpoint per analisi rischio
- Dashboard analytics
- Compliance reporting
- Gestione polizze
- Programmi fedeltà

### 8. Frontend Dashboard
- `frontend/dashboard.py`: Interfaccia web completa
- Dashboard principale con metriche
- Analisi rischio interattiva
- Report compliance
- Gestione sconti
- Metriche broker

## Schema Database Esteso

Lo schema database è stato aggiornato in `schema.sql` con:

- Nuove tabelle: `claims`, `premiums`, `risk_analysis`, `compliance_reports`, `discounts`
- Campi aggiuntivi nelle tabelle esistenti
- Relazioni foreign key estese
- Indici per ottimizzazione query

## Nuovi File di Configurazione

- `requirements-api.txt`: Dipendenze specifiche per API
- `requirements-frontend.txt`: Dipendenze specifiche per frontend