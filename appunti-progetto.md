# Documento di Riferimento: Broker Flow AI

Questo documento serve come riferimento rapido per la visione, l'architettura e le componenti chiave del progetto Broker Flow AI. Sostituisce le note sparse precedenti con una struttura chiara e organizzata.

---

## 1. Visione e Obiettivo del Progetto

L'obiettivo di **Broker Flow AI** è fornire un agente AI verticale per broker assicurativi, specializzato nell'automazione dei processi di preventivazione e gestione delle polizze. La piattaforma è progettata per ridurre drasticamente il lavoro manuale, minimizzare gli errori e accelerare i tempi di risposta ai clienti.

---

## 2. Target di Mercato e Problema

*   **Cliente Ideale:** Piccoli e medi broker assicurativi (5-30 persone) che operano in settori complessi (industria, professionisti, flotte, edilizia) e gestiscono un alto volume di preventivi.
*   **Problema Risolto:** I broker ricevono richieste non standard (email, PDF), devono confrontare manualmente più compagnie, usano strumenti inefficienti (es. Excel) per i rinnovi e sono troppo lenti nel rispondere, rischiando di perdere clienti.

---

## 3. Architettura e Stack Tecnologico

La piattaforma è costruita su un'architettura a microservizi/moduli in Python, orchestrata per eseguire un flusso di lavoro specifico.

| Componente | Tecnologia Scelta |
|---|
| **Linguaggio** | Python 3.x |
| **Backend/API** | FastAPI |
| **Database** | MySQL / PostgreSQL |
| **Intelligenza Artificiale** | OpenAI API (GPT-4o) |
| **Lettura PDF (Testo)** | `PyMuPDF` (fitz), `pdfplumber` |
| **Lettura PDF (Immagine)** | OCR con `Tesseract` (`pytesseract`) |
| **Frontend** | Streamlit |
| **Deployment** | Docker, docker-compose |

---

## 4. Flusso di Lavoro Principale (Core Workflow)

Il processo automatizzato gestisce una richiesta di preventivo dall'inizio alla fine:

1.  **Ingestione:** Una richiesta (email/PDF) viene ricevuta e salvata nella directory `inbox/`.
2.  **Estrazione Dati:** Il modulo `extract_data.py` analizza il file, usa l'OCR se necessario, e con GPT-4o estrae le informazioni chiave in un formato JSON strutturato.
3.  **Classificazione Rischio:** `classify_risk.py` interpreta i dati estratti per categorizzare il tipo di rischio assicurativo (es. "Flotta Autocarri").
4.  **Matching Compagnie:** Il sistema interroga il database per trovare le compagnie adatte a coprire quel rischio specifico.
5.  **Compilazione Moduli:** `compile_forms.py` usa i template PDF delle compagnie per pre-compilare i moduli di offerta.
6.  **Generazione Comunicazione:** `generate_email.py` redige una bozza di email per il cliente, allegando i preventivi.
7.  **Tracciamento:** Le scadenze e i dati della polizza vengono salvati nel database per futuri rinnovi.

---

## 5. Struttura dei Moduli Applicativi

La struttura del progetto riflette il flusso di lavoro, con moduli dedicati per ogni responsabilità:

*   `inbox/`: Directory di input per le richieste.
*   `output/`: Directory di output per i PDF compilati.
*   `templates/`: Contiene i moduli PDF vuoti delle compagnie.
*   `extract_data.py`: Legge e interpreta i documenti di input.
*   `classify_risk.py`: Categorizza il rischio.
*   `b2b_integrations.py` (ex `match_companies.py`): Gestisce l'interazione con le compagnie.
*   `compile_forms.py`: Compila i PDF.
*   `generate_email.py`: Scrive le email per i clienti.
*   `db.py`: Gestisce la connessione e le query al database.
*   `schema.sql`: Definisce la struttura del database.
*   `main.py`: Script principale che orchestra l'intero flusso.
*   `frontend/`: Contiene l'applicazione Streamlit per l'interfaccia utente.

---

## 6. Note Tecniche e Snippet Utili

### Rilevamento PDF Immagine vs. Testo

È cruciale distinguere tra PDF scansionati (immagini) e PDF digitali (con testo selezionabile) per evitare di eseguire l'OCR inutilmente. La seguente logica può essere implementata in `extract_data.py`.

```python
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_path: str) -> str:
    """Estrae il testo da un file PDF, decidendo autonomamente se usare l'OCR."""
    try:
        # Prova a estrarre testo direttamente
        doc = fitz.open(pdf_path)
        text_content = ""
        is_text_found = False
        for page in doc:
            page_text = page.get_text().strip()
            if page_text:
                text_content += page_text + "\n"
                is_text_found = True
        
        if is_text_found:
            print(f"INFO: Estratto testo digitale da {pdf_path}")
            return text_content

        # Se non trova testo, procede con l'OCR
        print(f"WARNING: Nessun testo digitale trovato in {pdf_path}. Avvio OCR...")
        images = convert_from_path(pdf_path)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img) + "\n"
        
        return ocr_text

    except Exception as e:
        print(f"ERROR: Impossibile processare il file {pdf_path}. Errore: {e}")
        return ""

```

---

## 🔍 In sintesi

| Tipo PDF         | Metodo consigliato | Tool                       |
| ---------------- | ------------------ | -------------------------- |
| Digitale (testo) | Estrazione diretta | `PyMuPDF`, `pdfplumber`    |
| Scansionato      | OCR su immagini    | `pytesseract`, `pdf2image` |

---

Se vuoi ti genero **un modulo Python completo `extract_data.py`** che implementa questa logica, già pronto da integrare.
Vuoi che lo faccia ora?









Perfetto, iniziamo subito.
Ti preparo un progetto completo per **lanciare e vendere un agente AI per broker assicurativi specializzati**.

---

## ✅ Obiettivo

Costruire un **AI Agent verticale per broker assicurativi** che:

* Automatizza preventivi e rinnovi
* Legge richieste assicurative da email o moduli
* Compila automaticamente documenti, tabelle e risposte
* Riduce errori, tempi e lavoro umano

---

## 1️⃣ Mercato target

### 👤 Cliente ideale:

* Piccoli/medi broker assicurativi B2B o retail
* Operano in settori complessi: **industria, professionisti, flotte auto, edilizia, rischi speciali**
* Hanno team da 5 a 30 persone
* Fanno almeno 20–50 preventivi/settimana

### 🔥 Dolore comune:

* Ricevono richieste non standard (email, moduli PDF, telefonate)
* Devono confrontare 3–5 compagnie per ogni rischio
* Gestiscono rinnovi e scadenze su Excel
* Rispondono in 24–72h → troppo lenti → perdono clienti

---

## 2️⃣ Soluzione: **BrokerFlow AI**

Una rete di agenti AI (mini AGI specializzati), orchestrati in un workflow.

### 🧠 Moduli AI principali:

| Agente              | Funzione                                                            | Tool / API              |
| ------------------- | ------------------------------------------------------------------- | ----------------------- |
| `DocReader`         | Legge PDF/Email/Moduli con richiesta assicurativa                   | OpenAI GPT-4o + OCR     |
| `RischioClassifier` | Classifica il tipo di rischio (es. fabbricato, RC professionale)    | GPT-4o + logica n8n     |
| `CompagnieMatcher`  | Suggerisce 2–3 compagnie compatibili con il rischio                 | Database + regole       |
| `ModuliCompiler`    | Compila automaticamente i moduli di offerta (PDF/Excel)             | GPT-4o + FillPDF        |
| `ClientEmailWriter` | Redige la mail finale al cliente (preventivo o richiesta documenti) | GPT-4o                  |
| `RinnoviTracker`    | Tiene traccia dei rinnovi imminenti e manda reminder automatici     | Google Sheets / CRM API |
| `DashboardManager`  | Riepiloga attività settimanale (preventivi, successi, scadenze)     | Google Sheets + n8n     |

---

## 3️⃣ Esempio di flusso completo (Workflow Broker Auto-Flotte)

1. Cliente scrive via email o compila un modulo su sito
2. `DocReader` estrae:

   * Targa, tipo mezzo, km, uso, sinistri
3. `RischioClassifier` → classifica come “RC auto flotta commerciale”
4. `CompagnieMatcher` → suggerisce: Allianz, Unipol, TUA
5. `ModuliCompiler` → compila i moduli compagnia in PDF
6. `ClientEmailWriter` → genera risposta con allegati + richiesta documenti mancanti
7. `RinnoviTracker` → imposta promemoria automatico a 11 mesi
8. `DashboardManager` → aggiorna report mensile

---

## 4️⃣ Tecnologie da usare

| Componente               | Tool consigliato                                  |
| ------------------------ | ------------------------------------------------- |
| Orchestrazione           | **n8n** (Docker o cloud)                          |
| Estrazione testo         | Tesseract OCR + GPT-4o                            |
| Database clienti/rinnovi | Airtable o PostgreSQL                             |
| PDF compiler             | FillPDF, pdf-lib o Python PDF toolkit             |
| Invio mail               | Gmail API / Outlook API                           |
| Hosting AI               | OpenAI API (modello GPT-4o)                       |
| UI semplice              | Google Sheets, Telegram bot o portale web leggero |

---

## 5️⃣ Offerta commerciale

### 💰 Prezzi suggeriti

| Servizio                                              | Prezzo                     |
| ----------------------------------------------------- | -------------------------- |
| Setup iniziale (configurazione + training)            | €4.500 – €8.000 una tantum |
| Canone mensile (gestione, aggiornamenti AI, supporto) | €600 – €2.000/mese         |
| Optional: hosting su server tuo                       | +€150/mese                 |

---

## 6️⃣ Lead Generation

### 🎯 Target:

* Titolari broker
* Responsabili operation
* Consulenti assicurativi con team

### 🎁 Lead Magnet:

> “Mini AI gratuita che legge una richiesta di polizza e ti restituisce il testo pronto da copiare nella mail al cliente.”

### 🎥 Contenuti LinkedIn/YouTube:

* “Come rispondere 3 volte più in fretta a una richiesta assicurativa con l’AI”
* “Abbiamo automatizzato il lavoro di 2 impiegati in 1 script AI”
* “Ecco cosa succede quando un broker NON si dimentica mai i rinnovi”

---

## 7️⃣ Prossimi step per te

1. **Decidi il tipo di rischio su cui partire** (es. RC professionale, flotte, rischi tecnici)
2. **Costruisci un MVP funzionante con n8n + GPT-4o** (posso aiutarti a creare il diagramma completo)
3. **Trova 3 broker interessati per pilota** → offri gratis in cambio di feedback/testimonianze
4. **Lancia i contenuti e i video** con lead magnet allegato
5. **Itera + scala ad altri settori assicurativi**

---

## Vuoi che ora ti prepari:

* il diagramma di n8n completo per questo use case?
* oppure lo script LinkedIn + landing page per il lead magnet?

Dimmi da cosa vuoi partire.


Perfetto! Procediamo con lo sviluppo del **workflow backend in Python per BrokerFlow AI**, usando:

* **Python** per orchestrazione e logica
* **MySQL** come database
* **OpenAI GPT-4o** per estrazione e generazione
* **Tesseract OCR** per PDF scansionati
* **PDF libraries** (come `pdfplumber`, `fpdf`, `PyPDF2`, `pdf-lib`) per lettura e compilazione
* **Flask / FastAPI** come API layer (se ti serve esporre endpoint)

---

## 🧩 Moduli del sistema

Ti descrivo la pipeline tecnica e poi ti preparo un diagramma logico + file strutturato.

---

### 🔁 FLUSSO COMPLETO — “Preventivo Assicurazione Flotte”

#### 1. **Ingestione richiesta**

Input:

* Email in arrivo o modulo web
  Contenuto:
* PDF allegato (anagrafica + dati veicolo) oppure testo libero

→ Salvato in una directory `inbox/`
→ Riferimento inserito in MySQL (`request_queue`)

---

#### 2. **Estrazione dati**

Modulo `extract_data.py`:

* Se PDF:

  * OCR con **Tesseract** (solo se PDF immagine)
  * Parsing con `pdfplumber` o `PyMuPDF`
* Se testo:

  * Pulizia + estrazione con **OpenAI GPT-4o**

📦 Output:

```json
{
  "cliente": "Mario Rossi",
  "azienda": "Rossi Autotrasporti SRL",
  "mezzi": [
    {"targa": "AB123CD", "uso": "trasporto conto terzi", "immatricolazione": "2018", "valore": 18000}
  ],
  "rischio": "Flotta Autocarri"
}
```

---

#### 3. **Classificazione del rischio**

Modulo `classify_risk.py`:

* Prompt GPT: “Dato questo profilo, qual è la categoria assicurativa più adatta?”
* Mappa su categorie predefinite:

  * RC Professionale
  * Flotta
  * Incendio/Furto Fabbricato
  * Rischi Tecnologici

📦 Output: `"Flotta Autocarri"` → salvato in MySQL

---

#### 4. **Matching compagnie assicurative**

Modulo `match_companies.py`:

* Tabella `compagnie` in MySQL con campi:

  * `rischio_supportato`
  * `note_restrizioni`
  * `email_di_contatto`
* Output:

```json
["Allianz", "UnipolSai", "TUA Assicurazioni"]
```

---

#### 5. **Compilazione moduli PDF**

Modulo `compile_forms.py`:

* Usa template PDF statici delle compagnie (puoi usare `fpdf`, `pdf-lib`, `pdf-form-fill`)
* Compila: dati anagrafici, mezzi, massimali, ecc.
* Salva in `output/forms/{cliente}/allianz_preventivo.pdf` ecc.

---

#### 6. **Generazione email finale**

Modulo `generate_email.py`:

* Prompt GPT:

  > “Scrivi una mail professionale a un cliente per inviare il preventivo di assicurazione per la sua flotta. Allega PDF, e chiedi anche copia libretto + documento.”

📧 Output: file `.eml` o testo + subject
Opzionale: invio automatico via SMTP o Gmail API

---

#### 7. **Tracking rinnovi e scadenze**

Modulo `tracker.py`:

* Inserisce record in tabella `rinnovi`:

```sql
CREATE TABLE rinnovi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente VARCHAR(255),
    targa VARCHAR(20),
    scadenza DATE,
    compagnia VARCHAR(50),
    stato VARCHAR(20) DEFAULT 'da_rinnovare'
);
```

* Notifica automatica 30 giorni prima scadenza (via email/SMS/API)

---

#### 8. **Dashboard & API**

Modulo `api.py` (FastAPI):

* `/preventivi/` → lista richieste processate
* `/clienti/` → anagrafica
* `/rinnovi/` → riepilogo scadenze imminenti

Può alimentare una dashboard web (anche in React o solo HTML+JS).

---

## 📁 Struttura progetto consigliata

```
brokerflow_ai/
│
├── inbox/                     # richieste in arrivo
├── output/                   # PDF compilati
├── templates/                # moduli PDF per compagnie
│
├── extract_data.py
├── classify_risk.py
├── match_companies.py
├── compile_forms.py
├── generate_email.py
├── tracker.py
├── db.py                     # connessione MySQL
├── config.py
├── api.py                    # FastAPI server (opzionale)
├── run.py                    # orchestrazione principale
└── requirements.txt
```

---

## 🚀 Prossimi step

1. **Ti creo i file base Python e schema MySQL per partire**
2. **Ti preparo un esempio reale (PDF → estrazione → classificazione → output)**

Vuoi che ti generi direttamente i primi file `.py` e `schema.sql` in un archivio ZIP scaricabile?
Posso farlo subito.



Ecco la **panoramica visiva completa** del progetto **BrokerFlow AI**, sviluppato in Python con backend MySQL:

---

## 🧠 **BrokerFlow AI – Architettura Modulare**

### 🔹 **FASE 1 – Input**

📥 **Email o PDF** con la richiesta assicurativa del cliente
→ Viene salvata e registrata nella tabella `request_queue`

---

### 🔹 **FASE 2 – Estrazione & Comprensione**

* 📄 `extract_data.py`: estrae il testo dal PDF (OCR se serve)
* 🤖 `GPT-4o`: interpreta e trasforma il testo in JSON strutturato

---

### 🔹 **FASE 3 – Automazione Decisionale**

* 🧠 `classify_risk.py`: classifica il rischio assicurativo (es. flotta, fabbricato, RC)
* 🏢 `match_companies.py`: seleziona 2–3 compagnie compatibili
* 📄 `compile_forms.py`: compila automaticamente i moduli PDF richiesti

---

### 🔹 **FASE 4 – Output & Automazione**

* ✉️ `generate_email.py`: genera una mail completa da inviare al cliente
* ⏳ `tracker.py`: salva scadenze e rinnovi in MySQL
* 📊 `api.py`: espone una dashboard per controllo attività e stato delle pratiche

---

## 📦 Output del Sistema:

* Preventivo PDF compilato
* Email automatica pronta o inviata
* Scadenze aggiornate
* Dashboard con KPIs assicurativi

---

Se vuoi, ora ti posso creare un archivio ZIP con:

* La struttura base dei file `.py`
* Lo schema MySQL `schema.sql`
* Un esempio di input PDF + output JSON

Ti preparo il progetto?



## Gestione pdf immagine e non

Se il PDF **non è un'immagine**, ovvero è un PDF **digitale con testo selezionabile**, non hai bisogno di OCR. In quel caso:

---

## ✅ Strategie quando il PDF contiene testo selezionabile

Puoi usare direttamente una delle seguenti librerie Python per **estrarre testo strutturato** in modo preciso:

### 🔹 `pdfplumber` (più preciso con layout strutturati)

```python
import pdfplumber

with pdfplumber.open("richiesta_preventivo.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
print(text)
```

### 🔹 `PyMuPDF` (fitz) — più veloce e robusto

```python
import fitz  # PyMuPDF

doc = fitz.open("richiesta_preventivo.pdf")
text = ""
for page in doc:
    text += page.get_text()
print(text)
```

---

## 🔄 Poi cosa fai col testo?

1. **Pre-processing** (opzionale):

   * Pulizia da numeri di pagina, intestazioni/footers
   * Rimozione caratteri speciali (`\n`, `\t`, ecc.)

2. **Prompt al modello GPT-4o**:

   * Gli passi direttamente il testo per estrarre entità (cliente, targa, valore veicolo, ecc.)
   * Prompt tipo:

     ```
     Estrai i seguenti dati dal testo: nome del cliente, azienda, numero di mezzi, targa, uso, anno immatricolazione e valore veicolo. Rispondi in JSON.
     Testo:
     [TESTO DEL PDF]
     ```

---

## 🔁 Flusso decisionale (dentro `extract_data.py`)

```python
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def is_pdf_scanned(path):
    reader = PdfReader(path)
    for page in reader.pages:
        if '/Font' in page['/Resources']:
            return False  # Ha font = è testo digitale
    return True  # Probabile immagine

def extract_text_from_pdf(path):
    if is_pdf_scanned(path):
        print("OCR in corso...")
        return ocr_pdf(path)
    else:
        print("PDF digitale rilevato, estraggo testo...")
        return extract_text_digital(path)

def extract_text_digital(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def ocr_pdf(path):
    # Converti in immagini e OCR con pytesseract
    from pdf2image import convert_from_path
    pages = convert_from_path(path)
    text = ""
    for image in pages:
        text += pytesseract.image_to_string(image)
    return text
```

---

## 🔍 In sintesi

| Tipo PDF         | Metodo consigliato | Tool                       |
| ---------------- | ------------------ | -------------------------- |
| Digitale (testo) | Estrazione diretta | `PyMuPDF`, `pdfplumber`    |
| Scansionato      | OCR su immagini    | `pytesseract`, `pdf2image` |

---

Se vuoi ti genero **un modulo Python completo `extract_data.py`** che implementa questa logica, già pronto da integrare.
Vuoi che lo faccia ora?
