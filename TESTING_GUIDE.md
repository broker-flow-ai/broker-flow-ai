# BrokerFlow AI - Guida Completa all'Installazione e Testing

## 📋 Prerequisiti di Sistema

Prima di iniziare, assicurati di avere installato:

- **Python 3.8+**
- **MySQL 5.7+**
- **Git**
- **Tesseract OCR** (opzionale, per PDF scansionati)
- **OpenAI API Key**

## 🗑️ Rimozione Installazione Precedente

### 1. Fermare i Servizi in Esecuzione
```bash
# Se hai il server API in esecuzione, fermalo con Ctrl+C
# Se hai il frontend in esecuzione, fermalo con Ctrl+C
```

### 2. Rimuovere il Database
```bash
# Accedi a MySQL
mysql -u root -p

# Elimina il database esistente
DROP DATABASE IF EXISTS brokerflow_ai;

# Esci da MySQL
EXIT;
```

### 3. Rimuovere il Repository Git
```bash
# Naviga alla directory del progetto
cd /path/to/brokerflow-ai

# Torna alla directory padre
cd ..

# Elimina la directory del progetto
rm -rf brokerflow-ai
```

## 🚀 Installazione Completa

### 1. Clonare il Repository
```bash
# Clona il repository aggiornato
git clone https://github.com/tuonome/broker-flow-ai.git
cd broker-flow-ai
```

### 2. Creare Ambiente Virtuale
```bash
# Crea ambiente virtuale Python
python -m venv brokerflow-env

# Attiva l'ambiente virtuale
# Su Windows:
brokerflow-env\\Scripts\\activate
# Su macOS/Linux:
source brokerflow-env/bin/activate
```

### 3. Installare Dipendenze
```bash
# Aggiorna pip
pip install --upgrade pip

# Installa tutte le dipendenze
pip install -r requirements.txt
```

### 4. Configurare le Variabili d'Ambiente
```bash
# Copia il file di esempio
cp .env.example .env

# Modifica il file .env con le tue credenziali
# Su Windows puoi usare notepad:
notepad .env
# Su macOS/Linux puoi usare nano:
nano .env

# Imposta almeno queste variabili:
OPENAI_API_KEY=tua_api_key_openai
MYSQL_HOST=localhost
MYSQL_USER=tuo_utente_mysql
MYSQL_PASSWORD=tua_password_mysql
MYSQL_DATABASE=brokerflow_ai
```

### 5. Configurare il Database
```bash
# Creare il database e le tabelle
mysql -u tuo_utente -p < schema.sql
```

### 6. Verificare l'Installazione
```bash
# Verifica che tutte le dipendenze siano installate
pip list

# Dovresti vedere:
# fastapi, streamlit, openai, mysql-connector-python, ecc.
```

## ▶️ Avvio dei Servizi

### 1. Avviare l'API Server
```bash
# In una nuova finestra terminale, attiva l'ambiente virtuale
cd /path/to/brokerflow-ai
brokerflow-env\\Scripts\\activate  # Windows
# oppure
source brokerflow-env/bin/activate  # macOS/Linux

# Avvia il server API
uvicorn api_b2b:app --reload --host 0.0.0.0 --port 8000
```

Dovresti vedere un output simile a:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. Avviare il Frontend Dashboard
```bash
# In un'altra finestra terminale, attiva l'ambiente virtuale
cd /path/to/brokerflow-ai
brokerflow-env\\Scripts\\activate  # Windows
# oppure
source brokerflow-env/bin/activate  # macOS/Linux

# Avvia il frontend
streamlit run frontend/dashboard.py
```

Il browser dovrebbe aprirsi automaticamente all'indirizzo `http://localhost:8501`

## 🧪 Guida al Testing Completo

### 1. Test API Health Check
```bash
# Verifica che l'API sia in esecuzione
curl http://localhost:8000/api/v1/health

# Dovresti ricevere:
# {"status": "healthy", "timestamp": "...", "version": "2.0.0"}
```

### 2. Test API Metrics
```bash
# Verifica le metriche di sistema
curl http://localhost:8000/api/v1/metrics

# Dovresti ricevere i conteggi dei record nel database
```

### 3. Testing Dashboard Web
1. Apri il browser all'indirizzo `http://localhost:8501`
2. Verifica che la dashboard principale si carichi correttamente
3. Naviga tra le diverse sezioni:
   - Dashboard Principale
   - Analisi Rischio
   - Dashboard Compagnia
   - Compliance
   - Programmi Sconto
   - Metriche Broker

### 4. Testing Funzionalità di Base (PDF Processing)

#### Creare un PDF di Test
```bash
# Genera un PDF di esempio
python create_sample_pdf.py
```

#### Verificare l'Elaborazione
```bash
# Il PDF di esempio è stato creato in inbox/sample_flotta.pdf
# Puoi ora testare il processo di elaborazione esistente
python main.py
```

### 5. Testing Analisi Rischio Avanzata
```bash
# Usa l'API per analizzare un cliente (ID 1)
curl -X POST http://localhost:8000/api/v1/insurance/risk-analysis \\
  -H "Content-Type: application/json" \\
  -d '{"client_id": 1}'

# Dovresti ricevere un'analisi completa del rischio
```

### 6. Testing Dashboard Analytics
```bash
# Recupera analisi portafoglio
curl http://localhost:8000/api/v1/insurance/portfolio-analytics

# Recupera performance compagnia (ID 1)
curl http://localhost:8000/api/v1/insurance/company-performance?company_id=1

# Recupera performance broker (ID 1)
curl http://localhost:8000/api/v1/insurance/broker-performance?broker_id=1
```

### 7. Testing Compliance Reporting
```bash
# Genera un report GDPR
curl -X POST http://localhost:8000/api/v1/insurance/compliance-report \\
  -H "Content-Type: application/json" \\
  -d '{
    "report_type": "GDPR",
    "period_start": "2025-01-01",
    "period_end": "2025-12-31"
  }'

# Recupera i report esistenti
curl http://localhost:8000/api/v1/insurance/compliance-reports
```

### 8. Testing AI Pricing & Underwriting
```bash
# Suggerimento pricing (simulato)
curl -X POST http://localhost:8000/api/v1/insurance/pricing-suggestion \\
  -H "Content-Type: application/json" \\
  -d '{
    "client_profile": {"name": "Test Client"},
    "risk_analysis": {"risk_score": 45},
    "market_data": {"avg_premium": 1200}
  }'

# Predizione sinistri
curl -X POST http://localhost:8000/api/v1/insurance/claims-prediction \\
  -H "Content-Type: application/json" \\
  -d '{
    "client_profile": {"sector": "Transportation"},
    "historical_data": [{"amount": 5000}]
  }'

# Underwriting automatizzato
curl -X POST http://localhost:8000/api/v1/insurance/automated-underwriting \\
  -H "Content-Type: application/json" \\
  -d '{"risk_type": "Flotta Auto"}'
```

### 9. Testing Programmi Sconto
```bash
# Crea uno sconto
curl -X POST http://localhost:8000/api/v1/insurance/discounts \\
  -H "Content-Type: application/json" \\
  -d '{
    "company_id": 1,
    "broker_id": 1,
    "discount_type": "Performance",
    "percentage": 10.5,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31"
  }'

# Recupera sconti attivi
curl http://localhost:8000/api/v1/insurance/discounts

# Calcola premio scontato
curl http://localhost:8000/api/v1/insurance/discounted-premium?base_premium=1000&company_id=1&broker_id=1

# Metriche performance broker
curl http://localhost:8000/api/v1/insurance/broker-metrics?broker_id=1
```

### 10. Testing Emissione Polizza
```bash
# Emissione polizza (simulata)
curl -X POST http://localhost:8000/api/v1/insurance/policy-issuance \\
  -H "Content-Type: application/json" \\
  -d '{
    "client_data": {"name": "Test Client"},
    "risk_data": {"type": "Flotta Auto"},
    "premium_data": {"amount": 1200},
    "company_id": 1
  }'
```

### 11. Testing Database Esteso
```bash
# Verifica che le nuove tabelle siano state create
mysql -u tuo_utente -p brokerflow_ai

# Esegui alcune query di verifica:
SELECT COUNT(*) FROM claims;
SELECT COUNT(*) FROM premiums;
SELECT COUNT(*) FROM risk_analysis;
SELECT COUNT(*) FROM compliance_reports;
SELECT COUNT(*) FROM discounts;

# Esci da MySQL
EXIT;
```

## 🧪 Testing Interfaccia Web

### 1. Dashboard Principale
- Verifica visualizzazione metriche sistema
- Controlla grafici distribuzione rischi
- Verifica trend temporale

### 2. Analisi Rischio
- Inserisci ID cliente (1)
- Clicca "Analizza Rischio"
- Verifica risultati analisi visualizzati

### 3. Dashboard Compagnia
- Inserisci ID compagnia (1)
- Clicca "Carica Dashboard"
- Verifica KPI e confronto mercato

### 4. Compliance
- Seleziona tipo report e date
- Clicca "Genera Report"
- Verifica lista report esistenti

### 5. Programmi Sconto
- Compila form creazione sconto
- Clicca "Crea Sconto"
- Verifica lista sconti attivi

### 6. Metriche Broker
- Inserisci ID broker (1)
- Clicca "Calcola Metriche"
- Verifica punteggio performance e tier

## 🛠 Troubleshooting Comune

### Problemi con le Dipendenze
```bash
# Se ci sono errori, reinstalla le dipendenze
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Problemi con il Database
```bash
# Ricrea il database
mysql -u tuo_utente -p
DROP DATABASE IF EXISTS brokerflow_ai;
CREATE DATABASE brokerflow_ai;
EXIT;

# Ricarica lo schema
mysql -u tuo_utente -p brokerflow_ai < schema.sql
```

### Problemi con l'API
```bash
# Verifica che la porta 8000 non sia occupata
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # macOS/Linux

# Se necessario, killa il processo occupante
taskkill /PID numero_processo /F  # Windows
kill -9 numero_processo  # macOS/Linux
```

### Problemi con il Frontend
```bash
# Se Streamlit non si apre, prova:
streamlit run frontend/dashboard.py --server.port 8502
```

## ✅ Verifica Installazione Completa

Dopo aver completato tutti i test, dovresti avere:

1. **API Server** in esecuzione su `http://localhost:8000`
2. **Frontend Dashboard** accessibile su `http://localhost:8501`
3. **Database MySQL** con tutte le tabelle create
4. **Tutti gli endpoint API** funzionanti
5. **Tutte le funzionalità dashboard** operative
6. **Connessione OpenAI** configurata e funzionante

## 📞 Supporto

In caso di problemi durante l'installazione o il testing:

1. Verifica tutti i prerequisiti siano installati
2. Controlla che le variabili d'ambiente siano corrette
3. Assicurati che MySQL sia in esecuzione
4. Verifica la connessione internet per OpenAI

Per ulteriore assistenza, contatta il team di sviluppo.