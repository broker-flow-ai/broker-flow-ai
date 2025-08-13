# BrokerFlow AI - Installazione Docker su Ubuntu e Avvio Progetto

## 🐧 Installazione Docker su Ubuntu

### Prerequisiti
Docker supporta le seguenti versioni di Ubuntu:
- Ubuntu Jammy 22.04 (LTS)
- Ubuntu Impish 21.10
- Ubuntu Focal 20.04 (LTS)
- Ubuntu Bionic 18.04 (LTS)

### 1. Aggiorna il Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Installa le Dipendenze Richieste
```bash
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y
```

### 3. Aggiungi la Chiave GPG Ufficiale di Docker
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### 4. Aggiungi il Repository di Docker
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 5. Aggiorna l'Indice dei Pacchetti
```bash
sudo apt update
```

### 6. Installa Docker Engine
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

### 7. Verifica l'Installazione
```bash
sudo docker --version
sudo docker compose version
```

### 8. Esegui Docker senza Sudo (Opzionale ma Consigliato)
```bash
# Aggiungi il tuo utente al gruppo docker
sudo usermod -aG docker $USER

# Applica le modifiche (logout e login richiesto)
newgrp docker

# Verifica
docker run hello-world
```

## 🐳 Installazione Docker Compose (Se Necessario)

Se `docker compose` non è disponibile, installa separatamente:

### Metodo 1: Usando il Plugin Ufficiale (Consigliato)
```bash
sudo apt install docker-compose-plugin
```

### Metodo 2: Download Binario
```bash
# Scarica l'ultima versione
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Rendi eseguibile
sudo chmod +x /usr/local/bin/docker-compose

# Crea link simbolico (opzionale)
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verifica
docker-compose --version
```

## ▶️ Avvio Progetto BrokerFlow AI

### 1. Clona il Repository
```bash
git clone https://github.com/yourorganization/brokerflow-ai.git
cd brokerflow-ai
```

### 2. Configura l'Ambiente
```bash
# Copia il file di esempio
cp .env.example .env

# Modifica le configurazioni sensibili (opzionale)
nano .env
```

### 3. Verifica la Configurazione Docker
Controlla che i file siano corretti:
```bash
# Verifica docker-compose.yml
cat docker-compose.yml

# Verifica .env
cat .env
```

### 4. Costruisci e Avvia i Container
```bash
# Avvia in modalità detached (background)
docker compose up -d

# Visualizza i log per verificare l'avvio
docker compose logs -f
```

### 5. Verifica i Servizi
```bash
# Controlla i container in esecuzione
docker compose ps

# Dovresti vedere:
# - brokerflow_ai_brokerflow_1
# - brokerflow_ai_db_1
# - brokerflow_ai_phpmyadmin_1
# - brokerflow_ai_redis_1
```

### 6. Accedi ai Servizi
- **Applicazione BrokerFlow AI**: http://localhost:8000
- **phpMyAdmin**: http://localhost:8080
- **Database MySQL**: localhost:3306

## 🔧 Configurazione Iniziale

### 1. Configura le API Key
```bash
# Modifica il file .env
nano .env

# Imposta la tua OpenAI API Key
OPENAI_API_KEY=sk-tua_api_key_reale_qui
```

### 2. Riavvia i Servizi
```bash
# Riavvia per applicare le nuove configurazioni
docker compose down
docker compose up -d
```

### 3. Verifica la Connessione al Database
```bash
# Accedi al container dell'applicazione
docker compose exec brokerflow bash

# Verifica la connessione al database
mysql -h db -u brokerflow -p brokerflow_ai -e "SHOW TABLES;"

# Esci dal container
exit
```

## 📁 Gestione File e Directory

### 1. Prepara le Directory Necessarie
```bash
# Verifica che le directory esistano
ls -la inbox/ output/ templates/

# Se non esistono, creale
mkdir -p inbox output templates logs
```

### 2. Aggiungi Template PDF
```bash
# Copia i tuoi template PDF nella directory templates/
cp /percorso/ai/tuoi/template/*.pdf templates/
```

### 3. Permessi delle Directory
```bash
# Assicurati che i permessi siano corretti
sudo chown -R $USER:$USER inbox output templates logs
```

## 🔍 Troubleshooting Comuni

### 1. Permessi Docker
Se ricevi errori di permessi:
```bash
# Aggiungi il tuo utente al gruppo docker
sudo usermod -aG docker $USER

# Logout e login, oppure esegui:
newgrp docker
```

### 2. Porte Occupate
Se le porte sono già in uso:
```bash
# Controlla quali processi usano le porte
sudo lsof -i :8000
sudo lsof -i :3306
sudo lsof -i :8080

# Termina i processi se necessario
sudo kill -9 <PID>
```

### 3. Problemi con i Volumi
```bash
# Rimuovi volumi e container (perdi i dati!)
docker compose down -v

# Ricrea tutto
docker compose up -d
```

### 4. Problemi di Build
```bash
# Forza la ricostruzione senza cache
docker compose build --no-cache

# Riavvia tutto
docker compose up -d
```

## 🛠 Comandi Utili

### Gestione Servizi
```bash
# Avvia servizi
docker compose up -d

# Ferma servizi
docker compose down

# Riavvia servizi
docker compose restart

# Visualizza log
docker compose logs -f

# Visualizza log servizio specifico
docker compose logs -f brokerflow
```

### Gestione Container
```bash
# Lista container
docker compose ps

# Accedi alla shell di un container
docker compose exec brokerflow bash

# Esegui comando in container
docker compose exec brokerflow python main.py
```

### Gestione Immagini
```bash
# Lista immagini
docker images

# Rimuovi immagini non usate
docker image prune

# Rimuovi tutti i container fermi
docker container prune
```

## 🔒 Sicurezza

### 1. Cambia le Password di Default
```bash
# Modifica .env con password sicure
nano .env

# Cambia:
MYSQL_PASSWORD=password_piu_sicuro
MYSQL_ROOT_PASSWORD=root_password_piu_sicura
```

### 2. Aggiorna Regolarmente
```bash
# Aggiorna Docker
sudo apt update
sudo apt upgrade docker-ce

# Aggiorna immagini
docker compose pull
docker compose up -d
```

## 📊 Monitoraggio

### 1. Risorse di Sistema
```bash
# Monitora le risorse dei container
docker stats

# Informazioni dettagliate su un container
docker inspect brokerflow_ai_brokerflow_1
```

### 2. Utilizzo Disco
```bash
# Spazio usato da Docker
docker system df

# Pulisci sistema (rimuove dati non usati)
docker system prune -a
```

## 🎯 Pronto per l'Uso

Dopo aver completato questi passaggi, il tuo sistema BrokerFlow AI sarà:

✅ **Docker installato e configurato**
✅ **Tutti i servizi in esecuzione**
✅ **Database connesso**
✅ **Applicazione accessibile**
✅ **Ambiente pronto per l'elaborazione**

### Prossimi Passi:
1. **Aggiungi i tuoi template PDF** nella directory `templates/`
2. **Configura le API Key** nel file `.env`
3. **Testa l'elaborazione** con PDF di esempio nella directory `inbox/`
4. **Consulta la guida utente** per l'uso quotidiano

---

*Ultimo aggiornamento: 13 agosto 2025*