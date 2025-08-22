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

docker compose down
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a --volumes
docker compose up -d
docker compose exec init-db python populate_dashboard_data.py

Ora eseguiamo lo script per popolare i dati della dashboard:

   1 # Eseguiamo lo script per popolare i dati della dashboard
   2 docker compose exec init-db python populate_dashboard_data.py

  Dopo aver eseguito lo script, verifichiamo che i dati siano stati popolati correttamente:

    1 # Verifichiamo le compagnie assicurative create
    2 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT id, name, company, sector
      FROM clients WHERE sector = 'Assicurativo';"
    3
    4 # Verifichiamo che le policy siano state associate alle compagnie
    5 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) as
      policies_with_company FROM policies WHERE company_id IS NOT NULL;"
    6
    7 # Verifichiamo che ci siano premi e sinistri
    8 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) as premiums_count
      FROM premiums;"
    9 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "SELECT COUNT(*) as claims_count
      FROM claims;"
   10
   11 # Verifichiamo i dati aggregati per la dashboard
   12 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "
   13 SELECT
   14     c.company as insurance_company,
   15     COUNT(DISTINCT p.id) as total_policies,
   16     COUNT(DISTINCT CASE WHEN p.status = 'active' THEN p.id END) as active_policies,
   17     SUM(pr.amount) as total_premiums,
   18     COUNT(cl.id) as total_claims,
   19     SUM(cl.amount) as total_claims_amount,
   20     CASE
   21         WHEN SUM(pr.amount) > 0 THEN (SUM(cl.amount) / SUM(pr.amount) * 100)
   22         ELSE 0
   23     END as claims_ratio
   24 FROM clients c
   25 JOIN policies p ON c.id = p.company_id
   26 LEFT JOIN premiums pr ON p.id = pr.policy_id AND pr.payment_status = 'paid'
   27 LEFT JOIN claims cl ON p.id = cl.policy_id
   28 WHERE c.sector = 'Assicurativo'
   29 GROUP BY c.id, c.company
   30 ORDER BY total_policies DESC;
   31 "

  Se tutto è andato bene, ora le dashboard dovrebbero mostrare dati realistici. Se necessario, possiamo anche aggiungere
  dati specifici per i broker:

    1 # Verifichiamo i broker con dati aggregati
    2 docker compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai -e "
    3 SELECT
    4     c.id as broker_id,
    5     c.name as broker_name,
    6     c.company as broker_company,
    7     COUNT(DISTINCT p.id) as policies_issued,
    8     SUM(pr.amount) as total_premiums,
    9     COUNT(cl.id) as claims_count,
   10     SUM(cl.amount) as total_claims_amount
   11 FROM clients c
   12 JOIN risks r ON c.id = r.client_id
   13 JOIN policies p ON r.id = p.risk_id
   14 LEFT JOIN premiums pr ON p.id = pr.policy_id AND pr.payment_status = 'paid'
   15 LEFT JOIN claims cl ON p.id = cl.policy_id
   16 WHERE c.sector IN ('Trasporti', 'Sanità', 'Edilizia', 'Legalità', 'Ingegneria', 'Commercio', 'Logistica',
      'Noleggio')
   17 GROUP BY c.id, c.name, c.company
   18 ORDER BY policies_issued DESC
   19 LIMIT 10;
   20 "

  Questi dati dovrebbero ora popolare correttamente le dashboard con informazioni realistiche per:
   - Dashboard Compagnia Assicurativa: Con totale polizze, polizze attive, premi totali, ratio sinistri
   - Metriche Performance Broker: Con punteggio performance, polizze emesse, premi totali, sinistri registrati

  Se i dati non appaiono immediatamente nella dashboard web, potrebbe essere necessario:
   1. Aggiornare la pagina del browser
   2. Attendere che l'API rilegga i dati dal database
   3. Verificare che non ci siano errori nell'API che impediscono la visualizzazione dei dati



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