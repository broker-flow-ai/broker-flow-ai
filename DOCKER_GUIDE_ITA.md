   1 # Nella tua macchina Ubuntu:
   2 cd ~/progetti/broker-flow-ai
   3 docker compose down
   4 docker compose up -d --build
   5 docker compose exec brokerflow python main.py

# BrokerFlow AI - Docker Guide (ITA)
## 🐳 Panoramica

Questa guida fornisce istruzioni complete per l'utilizzo di Docker con BrokerFlow AI, coprendo tutto dal setup base al deployment in produzione.

## 📋 Prerequisiti

### Requisiti di Sistema
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB+ RAM consigliati
- 10GB+ spazio disco libero

### Installazione
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows
# Installa Docker Desktop da https://www.docker.com/products/docker-desktop
```

### Verifica
```bash
docker --version
docker-compose --version
docker info
```

## 🚀 Avvio Veloce

### 1. Clona e Configura
```bash
git clone https://github.com/yourorganization/brokerflow-ai.git
cd brokerflow-ai
```

### 2. Configura l'Ambiente
```bash
cp .env.example .env
# Modifica .env con la tua configurazione
```

### 3. Build e Avvia
```bash
docker-compose up -d
```

### 4. Accedi ai Servizi
- Applicazione: http://localhost:8000
- phpMyAdmin: http://localhost:8080
- MySQL: localhost:3306

## 📁 Analisi Dockerfile

### Immagine Base
```dockerfile
FROM python:3.10-slim
```
- Usa l'immagine ufficiale Python 3.10 slim per ridurre le dimensioni
- Basata su Debian per compatibilità

### Directory di Lavoro
```dockerfile
WORKDIR /app
```
- Imposta `/app` come directory di lavoro
- Tutti i comandi successivi vengono eseguiti da questa directory

### Variabili d'Ambiente
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```
- Impedisce a Python di scrivere file bytecode
- Assicura che l'output di Python non sia bufferizzato

### Dipendenze di Sistema
```dockerfile
RUN apt-get update \\
    && apt-get install -y --no-install-recommends \\
        gcc \\
        default-libmysqlclient-dev \\
        pkg-config \\
        tesseract-ocr \\
        libtesseract-dev \\
        poppler-utils \\
    && rm -rf /var/lib/apt/lists/*
```
- Installa strumenti di build essenziali
- Header di sviluppo client MySQL
- Motore OCR Tesseract e librerie
- Utilità Poppler per elaborazione PDF
- Pulisce la cache dei pacchetti per ridurre le dimensioni dell'immagine

### Dipendenze Python
```dockerfile
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
```
- Copia requirements di runtime e sviluppo
- Installa dipendenze senza caching per ridurre le dimensioni dell'immagine

### Codice Applicazione
```dockerfile
COPY . .
```
- Copia l'intero codebase dell'applicazione
- Esclude file specificati in `.gitignore`

### Setup Directory
```dockerfile
RUN mkdir -p inbox output templates
```
- Crea le directory necessarie per l'elaborazione dei file

### Esposizione Porte
```dockerfile
EXPOSE 8000
```
- Espone la porta 8000 per l'accesso API
- Non pubblica la porta (usa docker-compose per quello)

### Sicurezza
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser
```
- Crea utente non-root per sicurezza
- Cambia la proprietà dei file dell'applicazione
- Esegue il container come utente non-root

### Comando di Avvio
```dockerfile
CMD [\"python\", \"main.py\"]
```
- Comando predefinito per eseguire l'applicazione

## 🐳 Configurazione Docker Compose

### Panoramica Servizi
```yaml
version: '3.8'

services:
  brokerflow:    # Applicazione principale
  db:           # Database MySQL
  phpmyadmin:   # Interfaccia gestione database
  redis:        # Servizio cache
```

### 1. Servizio Applicazione Principale
```yaml
brokerflow:
  build: .
  ports:
    - \"8000:8000\"
  environment:
    - MYSQL_HOST=db
    - MYSQL_USER=brokerflow
    - MYSQL_PASSWORD=brokerflow123
    - MYSQL_DATABASE=brokerflow_ai
    - OPENAI_API_KEY=${OPENAI_API_KEY}
  volumes:
    - ./inbox:/app/inbox
    - ./output:/app/output
    - ./templates:/app/templates
    - ./logs:/app/logs
  depends_on:
    - db
  restart: unless-stopped
```

**Configurazione Principale:**
- **Build**: Costruisce dall'attuale Dockerfile
- **Ports**: Mappa la porta host 8000 alla porta container 8000
- **Environment**: Imposta variabili d'ambiente per database e API key
- **Volumes**: Monta directory host per dati persistenti
- **Depends On**: Assicura che il database si avvii prima dell'applicazione
- **Restart**: Riavvia automaticamente a meno che non venga fermato manualmente

### 2. Servizio Database
```yaml
db:
  image: mysql:8.0
  environment:
    - MYSQL_ROOT_PASSWORD=root123
    - MYSQL_USER=brokerflow
    - MYSQL_PASSWORD=brokerflow123
    - MYSQL_DATABASE=brokerflow_ai
  volumes:
    - db_data:/var/lib/mysql
    - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
  ports:
    - \"3306:3306\"
  restart: unless-stopped
```

**Configurazione Principale:**
- **Image**: Immagine MySQL 8.0 ufficiale
- **Environment**: Credenziali database e setup iniziale
- **Volumes**: 
  - `db_data`: Volume nominato per storage persistente
  - `schema.sql`: Inizializza lo schema database
- **Ports**: Espone la porta MySQL per accesso esterno

### 3. Servizio phpMyAdmin
```yaml
phpmyadmin:
  image: phpmyadmin/phpmyadmin
  environment:
    - PMA_HOST=db
    - PMA_USER=root
    - PMA_PASSWORD=root123
  ports:
    - \"8080:80\"
  depends_on:
    - db
  restart: unless-stopped
```

**Configurazione Principale:**
- **Image**: Immagine phpMyAdmin ufficiale
- **Environment**: Connette al database MySQL
- **Ports**: Mappa la porta host 8080 alla porta container 80
- **Depends On**: Assicura che il database si avvii prima

### 4. Servizio Redis
```yaml
redis:
  image: redis:7-alpine
  ports:
    - \"6379:6379\"
  restart: unless-stopped
```

**Configurazione Principale:**
- **Image**: Immagine Redis Alpine leggera
- **Ports**: Espone la porta Redis per caching
- **Restart**: Policy di riavvio automatico

### Volumi
```yaml
volumes:
  db_data:
```
- **db_data**: Volume nominato per storage database persistente

## ⚙️ Configurazione Ambiente

### Struttura File .env
```bash
# Configurazione OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Configurazione Database MySQL
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=brokerflow_ai

# Configurazione Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# Configurazione Sistema
INBOX_PATH=inbox/
OUTPUT_PATH=output/
TEMPLATE_PATH=templates/

# Configurazione Logging
LOG_LEVEL=INFO
LOG_FILE=brokerflow.log

# Configurazione Sicurezza
SECRET_KEY=your_secret_key_here
JWT_EXPIRATION_DAYS=30
```

### Variabili d'Ambiente Docker
Le variabili possono essere impostate in diversi modi:

1. **File .env** (consigliato per sviluppo)
2. **Linea di comando** (per override)
3. **Docker Compose** (per impostazioni specifiche servizio)

### Dati Sensibili
```bash
# Non committare mai le API key nel version control
# Usa il file .env e aggiungilo a .gitignore
echo \".env\" >> .gitignore
```

## ▶️ Esecuzione Servizi Docker

### Comandi Base

#### Avvia Tutti i Servizi
```bash
docker-compose up -d
```
- `-d`: Esegue in modalità detached (background)

#### Visualizza Log
```bash
# Tutti i servizi
docker-compose logs -f

# Servizio specifico
docker-compose logs -f brokerflow

# Ultime 100 righe
docker-compose logs --tail=100 brokerflow
```

#### Ferma Servizi
```bash
# Ferma tutti i servizi
docker-compose down

# Ferma servizio specifico
docker-compose stop brokerflow

# Ferma e rimuove volumi
docker-compose down -v
```

#### Riavvia Servizi
```bash
# Riavvia tutti i servizi
docker-compose restart

# Riavvia servizio specifico
docker-compose restart db
```

### Gestione Servizi

#### Visualizza Servizi in Esecuzione
```bash
docker-compose ps
```

#### Esegui Comandi nel Container
```bash
# Accedi alla shell del container
docker-compose exec brokerflow bash

# Esegui comando specifico
docker-compose exec brokerflow python main.py

# Accedi al database
docker-compose exec db mysql -u brokerflow -p brokerflow_ai
```

#### Build Immagini
```bash
# Ricostruisci tutti i servizi
docker-compose build

# Ricostruisci servizio specifico
docker-compose build brokerflow

# Forza ricostruzione senza cache
docker-compose build --no-cache brokerflow
```

## 📁 Gestione Volumi

### Tipi di Volumi

#### Volumi Nominati
```yaml
volumes:
  db_data:
```
- Gestiti da Docker
- Persistenti tra riavvii container
- Posizionati nell'area di storage di Docker

#### Bind Mounts
```yaml
volumes:
  - ./inbox:/app/inbox
  - ./output:/app/output
```
- Mappa directory host a container
- Accesso diretto ai file dall'host
- Utili per sviluppo

### Comandi Volumi

#### Elenca Volumi
```bash
docker volume ls
```

#### Ispeziona Volume
```bash
docker volume inspect brokerflow_ai_db_data
```

#### Rimuovi Volumi
```bash
# Rimuovi volume specifico
docker volume rm brokerflow_ai_db_data

# Rimuovi volumi inutilizzati
docker volume prune
```

### Persistenza Dati

#### Backup Volume Database
```bash
# Crea backup
docker run --rm \\
  -v brokerflow_ai_db_data:/source \\
  -v $(pwd):/backup \\
  alpine tar czf /backup/db_backup.tar.gz -C /source .
```

#### Ripristina Volume Database
```bash
# Ripristina da backup
docker run --rm \\
  -v brokerflow_ai_db_data:/target \\
  -v $(pwd):/backup \\
  alpine tar xzf /backup/db_backup.tar.gz -C /target
```

## 🔧 Configurazione e Personalizzazione

### Dockerfile Personalizzato
Crea `Dockerfile.custom` per esigenze specifiche:

```dockerfile
FROM brokerflow/brokerflow-ai:latest

# Installa dipendenze aggiuntive
RUN apt-get update && apt-get install -y \\
    additional-package \\
    && rm -rf /var/lib/apt/lists/*

# Copia configurazione personalizzata
COPY custom-config.yaml /app/config/custom.yaml

# Espone porte aggiuntive
EXPOSE 8000 9000

# Comando di avvio personalizzato
CMD [\"python\", \"main.py\", \"--config\", \"custom.yaml\"]
```

### File Compose Specifici per Ambiente
Crea `docker-compose.prod.yml` per produzione:

```yaml
version: '3.8'

services:
  brokerflow:
    build: .
    environment:
      - DEBUG=false
      - LOG_LEVEL=WARNING
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    restart: always

  db:
    environment:
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_root_password
    secrets:
      - db_root_password

secrets:
  db_root_password:
    file: ./secrets/db_root_password.txt
```

### Override Configurazione
```bash
# Usa file compose multipli
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🛠 Risoluzione Problemi

### Problemi Comuni

#### 1. Porta Già in Uso
```bash
# Controlla quale processo usa la porta
lsof -i :8000

# Termina il processo
kill -9 <PID>

# O cambia porta in docker-compose.yml
```

#### 2. Problemi Connessione Database
```bash
# Controlla se il database è in esecuzione
docker-compose ps db

# Controlla log database
docker-compose logs db

# Testa connessione database
docker-compose exec brokerflow \\
  mysql -h db -u brokerflow -p brokerflow_ai -e \"SELECT 1;\"
```

#### 3. Problemi Permessi
```bash
# Correggi permessi file
sudo chown -R $(id -u):$(id -g) inbox output templates logs

# O esegui come root (non consigliato per produzione)
# Rimuovi USER appuser dal Dockerfile
```

#### 4. Problemi Mount Volumi
```bash
# Controlla mount volumi
docker-compose exec brokerflow ls -la /app

# Verifica esistenza directory host
ls -la inbox output templates
```

### Comandi Debug

#### Informazioni Container
```bash
# Ispeziona container
docker inspect brokerflow_ai_brokerflow_1

# Controlla risorse container
docker stats brokerflow_ai_brokerflow_1

# Visualizza processi container
docker top brokerflow_ai_brokerflow_1
```

#### Debug Rete
```bash
# Controlla configurazione rete
docker network ls
docker network inspect brokerflow_ai_default

# Testa connettività tra container
docker-compose exec brokerflow ping db
```

#### Debug Immagini
```bash
# Visualizza layer immagine
docker history brokerflow/brokerflow-ai

# Ispeziona immagine
docker inspect brokerflow/brokerflow-ai:latest
```

## 📊 Monitoraggio e Logging

### Logging Docker

#### Configura Driver Logging
```yaml
services:
  brokerflow:
    logging:
      driver: \"json-file\"
      options:
        max-size: \"10m\"
        max-file: \"3\"
```

#### Visualizza Log
```bash
# Log in tempo reale
docker-compose logs -f

# Filtra log per data
docker-compose logs --since=\"2025-08-13\"

# Filtra log per pattern
docker-compose logs | grep ERROR
```

### Monitoraggio Risorse

#### Risorse Container
```bash
# Monitora tutti i container
docker stats

# Monitora container specifico
docker stats brokerflow_ai_brokerflow_1
```

#### Risorse Sistema
```bash
# Controlla statistiche Docker daemon
docker system df

# Visualizza informazioni sistema
docker info
```

## 🚀 Deployment Produzione

### Best Practices

#### Sicurezza
```yaml
# docker-compose.yml produzione
services:
  brokerflow:
    environment:
      - DEBUG=false
      - SECRET_KEY_FILE=/run/secrets/secret_key
    secrets:
      - secret_key
    restart: always
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
```

#### Limiti Risorse
```yaml
services:
  brokerflow:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

#### Health Checks
```yaml
services:
  brokerflow:
    healthcheck:
      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:8000/health\"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Scaling

#### Scaling Orizzontale
```bash
# Scala servizio specifico
docker-compose up -d --scale brokerflow=3
```

#### Load Balancing
Usa load balancer esterno come NGINX o HAProxy per produzione.

### Strategia Backup

#### Backup Automatici
```bash
# Crea script backup
#!/bin/bash
docker-compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD brokerflow_ai > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Backup Pianificati
```bash
# Aggiungi a crontab
0 2 * * * /path/to/backup_script.sh
```

## 🔒 Considerazioni Sicurezza

### Sicurezza Immagini
```bash
# Scansiona immagini per vulnerabilità
docker scan brokerflow/brokerflow-ai

# Usa immagini base ufficiali
# Mantieni immagini aggiornate
# Rimuovi pacchetti non necessari
```

### Sicurezza Runtime
```yaml
services:
  brokerflow:
    user: \"1000:1000\"  # Utente non-root
    read_only: true    # Filesystem read-only
    tmpfs:
      - /tmp          # Filesystem temporaneo scrivibile
    security_opt:
      - no-new-privileges:true
```

### Gestione Secret
```yaml
# Usa Docker secrets
services:
  brokerflow:
    secrets:
      - db_password
      - openai_api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  openai_api_key:
    file: ./secrets/openai_api_key.txt
```

## 🎯 Utilizzo Avanzato

### Build Multi-stage
```dockerfile
# Stage build
FROM python:3.10-slim as builder
# Installa dipendenze build e compila

# Stage runtime
FROM python:3.10-slim as runtime
# Copia solo file necessari dal builder
# Installa solo dipendenze runtime
```

### Reti Personalizzate
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  brokerflow:
    networks:
      - frontend
      - backend
```

### Volumi Nominati per Path Specifici
```yaml
volumes:
  db_data:
  logs_data:

services:
  brokerflow:
    volumes:
      - logs_data:/app/logs
  db:
    volumes:
      - db_data:/var/lib/mysql
```

## 📞 Supporto

### Documentazione
- Guide utente nella directory `docs/`
- Documentazione API
- Guide risoluzione problemi

### Supporto Community
- GitHub Issues: https://github.com/yourorganization/brokerflow-ai/issues
- GitHub Discussions: https://github.com/yourorganization/brokerflow-ai/discussions

### Supporto Professionale
- Email: support@brokerflow.ai
- SLA: Supporto 24/7 per clienti enterprise

---

*Ultimo aggiornamento: 13 agosto 2025*
*Versione: 1.0*