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





 Certo! Ecco i comandi per fare una pulizia completa di Docker nel tuo ambiente WSL:

    1 # 1. Ferma tutti i container in esecuzione
    2 docker compose down
    3
    4 # 2. Rimuovi tutti i container
    5 docker rm $(docker ps -aq)
    6
    7 # 3. Rimuovi tutte le immagini
    8 docker rmi $(docker images -q)
    9
   10 # 4. Rimuovi tutti i volumi
   11 docker volume rm $(docker volume ls -q)
   12
   13 # 5. Rimuovi tutte le reti
   14 docker network rm $(docker network ls -q)
   15
   16 # 6. Pulizia generale (container, immagini, volumi, reti non utilizzati)
   17 docker system prune -a --volumes
   18
   19 # 7. Se vuoi essere ancora più radicale, puoi anche resettare Docker (opzionale)
   20 # Questo comando rimuove TUTTO, usalo con cautela:
   21 # docker system prune -a --volumes --force

  Dopo aver eseguito questi comandi, puoi ricostruire l'ambiente con:

   1 # Ricostruisci l'ambiente
   2 docker compose up -d

  Questo processo:

   1. Fermerà tutti i container in esecuzione
   2. Rimuoverà tutti i container, immagini, volumi e reti Docker
   3. Pulirà completamente l'ambiente Docker
   4. Ti permetterà di ricostruire tutto da zero con le nuove modifiche

  Nota importante: Questo rimuoverà TUTTI i dati Docker nel tuo sistema, non solo quelli di questo progetto. Se hai altri
  progetti Docker in esecuzione, dovrai riavviarli separatamente.

  Dopo la pulizia, quando esegui docker compose up -d, Docker ricostruirà tutte le immagini dal Dockerfile, quindi le tue
  nuove modifiche saranno incluse.




  ✦ Hai ragione di dubitare. In alcuni casi, specialmente quando si modificano file Python che vengono importati da altri
  moduli o quando ci sono cache di compilazione, potrebbe essere necessario ricostruire le immagini Docker.

  Per essere sicuri al 100%, ti consiglio di eseguire:

   1 docker compose down
   2 docker compose build --no-cache
   3 docker compose up -d

  Questo comando:
   1. docker compose down - ferma e rimuove i container
   2. docker compose build --no-cache - ricostruisce le immagini Docker senza utilizzare la cache, assicurando che tutte le
      modifiche al codice vengano incorporate
   3. docker compose up -d - avvia i container con le nuove immagini

  In alternativa, se vuoi essere ancora più sicuro, puoi eseguire una pulizia completa e ricostruire tutto:

   1 docker compose down
   2 docker system prune -a
   3 docker compose up -d --build

  Ma per il tuo caso specifico, il primo approccio con --no-cache dovrebbe essere sufficiente per assicurarti che tutte le
  modifiche al codice vengano incorporate correttamente nelle immagini Docker.