# BrokerFlow AI - Documentazione Tecnica

## 📋 Panoramica

BrokerFlow AI è un sistema automatizzato per la gestione di preventivi assicurativi per broker. L'obiettivo è ridurre il lavoro manuale e accelerare il processo di emissione dei preventivi.

## 🏗️ Architettura del Sistema

```
brokerflow_ai/
│
├── inbox/                 # PDF in arrivo da elaborare
├── output/                # Risultati generati (PDF compilati, email)
├── templates/             # Moduli PDF standard delle compagnie
├── modules/               # Moduli core del sistema
│   ├── extract_data.py    # Estrazione testo da PDF
│   ├── classify_risk.py   # Classificazione del rischio
│   ├── compile_forms.py   # Compilazione moduli PDF
│   ├── generate_email.py  # Generazione email
│   └── db.py             # Gestione database
├── config.py             # Configurazione dell'app
├── schema.sql            # Schema database
├── requirements.txt      # Dipendenze Python
├── .env                  # Variabili d'ambiente
├── main.py               # Orchestrazione principale
└── main_simulated.py     # Versione demo senza dipendenze esterne
```

## 🧠 Flusso di Lavoro

1. **Input**: Un PDF con richiesta assicurativa viene salvato in `inbox/`
2. **Estrazione**: Il sistema legge il PDF e ne estrae il testo
3. **Classificazione**: Il tipo di rischio viene identificato
4. **Compilazione**: I dati vengono inseriti in un modulo PDF
5. **Output**: Un preventivo compilato e un'email vengono generati in `output/`
6. **Registrazione**: La richiesta viene salvata nel database

## 📦 Moduli Core

### 1. `extract_data.py`
Estrae testo da PDF sia digitali che scansionati:
- Per PDF digitali: usa PyMuPDF per estrarre testo direttamente
- Per PDF scansionati: usa OCR con pytesseract

### 2. `classify_risk.py`
Determina il tipo di rischio assicurativo:
- Nella versione demo: usa euristiche semplici
- Nella versione completa: usa OpenAI GPT per classificazione avanzata

### 3. `compile_forms.py`
Compila moduli PDF con i dati estratti:
- Usa PyPDF2 per manipolare PDF
- Richiede template PDF editabili

### 4. `generate_email.py`
Crea email personalizzate per i clienti:
- Genera subject e corpo dell'email
- Nella versione completa: può inviare email reali

### 5. `db.py`
Gestisce la connessione al database:
- Nella versione demo: simulata con file JSON
- Nella versione completa: connessione MySQL reale

## ⚙️ Configurazione

### Variabili d'Ambiente (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=brokerflow_ai
```

### Path Configurabili (config.py)
- `INBOX_PATH`: Cartella dei PDF in ingresso
- `OUTPUT_PATH`: Cartella dei risultati
- `TEMPLATE_PATH`: Cartella dei template PDF

## 🧪 Versione Demo

`main_simulated.py` permette di testare il flusso completo senza:
- Database MySQL reale
- API OpenAI
- Tesseract OCR installato

I risultati vengono salvati in file JSON e TXT per simulare il comportamento del sistema.

## 🔧 Dipendenze

Vedere `requirements.txt` per l'elenco completo delle dipendenze Python.

## 🚀 Avvio del Sistema

1. Posizionare un PDF in `inbox/`
2. Eseguire `python main.py` (richiede tutte le dipendenze)
   oppure
3. Eseguire `python main_simulated.py` (versione demo)

## 📁 File di Esempio

- `inbox/sample_flotta.pdf`: Esempio di richiesta per flotta auto
- `inbox/sample_rc_professionale.pdf`: Esempio di richiesta RC professionale
- `templates/template.pdf`: Template PDF di esempio

## 📊 Database Schema

Vedere `schema.sql` per lo schema del database MySQL con tabelle per:
- Richieste (`request_queue`)
- Clienti (`clients`)
- Rischi (`risks`)
- Polizze (`policies`)