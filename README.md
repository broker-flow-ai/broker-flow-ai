# BrokerFlow AI - README

## 🎯 Cos'è BrokerFlow AI?

BrokerFlow AI è una **piattaforma intelligente B2B2B** progettata per **automatizzare l'intero ciclo di vita del processo assicurativo** per compagnie assicurative e broker. Trasforma semplici richieste in polizze complete con analisi predittiva, compliance automatizzata e dashboard executive.

## 🚀 Funzionalità Principali

### Per Compagnie Assicurative
- **Analisi Rischio Avanzata**: AI-powered risk scoring e underwriting
- **Dashboard Executive**: Analisi portafoglio, performance KPI, trend di mercato
- **Compliance Automatizzata**: Report GDPR/SOX/IVASS generati automaticamente
- **AI Pricing & Predizione**: Suggerimenti premi e previsione sinistri
- **Integrazioni Enterprise**: Connettori SGA, portali broker, gateway pagamento

### Per Broker Assicurativi
- **Lettura Intelligente PDF**: Supporto per PDF digitali e scansionati
- **Classificazione Automatica**: Riconoscimento del tipo di rischio assicurativo
- **Compilazione Moduli**: Generazione automatica di preventivi PDF
- **Email Personalizzate**: Creazione e invio di email ai clienti
- **Tracciamento Richieste**: Database integrato per monitorare le richieste
- **Programmi Fedeltà**: Sconti volume e performance basati su AI

## 🏗️ Architettura Estesa

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                        │
├─────────────────────────────────────────────────────────────┤
│                    Processing Layer                         │
├─────────────────────────────────────────────────────────────┤
│                    Integration Layer                        │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer                               │
└─────────────────────────────────────────────────────────────┘
```

### Componenti Principali
- **Frontend Dashboard**: Interfaccia web completa con Streamlit
- **API B2B2B**: REST API enterprise con FastAPI
- **Moduli AI**: Analisi rischio, pricing, underwriting, predizione sinistri
- **Integrazioni**: Connettori SGA, portali broker, sistemi di pagamento
- **Compliance**: Report automatici per normative assicurative
- **Programmi Fedeltà**: Gestione sconti e metriche performance

## 📦 Cosa c'è nella Scatola?

```
brokerflow_ai/
├── inbox/                 # PDF in arrivo da elaborare
├── output/                # Preventivi e email generati
├── templates/             # Moduli PDF delle compagnie
├── modules/               # Moduli core del sistema
├── frontend/              # Interfaccia web dashboard
├── api_b2b.py            # API REST enterprise
├── DOCUMENTAZIONE.md      # Documentazione tecnica completa
├── MODULES.md            # Dettaglio moduli implementati
├── GUIDA_UTENTE.md        # Istruzioni per l'utente
├── SVILUPPO.md            # Guida per sviluppatori
├── INSTALLAZIONE.md       # Guida all'installazione
├── CHANGELOG.md           # Registro modifiche
├── requirements.txt       # Dipendenze Python
├── schema.sql            # Schema database esteso
├── Dockerfile            # Configurazione Docker
├── docker-compose.yml    # Orchestrazione Docker
├── .env.example          # Esempio configurazione
└── ...                   # Altri file di configurazione
```

## 🐳 Come Iniziare con Docker (Consigliato)

### Requisiti
- Docker e Docker Compose
- Almeno 4GB di RAM disponibili
- 2GB di spazio su disco

### Installazione Veloce con Docker
```bash
# Clona il repository
git clone https://github.com/tuonome/broker-flow-ai.git
cd broker-flow-ai

# Copia il file di configurazione
cp .env.example .env
# Modifica .env con la tua API Key OpenAI (opzionale per demo)

# Avvia tutti i servizi
docker-compose up -d

# L'applicazione sarà accessibile su:
# API: http://localhost:8000
# Frontend: http://localhost:8501
# phpMyAdmin: http://localhost:8080
```

## 💻 Installazione Manuale (Alternative)

### Requisiti
- Python 3.8+
- MySQL 5.7+
- Tesseract OCR (opzionale, per PDF scansionati)
- OpenAI API Key (per funzionalità AI)

### Installazione Veloce
```bash
# Clona il repository
git clone https://github.com/tuonome/broker-flow-ai.git
cd broker-flow-ai

# Crea ambiente virtuale
python -m venv brokerflow-env
source brokerflow-env/bin/activate  # Su Windows: brokerflow-env\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Configura le variabili d'ambiente
cp .env.example .env
# Modifica .env con le tue credenziali

# Aggiorna schema database
mysql -u tuo_utente -p < schema.sql

# Avvia il server API
uvicorn api_b2b:app --reload

# In un altro terminale, avvia il frontend
streamlit run frontend/dashboard.py
```

## 🧪 Testing dell'Ambiente

### Con Docker
```bash
# Verifica che tutti i servizi siano attivi
docker-compose ps

# Esegui il testing completo
docker-compose exec api python -m pytest

# Oppure segui la guida DOCKER_TESTING.md per test manuali
```

### Manuale
```bash
# Segui la guida TESTING_GUIDE.md per test completi
```

## 📖 Documentazione Completa

- 📚 **[DOCUMENTAZIONE TECNICA](DOCUMENTAZIONE.md)** - Dettagli tecnici dell'implementazione
- 🧩 **[MODULES.md](MODULES.md)** - Descrizione moduli implementati
- 👤 **[GUIDA UTENTE](GUIDA_UTENTE.md)** - Istruzioni per l'uso quotidiano
- 💻 **[GUIDA SVILUPPO](SVILUPPO.md)** - Estendere e modificare il sistema
- ⚙️ **[INSTALLAZIONE.md](INSTALLAZIONE.md)** - Setup completo del sistema
- 🐳 **[DOCKER_USAGE.md](DOCKER_USAGE.md)** - Uso dell'ambiente Docker
- 🧪 **[DOCKER_TESTING.md](DOCKER_TESTING.md)** - Testing con Docker
- 🧪 **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing manuale
- 📋 **[CHANGELOG](CHANGELOG.md)** - Storico delle versioni

## 🎯 Casi d'Uso

### Compagnie Assicurative
- **Analisi Portfolio**: Dashboard executive con KPI in tempo reale
- **Underwriting AI**: Processo di valutazione rischi automatizzato
- **Compliance**: Report normativi generati automaticamente
- **Predizione Sinistri**: Modelli AI per anticipare sinistrosità
- **Integrazioni**: Connettori con SGA e portali broker

### Broker Assicurativi B2B
- **Automazione Preventivi**: Da richiesta a polizza in minuti
- **Comparazione Compagnie**: Analisi multi-compagnia automatizzata
- **Gestione Rinnovi**: Sistema di reminder e tracking
- **Programmi Fedeltà**: Sconti performance basati su AI
- **Report Cliente**: Dashboard personalizzate per clienti

### Consulenti Assicurativi
- **Standardizzazione**: Processi uniformi per tutti i clienti
- **Analisi Settoriale**: Benchmark per settori economici
- **Documentazione**: Tracciamento completo delle attività
- **Collaborazione**: Strumenti di condivisione con clienti

## 🔧 Requisiti di Sistema

### Con Docker (Consigliato)
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB RAM minimo (8GB consigliati)
- 2GB spazio su disco

### Manuale
- CPU: Dual core 2GHz
- RAM: 4GB
- Storage: 2GB disponibile
- Sistema: Windows 10+, macOS 10.14+, Linux
- Database: MySQL 5.7+

### Consigliati per Tutti gli Ambienti
- GPU: Consigliata per funzionalità AI avanzate
- SSD: Per migliori performance I/O
- Connessione Internet: Per API OpenAI e aggiornamenti

## 🔒 Sicurezza

- Tutti i dati rimangono locali
- Crittografia AES-256 per dati sensibili
- Autenticazione JWT per API
- Conforme a GDPR, SOX, IVASS
- Audit trail completo

## 📈 Vantaggi

| Beneficio | Miglioramento |
|----------|---------------|
| **Tempo** | Da 2-3 ore a 2-3 minuti per polizza completa |
| **Precisione** | Riduzione errori del 95% con AI |
| **Costi** | Risparmio fino al 70% su operazioni ripetitive |
| **Scalabilità** | Gestione fino a 10.000 polizze/giorno |
| **Compliance** | 100% report normativi automatizzati |
| **Decision Making** | KPI real-time per decisioni informate |

## 🤝 Contribuire

1. Forka il progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha il branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 📞 Contatti

- **Website**: https://brokerflow.ai
- **Email**: info@brokerflow.ai
- **Twitter**: [@BrokerFlowAI](https://twitter.com/BrokerFlowAI)
- **LinkedIn**: [BrokerFlow AI](https://linkedin.com/company/brokerflow-ai)

## 🙏 Ringraziamenti

- OpenAI per le API GPT
- Community open source per le librerie utilizzate
- Tutti i beta tester che hanno contribuito al progetto

---

<p align="center">
  Made with ❤️ for Insurance Companies & Brokers
</p>