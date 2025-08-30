# To-Do List: Implementazione Generazione Documenti di Compliance

Questo documento elenca gli step necessari per sviluppare il modulo di generazione automatica dei documenti di compliance, sfruttando i moduli AI esistenti e i requisiti presenti in `compilance/`.

---

## Fase 1: Analisi e Setup dei Dati

L'obiettivo di questa fase è preparare il sistema a "capire" quali documenti sono necessari per ogni specifica situazione.

-   [ ] **1.1. Mappare i Documenti di Compliance:** Analizzare il `compliance_starter_kit` e creare una tabella (o un file di configurazione JSON/YAML) che mappa ogni documento (es. "Allegato 3", "Allegato 4", "Informativa Privacy") alle condizioni che ne richiedono la generazione (es. tipo di cliente 'privato' vs 'azienda', tipo di polizza, nuovo cliente vs cliente esistente).

-   [ ] **1.2. Digitalizzare i Template:** Convertire tutti i documenti di compliance dello starter kit in un formato "template" utilizzabile dal software. La scelta migliore è creare dei PDF "fillable" (con campi modulo nominati, es. `nome_cliente`, `data_sottoscrizione`) o usare template in formato `Jinja2` per generare HTML che verrà poi convertito in PDF.

-   [ ] **1.3. Estendere lo Schema del Database:** Aggiungere una tabella al `schema.sql` per tracciare i documenti di compliance generati per ogni cliente/polizza. Esempio: `CREATE TABLE generated_compliance_docs (id INT, client_id INT, policy_id INT, document_type VARCHAR(50), generation_date DATE, file_path VARCHAR(255));`.

---

## Fase 2: Sviluppo del Motore di Generazione

Questa fase si concentra sulla creazione del servizio che materialmente produce i documenti.

-   [ ] **2.1. Creare il Modulo `compliance_generator.py`:** Sviluppare un nuovo modulo in `modules/` che sarà il cuore di questa logica.

-   [ ] **2.2. Implementare la Logica Decisionale:** All'interno di `compliance_generator.py`, scrivere una funzione `decide_documents_to_generate(client_info, policy_info)` che, usando la mappa creata al punto 1.1, restituisce una lista dei documenti necessari per quella specifica transazione.

-   [ ] **2.3. Implementare il Riempimento dei Template:** Creare una funzione `fill_template(template_path, data)` che prende i dati estratti da `extract_data.py` (e altri dati di sistema come la data odierna) e li usa per compilare i template PDF (usando una libreria come `pdfrw` o `fillpdf`) o i template HTML/Jinja2.

-   [ ] **2.4. Sviluppare la Funzione Principale:** Creare una funzione `generate_all_docs(client_id, policy_id)` che orchestra il processo: chiama la logica decisionale, recupera i dati del cliente/polizza dal DB, esegue il riempimento per ogni documento necessario e salva i file generati in una cartella dedicata (es. `output/compliance/{client_id}/`).

---

## Fase 3: Integrazione e Flusso Utente

L'ultima fase consiste nell'integrare il nuovo motore nel flusso di lavoro esistente e nell'interfaccia utente.

-   [ ] **3.1. Integrare nel Flusso Principale:** Modificare `main.py` (o l'orchestratore principale) per chiamare il `compliance_generator.py` dopo la fase di preventivazione e prima della generazione dell'email finale al cliente.

-   [ ] **3.2. Aggiornare `generate_email.py`:** Modificare il modulo che genera le email per includere i nuovi documenti di compliance come allegati, insieme al preventivo. Il prompt per GPT dovrà essere aggiornato per menzionare questi documenti.

-   [ ] **3.3. Creare Interfaccia nel Frontend:** Aggiungere una sezione nel frontend Streamlit (es. nella pagina di dettaglio del cliente) dove il broker può vedere la lista dei documenti di compliance generati, scaricarli singolarmente o rigenerarli in caso di necessità.

-   [ ] **3.4. Implementare Test:** Creare degli unit test per il `compliance_generator.py` per verificare che la logica decisionale funzioni correttamente e che i documenti vengano compilati senza errori.
