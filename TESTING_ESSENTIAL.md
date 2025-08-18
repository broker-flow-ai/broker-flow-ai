# BrokerFlow AI - Guida Essenziale al Testing

## 🚀 Avvio Rapido con Docker

```bash
# 1. Configurazione iniziale
cp .env.example .env
# Modifica .env con la tua API Key OpenAI (opzionale per demo)

# 2. Avvio ambiente
docker compose up -d

# 3. Verifica servizi attivi
docker compose ps
```

Servizi disponibili:
- **API**: http://localhost:8000
- **Frontend**: http://localhost:8501
- **phpMyAdmin**: http://localhost:8080

## 🧪 Testing Funzionalità Principali

### 1. Testing API Endpoints

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

#### Analisi Rischio
```bash
# Crea cliente di test
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "INSERT INTO clients (name, company, email) VALUES ('Test Client', 'Test Company', 'test@example.com');"

# Analizza rischio
curl -X POST http://localhost:8000/api/v1/insurance/risk-analysis \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1}'
```

#### Dashboard Analytics
```bash
curl http://localhost:8000/api/v1/insurance/portfolio-analytics
```

### 2. Testing Frontend Web

1. Apri http://localhost:8501
2. Naviga tra le sezioni:
   - Dashboard Principale
   - Analisi Rischio
   - Programmi Sconto

### 3. Testing Elaborazione Documenti

```bash
# Genera PDF di test
docker compose exec processor python create_sample_pdf.py

# Elabora documento
docker compose exec processor python main.py

# Verifica output
docker compose exec processor ls -la output/
```

## 🛠 Operazioni Comuni

### Visualizzazione Logs
```bash
docker compose logs api
docker compose logs frontend
```

### Accesso Database
```bash
# Via phpMyAdmin: http://localhost:8080
# Credenziali: server=db, user=root, password=root123

# Via command line
docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai
```

### Restart Servizi
```bash
docker compose restart
```

### Stop Ambiente
```bash
docker compose down
```

## ✅ Verifica Installazione

1. Tutti i servizi Docker attivi: `docker compose ps`
2. API accessibile: `curl http://localhost:8000/api/v1/health`
3. Frontend accessibile: http://localhost:8501
4. Database funzionante: verifica via phpMyAdmin

## 📞 Troubleshooting

### Problemi di Avvio
```bash
# Verifica logs
docker compose logs

# Ricostruisci immagini
docker compose down
docker compose up --build
```

### Reset Completo
```bash
# PERDE TUTTI I DATI!
docker compose down -v
docker volume prune -f
docker compose up
```