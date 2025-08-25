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

## 🆕 Novità Recenti

### Agosto 2025 - Miglioramenti alla Compliance
- Implementata la generazione e il download di report di compliance in formato PDF, Excel e Word
- Aggiunta struttura database per tracciamento file generati in tutti i formati
- Creati endpoint API per download report in tutti i formati
- Implementata funzionalità di invio email con allegati
- Aggiunta tabella per tracciamento invii email
- Aggiornato sistema di tracciamento avanzamento sviluppo
- Implementata interfaccia utente per download ed invio report

## 📋 Indice dei Contenuti
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
├── TESTING_ESSENTIAL.md  # Guida essenziale al testing
├── CHANGELOG.md          # Registro modifiche
├── requirements.txt      # Dipendenze Python
├── schema.sql           # Schema database esteso
├── Dockerfile           # Configurazione Docker
├── docker-compose.yml   # Orchestrazione Docker
├── .env.example         # Esempio configurazione
└── ...                  # Altri file di configurazione
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

## 🧪 Testing dell'Ambiente

### Testing Rapido - Segui TESTING_ESSENTIAL.md
```bash
# Per un testing completo e guidato, consulta:
# TESTING_ESSENTIAL.md
```

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

## 🔧 Requisiti di Sistema

### Con Docker (Consigliato)
- Docker Engine 20.10+
- Docker Compose 1.29+
- 4GB RAM minimo (8GB consigliati)
- 2GB spazio su disco

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