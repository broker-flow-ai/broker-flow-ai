# BrokerFlow AI - Guida all'Uso con Docker

## 🐳 Panoramica Docker

L'ambiente Docker include i seguenti servizi:
- **brokerflow**: Applicazione principale Python (API + Processi)
- **db**: Database MySQL 8.0
- **phpmyadmin**: Interfaccia web per gestione database
- **redis**: Cache in-memory (per usi futuri)

## ▶️ Avvio con Docker

### 1. Configurazione Iniziale
```bash
# Copia il file di esempio delle variabili d'ambiente
cp .env.example .env

# Modifica le variabili secondo le tue esigenze
# Nota: per l'ambiente Docker, i valori di default dovrebbero funzionare
nano .env  # o usa il tuo editor preferito
```

### 2. Avvio dei Servizi
```bash
# Costruisci e avvia tutti i servizi
docker-compose up --build

# Per avviare in background:
docker-compose up --build -d
```

### 3. Accesso ai Servizi
Dopo l'avvio, i servizi saranno accessibili su:
- **API**: http://localhost:8000
- **phpMyAdmin**: http://localhost:8080
- **MySQL**: localhost:3306 (per connessioni esterne)

## 🔧 Gestione dei Servizi Docker

### Visualizzare i Log
```bash
# Visualizza i log di tutti i servizi
docker-compose logs

# Visualizza i log di un servizio specifico
docker-compose logs brokerflow

# Segui i log in tempo reale
docker-compose logs -f
```

### Accesso alla Shell del Container
```bash
# Accedi alla shell del container brokerflow
docker-compose exec brokerflow bash

# Accedi alla shell del database
docker-compose exec db bash
```

### Accesso al Database MySQL
```bash
# Accedi al database MySQL dal container
docker-compose exec db mysql -u brokerflow -pbrokerflow123 brokerflow_ai

# Oppure da host esterno (se la porta 3306 è esposta)
mysql -h localhost -P 3306 -u brokerflow -pbrokerflow123 brokerflow_ai
```

### Accesso a phpMyAdmin
1. Apri il browser all'indirizzo: http://localhost:8080
2. Credenziali di accesso:
   - Server: db
   - Username: root
   - Password: root123 (o quella impostata in .env)

## 🛠 Operazioni Comuni

### Riavvio dei Servizi
```bash
# Riavvia tutti i servizi
docker-compose restart

# Riavvia un servizio specifico
docker-compose restart brokerflow
```

### Arresto dei Servizi
```bash
# Ferma tutti i servizi
docker-compose down

# Ferma i servizi e rimuovi i volumi (PERDE I DATI!)
docker-compose down -v
```

### Aggiornamento dell'Applicazione
```bash
# Pull dei cambiamenti dal repository
git pull

# Ricostruisci e riavvia i servizi
docker-compose down
docker-compose up --build
```

## 🧪 Testing con Docker

### 1. Verifica Servizi in Esecuzione
```bash
# Lista servizi attivi
docker-compose ps

# Dovresti vedere tutti i servizi in stato "Up"
```

### 2. Test API Health Check
```bash
# Verifica che l'API sia accessibile
curl http://localhost:8000/api/v1/health

# Risposta attesa:
# {"status": "healthy", "timestamp": "...", "version": "2.0.0"}
```

### 3. Test Database
```bash
# Verifica connessione al database
docker-compose exec db mysql -u brokerflow -pbrokerflow123 -e "SHOW DATABASES;"

# Dovresti vedere il database "brokerflow_ai"
```

## 📁 Gestione File e Dati

### Directory Montate
Le seguenti directory sono montate come volumi persistenti:
- `./inbox` → Documenti in ingresso
- `./output` → Documenti generati
- `./templates` → Modelli PDF
- `./logs` → File di log
- `db_data` → Dati del database (volume Docker)

### Aggiunta di Documenti di Test
```bash
# Genera un documento di test
docker-compose exec brokerflow python create_sample_pdf.py

# Verifica che il documento sia stato creato
ls -la inbox/
```

## 🔒 Sicurezza

### Variabili d'Ambiente
Le password e le chiavi API sono gestite tramite il file `.env` che:
- NON deve essere committato nel repository
- Deve essere configurato per ogni ambiente

### Accesso ai Servizi
- L'API è accessibile solo da localhost per impostazione predefinita
- phpMyAdmin richiede autenticazione
- MySQL accetta connessioni solo dal network Docker interno

## 🚀 Avvio dei Componenti Separati

### Avvio Solo del Database
```bash
# Avvia solo il database e phpMyAdmin
docker-compose up -d db phpmyadmin
```

### Avvio dell'Applicazione
```bash
# Avvia solo l'applicazione (dopo che il DB è pronto)
docker-compose up -d brokerflow
```

## 📞 Risoluzione Problemi

### Problemi di Avvio
```bash
# Se i servizi non si avviano, controlla i log
docker-compose logs

# Verifica che tutte le immagini siano state costruite correttamente
docker-compose build --no-cache
```

### Problemi di Connessione al Database
```bash
# Verifica che il database sia in ascolto
docker-compose exec db mysql -u root -proot123 -e "SELECT 1;"

# Controlla le variabili d'ambiente nel container brokerflow
docker-compose exec brokerflow env | grep MYSQL
```

### Reset Completo dell'Ambiente
```bash
# ATTENZIONE: Questo cancellerà tutti i dati!
docker-compose down -v
docker volume prune
docker image prune

# Ricostruisci tutto da zero
docker-compose up --build
```

## 🎯 Flusso di Lavoro Tipico

1. **Avvio ambiente**: `docker-compose up -d`
2. **Accesso phpMyAdmin**: http://localhost:8080
3. **Verifica API**: `curl http://localhost:8000/api/v1/health`
4. **Creazione documenti test**: `docker-compose exec brokerflow python create_sample_pdf.py`
5. **Testing funzionalità**: Usa l'API o il frontend
6. **Arresto ambiente**: `docker-compose down`

## 📚 Risorse Utili

- **Documentazione API**: http://localhost:8000/docs
- **phpMyAdmin**: http://localhost:8080
- **Log applicazione**: `docker-compose logs brokerflow`
- **Log database**: `docker-compose logs db`

L'ambiente Docker è configurato per fornire uno sviluppo e testing rapido e riproducibile, con persistenza dei dati tra i riavvii.