# BrokerFlow AI - Guida allo Sviluppo

## 🎯 Obiettivo
Questa guida è per sviluppatori che vogliono estendere o modificare BrokerFlow AI.

## 🏗️ Struttura del Progetto

```
brokerflow_ai/
│
├── inbox/                 # PDF in arrivo (input)
├── output/                # PDF compilati e email (output)
├── templates/             # Moduli PDF delle compagnie
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
├── main_simulated.py     # Versione demo
├── DOCUMENTAZIONE.md     # Documentazione tecnica
├── GUIDA_UTENTE.md       # Guida per l'utente finale
├── INSTALLAZIONE.md      # Guida all'installazione
├── create_sample_pdf.py  # Script per creare PDF di esempio
├── create_template.py    # Script per creare template
└── ...                   # Altri file di supporto
```

## 🔧 Setup per Sviluppo

### Prerequisiti
- Python 3.8+
- MySQL 5.7+ (per versione completa)
- Tesseract OCR (per PDF scansionati)

### Installazione Dipendenze
```bash
pip install -r requirements.txt
```

### Configurazione
1. Copia `.env.example` in `.env`
2. Modifica le variabili con i tuoi valori

## 🧠 Architettura del Codice

### Principi di Design
1. **Modularità**: Ogni funzionalità è in un modulo separato
2. **Separazione dei Concern**: Logica di business separata dall'I/O
3. **Configurabilità**: Parametri esternalizzati
4. **Testabilità**: Facile da testare in isolamento

### Pattern Utilizzati
- **Strategy**: Per diversi tipi di estrazione/classificazione
- **Factory**: Per creare diversi tipi di output
- **Observer**: Per notifiche di stato (futura implementazione)

## 📦 Moduli Core - Dettagli Tecnici

### 1. `modules/extract_data.py`

#### Funzioni Principali
- `is_pdf_scanned(path)`: Determina se un PDF è scansionato
- `extract_text_from_pdf(path)`: Punto d'ingresso per estrazione
- `extract_text_digital(path)`: Estrae testo da PDF digitali
- `ocr_pdf(path)`: Esegue OCR su PDF scansionati

#### Dipendenze
- `PyMuPDF` (fitz): Per lettura PDF digitali
- `PyPDF2`: Per analisi struttura PDF
- `pdf2image`: Per conversione PDF->immagine
- `pytesseract`: Per OCR

#### Estendibilità
Puoi aggiungere nuovi metodi di estrazione:
```python
def extract_text_with_ai(path):
    # Implementazione con servizio AI esterno
    pass
```

### 2. `modules/classify_risk.py`

#### Funzioni Principali
- `classify_risk(text)`: Classifica il tipo di rischio

#### Versione Demo
Usa euristiche semplici basate su keywords:
```python
if "flotta" in text.lower():
    return "Flotta Auto"
```

#### Versione Completa
Integra OpenAI GPT:
```python
response = openai.Completion.create(
    engine="gpt-4",
    prompt=f"Classifica il rischio in: {text}"
)
```

#### Estendibilità
Aggiungi nuove categorie di rischio modificando il prompt o le regole.

### 3. `modules/compile_forms.py`

#### Funzioni Principali
- `compile_form(data, template_name, output_name)`: Compila un modulo PDF

#### Dipendenze
- `PyPDF2`: Per manipolazione PDF

#### Limitazioni Note
- Richiede PDF editabili con campi form
- Non supporta ancora compilazione complessa di tabelle

#### Estendibilità
```python
def compile_advanced_form(data, template_name, output_name):
    # Implementazione per PDF complessi
    pass
```

### 4. `modules/generate_email.py`

#### Funzioni Principali
- `generate_email(client_name, policy_paths)`: Genera email

#### Estendibilità
- Aggiungi template email diversi per tipi di rischio
- Integra invio email reale con SMTP

### 5. `modules/db.py`

#### Funzioni Principali
- `get_db_connection()`: Restituisce connessione al database

#### Versione Demo
Simulata con file JSON

#### Versione Completa
Connessione MySQL reale

## 🧪 Testing

### Test Unitari
Creare test per ogni modulo:
```python
# test_extract_data.py
def test_extract_text_digital():
    # Test con PDF digitale di esempio
    pass
```

### Test di Integrazione
Testare il flusso completo con PDF reali.

### Test di Performance
Verificare tempi di elaborazione per diversi tipi di PDF.

## 🚀 Deployment

### Requisiti di Produzione
- Server dedicato o cloud
- Database MySQL configurato
- Tesseract OCR installato
- OpenAI API key configurata

### Variabili d'Ambiente
```bash
OPENAI_API_KEY=sk-...
MYSQL_HOST=db.host.com
MYSQL_USER=brokerflow
MYSQL_PASSWORD=securepassword
MYSQL_DATABASE=brokerflow_ai
```

### Avvio del Servizio
```bash
# Avvio come servizio
nohup python main.py &

# Oppure con systemd/supervisor
```

## 🔒 Sicurezza

### Best Practice Implementate
- Nessun hardcoding di credenziali
- Validazione input
- Gestione errori senza leak di informazioni

### Da Implementare
- Crittografia dei PDF in transito
- Autenticazione per API
- Rate limiting per chiamate AI

## 📈 Monitoraggio e Logging

### Logging Attuale
Messaggi di log su console durante l'elaborazione.

### Miglioramenti Suggeriti
- Logging su file rotativo
- Integrazione con sistemi di monitoring (Prometheus, etc.)
- Alert per errori critici

## 🔄 CI/CD

### Pipeline Consigliata
1. Test automatici su ogni commit
2. Deploy automatico su staging
3. Deploy manuale su produzione

### Strumenti Consigliati
- GitHub Actions/GitLab CI
- Docker per containerizzazione
- Kubernetes per orchestrazione (per scalabilità)

## 📚 Aggiornamenti Futuri

### Roadmap Tecnica
1. **v1.1**: Supporto per compilazione PDF avanzata
2. **v1.2**: Integrazione con mailbox email
3. **v1.3**: Dashboard web per monitoraggio
4. **v1.4**: API REST per integrazioni
5. **v1.5**: Supporto multi-lingua

### Contributi Esterni
1. Forka il repository
2. Crea un branch per la tua feature
3. Apri una pull request con descrizione dettagliata

## 📞 Supporto Sviluppatori

### Community
- GitHub Issues per bug e feature request
- Wiki per documentazione collaborativa

### Contatti
- Team di sviluppo interno per modifiche critiche