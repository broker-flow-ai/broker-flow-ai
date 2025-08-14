# BrokerFlow AI - Docker Testing Guide

## 🧪 Testing Completo dell'Ambiente Docker

Questa guida ti accompagnerà attraverso il testing completo di tutti i componenti dell'ambiente Docker di BrokerFlow AI.

## ▶️ 1. Avvio dell'Ambiente

```bash
# Avvia tutti i servizi in background
docker-compose up -d

# Verifica che tutti i servizi siano in esecuzione
docker-compose ps
```

Dovresti vedere tutti i servizi con stato "Up":
- `brokerflow-ai_api_1`
- `brokerflow-ai_frontend_1`
- `brokerflow-ai_db_1`
- `brokerflow-ai_phpmyadmin_1`
- `brokerflow-ai_redis_1`

## 🔍 2. Testing Servizi Individuali

### API Service
```bash
# Verifica che l'API sia accessibile
curl http://localhost:8000/api/v1/health

# Dovresti ricevere:
# {"status": "healthy", "timestamp": "...", "version": "2.0.0"}

# Verifica la documentazione API
curl http://localhost:8000/docs
```

### Frontend Service
```bash
# Verifica che il frontend sia accessibile
curl -I http://localhost:8501

# Dovresti ricevere uno status 200 OK
```

### Database
```bash
# Verifica connessione al database
docker-compose exec db mysql -u brokerflow -pbrokerflow123 -e "SHOW DATABASES;"

# Verifica che le tabelle siano state create
docker-compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SHOW TABLES;"
```

### phpMyAdmin
```bash
# Verifica accesso a phpMyAdmin
curl -I http://localhost:8080

# Dovresti ricevere uno status 200 OK
```

## 📊 3. Testing API Endpoints

### Health Check e Metriche
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Metriche di sistema
curl http://localhost:8000/api/v1/metrics
```

### Analisi Rischio
```bash
# Poiché non ci sono ancora clienti, creiamo prima un record di test
docker-compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "INSERT INTO clients (name, company, email) VALUES ('Test Client', 'Test Company', 'test@example.com');"

# Ora testiamo l'analisi rischio
curl -X POST http://localhost:8000/api/v1/insurance/risk-analysis \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1}'
```

### Dashboard Analytics
```bash
# Portfolio analytics
curl http://localhost:8000/api/v1/insurance/portfolio-analytics

# Performance compagnia (simuliamo con ID 1)
curl http://localhost:8000/api/v1/insurance/company-performance?company_id=1

# Performance broker (simuliamo con ID 1)
curl http://localhost:8000/api/v1/insurance/broker-performance?broker_id=1
```

### Compliance Reporting
```bash
# Genera un report GDPR
curl -X POST http://localhost:8000/api/v1/insurance/compliance-report \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "GDPR",
    "period_start": "2025-01-01",
    "period_end": "2025-12-31"
  }'

# Recupera report esistenti
curl http://localhost:8000/api/v1/insurance/compliance-reports
```

### AI Pricing & Underwriting
```bash
# Suggerimento pricing (simulato)
curl -X POST http://localhost:8000/api/v1/insurance/pricing-suggestion \
  -H "Content-Type: application/json" \
  -d '{
    "client_profile": {"name": "Test Client"},
    "risk_analysis": {"risk_score": 45},
    "market_data": {"avg_premium": 1200}
  }'

# Predizione sinistri
curl -X POST http://localhost:8000/api/v1/insurance/claims-prediction \
  -H "Content-Type: application/json" \
  -d '{
    "client_profile": {"sector": "Transportation"},
    "historical_data": [{"amount": 5000}]
  }'

# Underwriting automatizzato
curl -X POST http://localhost:8000/api/v1/insurance/automated-underwriting \
  -H "Content-Type: application/json" \
  -d '{"risk_type": "Flotta Auto"}'
```

### Programmi Sconto
```bash
# Crea uno sconto (simuliamo con ID 1 per entrambi)
curl -X POST http://localhost:8000/api/v1/insurance/discounts \
  -H "Content-Type: application/json" \
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

## 🖥️ 4. Testing Interfaccia Web

### Accesso al Frontend
1. Apri il browser all'indirizzo: http://localhost:8501
2. Verifica che la dashboard principale si carichi correttamente

### Testing Sezioni Dashboard
1. **Dashboard Principale**: Verifica metriche sistema e grafici
2. **Analisi Rischio**: Prova ad analizzare il cliente ID 1
3. **Dashboard Compagnia**: Verifica performance con ID 1
4. **Compliance**: Genera un report di test
5. **Programmi Sconto**: Crea e visualizza sconti
6. **Metriche Broker**: Verifica metriche broker ID 1

### Accesso a phpMyAdmin
1. Apri il browser all'indirizzo: http://localhost:8080
2. Credenziali:
   - Server: db
   - Username: root
   - Password: root123
3. Verifica che il database `brokerflow_ai` sia accessibile
4. Controlla che le tabelle siano state create correttamente

## 📄 5. Testing Processo Documenti

### Creazione Documento di Test
```bash
# Genera un PDF di esempio
docker-compose exec processor python create_sample_pdf.py

# Verifica che il documento sia stato creato
docker-compose exec processor ls -la inbox/
```

### Elaborazione Documento
```bash
# Esegui il processo di elaborazione
docker-compose exec processor python main.py

# Verifica che il documento compilato sia stato generato
docker-compose exec processor ls -la output/
```

## 🧪 6. Testing Integrazione Componenti

### Verifica Flusso Completo
1. Crea un documento di test con `create_sample_pdf.py`
2. Verifica che appaia in `inbox/`
3. Esegui `main.py` per elaborare il documento
4. Verifica che il risultato appaia in `output/`
5. Controlla nel database che i record siano stati creati
6. Verifica nella dashboard che le metriche si siano aggiornate

### Testing API con Documento Elaborato
```bash
# Recupera i clienti creati dall'elaborazione
curl http://localhost:8000/api/v1/insurance/portfolio-analytics

# Prova ad analizzare il rischio del cliente appena creato
curl -X POST http://localhost:8000/api/v1/insurance/risk-analysis \
  -H "Content-Type: application/json" \
  -d '{"client_id": 2}'  # L'ID potrebbe essere diverso
```

## 🛠 7. Testing Operazioni di Gestione

### Scaling Servizi
```bash
# Scala il servizio API a 2 istanze
docker-compose up -d --scale api=2

# Verifica che ci siano 2 istanze
docker-compose ps | grep api

# Riporta a 1 istanza
docker-compose up -d --scale api=1
```

### Restart Servizi
```bash
# Restart di un singolo servizio
docker-compose restart api

# Restart di tutti i servizi
docker-compose restart
```

### Visualizzazione Logs
```bash
# Visualizza logs di tutti i servizi
docker-compose logs

# Visualizza logs di un servizio specifico
docker-compose logs api

# Segui i logs in tempo reale
docker-compose logs -f
```

## 🧹 8. Cleanup e Reset

### Stop Servizi
```bash
# Ferma tutti i servizi
docker-compose down
```

### Reset Completo (PERDE I DATI!)
```bash
# ATTENZIONE: Questo cancellerà tutti i dati persistenti!
docker-compose down -v
docker volume prune -f
```

### Ricostruzione Ambiente
```bash
# Ricostruisci l'ambiente da zero
docker-compose up --build
```

## ✅ Verifica Finale

Dopo aver completato tutti i test, dovresti avere conferma che:

1. **Tutti i servizi Docker** si avviano correttamente
2. **API endpoints** rispondono come atteso
3. **Frontend dashboard** è accessibile e funzionale
4. **Database** è configurato con lo schema corretto
5. **phpMyAdmin** permette l'accesso al database
6. **Processo documenti** funziona end-to-end
7. **Integrazione tra componenti** è funzionante
8. **Operazioni di gestione** (restart, scale, logs) funzionano

## 📞 Troubleshooting

### Problemi Comuni
1. **Porte occupate**: Verifica che le porte 8000, 8501, 8080, 3306 non siano in uso
2. **Errori di connessione al database**: Controlla le variabili d'ambiente
3. **Servizi che non si avviano**: Controlla i logs con `docker-compose logs`
4. **Problemi con le dipendenze**: Ricostruisci con `docker-compose up --build`

### Comandi Utili per Debug
```bash
# Verifica lo stato dei servizi
docker-compose ps

# Visualizza logs di un servizio
docker-compose logs nome_servizio

# Accedi alla shell di un container
docker-compose exec nome_servizio bash

# Verifica le variabili d'ambiente
docker-compose exec nome_servizio env
```

Questa guida completa ti permette di verificare che l'intero ambiente Docker di BrokerFlow AI sia configurato e funzionante correttamente.