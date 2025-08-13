# BrokerFlow AI - Guida all'Installazione

## 📋 Prerequisiti di Sistema

### Sistema Operativo
- Windows 10/11, macOS 10.14+, o Linux (Ubuntu 18.04+, CentOS 7+)

### Software Richiesti
- Python 3.8 o superiore
- Git (opzionale, per clonare il repository)
- MySQL 5.7 o superiore (per versione completa)

### Software Opzionale
- Tesseract OCR (per PDF scansionati)
- Docker (per deployment containerizzato)

## 🚀 Installazione Passo-passo

### 1. Clonare il Repository
```bash
git clone https://github.com/tuonome/broker-flow-ai.git
cd broker-flow-ai
```

### 2. Creare un Ambiente Virtuale (Consigliato)
```bash
python -m venv brokerflow-env
# Su Windows
brokerflow-env\Scripts\activate
# Su macOS/Linux
source brokerflow-env/bin/activate
```

### 3. Installare le Dipendenze Python
```bash
pip install -r requirements.txt
```

### 4. Installare Tesseract OCR (Per PDF Scansionati)
#### Windows
1. Scarica l'installer da: https://github.com/UB-Mannheim/tesseract/wiki
2. Esegui l'installer e segui le istruzioni
3. Aggiungi Tesseract al PATH di sistema

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 5. Configurare le Variabili d'Ambiente
1. Copia il file di esempio:
   ```bash
   cp .env.example .env
   ```
2. Modifica `.env` con i tuoi valori:
   ```bash
   OPENAI_API_KEY=sk-tua_api_key_qui
   MYSQL_HOST=localhost
   MYSQL_USER=tuo_username
   MYSQL_PASSWORD=tua_password
   MYSQL_DATABASE=brokerflow_ai
   ```

### 6. Configurare il Database MySQL (Versione Completa)
1. Crea il database:
   ```sql
   CREATE DATABASE brokerflow_ai;
   ```
2. Esegui lo schema:
   ```bash
   mysql -u tuo_username -p brokerflow_ai < schema.sql
   ```

## 📁 Configurazione delle Directory

### Directory Predefinite
- `inbox/`: Posiziona qui i PDF da elaborare
- `output/`: Qui verranno salvati i risultati
- `templates/`: Posiziona qui i moduli PDF delle compagnie

### Personalizzazione Path
Modifica `config.py` per cambiare i path predefiniti:
```python
INBOX_PATH = "/custom/path/to/inbox/"
OUTPUT_PATH = "/custom/path/to/output/"
TEMPLATE_PATH = "/custom/path/to/templates/"
```

## 🔧 Verifica dell'Installazione

### Test della Versione Demo
```bash
python main_simulated.py
```
Dovresti vedere un output simile a:
```
Processing sample_flotta.pdf...
Text extracted.
Risk classified as: Flotta Auto
Form compiled at output/compiled_sample_flotta.pdf
Email generated.
Request saved to DB.
```

### Test della Versione Completa (Se Tutto Configurato)
```bash
python main.py
```

## 🛠 Troubleshooting

### Problemi Comuni

#### 1. "ModuleNotFoundError"
**Causa**: Dipendenze non installate
**Soluzione**:
```bash
pip install -r requirements.txt
```

#### 2. "Tesseract not found"
**Causa**: Tesseract non installato o non nel PATH
**Soluzione**:
- Verifica l'installazione di Tesseract
- Riavvia il terminale dopo l'installazione
- Verifica il PATH di sistema

#### 3. "MySQL connection failed"
**Causa**: Credenziali o configurazione errata
**Soluzione**:
- Verifica che MySQL sia in esecuzione
- Controlla le credenziali nel file `.env`
- Verifica che il database `brokerflow_ai` esista

#### 4. "Permission denied" su Windows
**Causa**: Permessi insufficienti
**Soluzione**:
- Esegui il terminale come amministratore
- Verifica i permessi sulle directory

### Verifica delle Dipendenze
```bash
# Verifica Python
python --version

# Verifica pip
pip --version

# Verifica Tesseract (se installato)
tesseract --version

# Verifica connessione MySQL (se configurato)
mysql --version
```

## 🔄 Aggiornamento del Sistema

### Aggiornamento dal Repository
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Aggiornamento del Database
Se lo schema è cambiato:
```bash
mysql -u tuo_username -p brokerflow_ai < schema.sql
```

## 🔒 Sicurezza

### Best Practice per l'Installazione
1. Usa un ambiente virtuale
2. Non salvare credenziali nel codice
3. Usa permessi minimi per l'utente MySQL
4. Mantieni aggiornate le dipendenze

### Configurazione Firewall
Se esposto su rete:
- Limita l'accesso alla porta MySQL
- Usa connessioni SSL per il database
- Implementa autenticazione per l'API

## 📈 Performance e Scalabilità

### Ottimizzazione per Grandi Volumi
1. Usa SSD per storage
2. Configura MySQL con parametri ottimizzati
3. Considera l'uso di worker paralleli

### Monitoraggio delle Risorse
- CPU: Monitora durante l'elaborazione OCR
- RAM: PyMuPDF può essere memory-intensive
- Disk I/O: Operazioni di lettura/scrittura file

## 🧪 Test Post-Installazione

### Test Funzionali
1. Elabora un PDF di esempio
2. Verifica che l'output sia corretto
3. Controlla che i dati siano salvati nel database

### Test di Carico
1. Elabora più PDF contemporaneamente
2. Verifica tempi di risposta
3. Monitora l'uso delle risorse

## 📞 Supporto

### Documentazione
- `DOCUMENTAZIONE.md`: Panoramica tecnica
- `GUIDA_UTENTE.md`: Istruzioni per l'utente
- `SVILUPPO.md`: Guida per sviluppatori

### Segnalazione Problemi
1. Verifica di usare l'ultima versione
2. Controlla issue esistenti
3. Apri una nuova issue con:
   - Versione del software
   - Sistema operativo
   - Messaggio di errore completo
   - Passi per riprodurre il problema