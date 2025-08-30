✦ Certamente. Analizzo i tuoi appunti, il nuovo schema.sql e il
  codice esistente per darti un quadro chiaro e un piano d'azione
  dettagliato per la gestione dei documenti in ingresso.


  Prima di tutto, esamino il nuovo schema.sql e il main.py per
  capire le novità e lo stato attuale dell'import.


 ╭─────────────────────────────────────────────────────────────────╮
 │ ✔  ReadManyFiles Will attempt to read and concatenate files us… │
 │                                                                 │
 │    ### ReadManyFiles Result (Target Dir:                        │
 │    `C:\Users\hp\Documents\GitHub\broker-flow-ai`)               │
 │                                                                 │
 │    Successfully read and concatenated content from              │
 │    **2 file(s)**.                                               │
 │                                                                 │
 │    **Processed Files:**                                         │
 │    - `main.py`                                                  │
 │    - `schema.sql`                                               │
 ╰─────────────────────────────────────────────────────────────────╯
✦ -- Inserimento dei permessi di base
  INSERT INTO permissions (name, description) VALUES
  ('view_clients', 'Visualizzare la lista e i dettagli dei
  clienti'),
  ('manage_clients', 'Creare, modificare ed eliminare clienti'),
  ('view_policies', 'Visualizzare la lista e i dettagli delle
  polizze'),
  ('manage_policies', 'Creare, modificare ed eliminare polizze'),
  ('view_claims', 'Visualizzare la lista e i dettagli dei
  sinistri'),
  ('manage_claims', 'Creare, modificare ed eliminare sinistri'),
  ('view_risks', 'Visualizzare la lista e i dettagli dei rischi'),
  ('manage_risks', 'Creare, modificare ed eliminare rischi'),
  ('analyze_risks', 'Eseguire analisi di rischio e underwriting'),
  ('view_reports', 'Visualizzare i report di compliance e
  analytics'),
  ('manage_reports', 'Generare e gestire i report'),
  ('view_users', 'Visualizzare la lista degli utenti'),
  ('manage_users', 'Creare, modificare ed eliminare utenti'),
  ('manage_system_settings', 'Gestire le impostazioni di sistema');


  -- Assegnazione dei permessi ai ruoli
  -- Admin: ha tutti i permessi
  INSERT INTO role_permissions (role, permission_id) SELECT
  'admin', id FROM permissions;


  -- Broker: gestisce clienti, polizze, sinistri e rischi
  INSERT INTO role_permissions (role, permission_id) SELECT
  'broker', id FROM permissions WHERE name IN
  ('view_clients', 'manage_clients', 'view_policies',
  'manage_policies', 'view_claims', 'manage_claims', 'view_risks',
  'manage_risks');


  -- Underwriter: analizza rischi e visualizza polizze
  INSERT INTO role_permissions (role, permission_id) SELECT
  'underwriter', id FROM permissions WHERE name IN
  ('view_risks', 'analyze_risks', 'view_policies');


  -- Claims Adjuster: gestisce sinistri e visualizza polizze
  INSERT INTO role_permissions (role, permission_id) SELECT
  'claims_adjuster', id FROM permissions WHERE name IN
  ('view_claims', 'manage_claims', 'view_policies');

  -- Customer Service: visualizza clienti, polizze e sinistri
  INSERT INTO role_permissions (role, permission_id) SELECT
  'customer_service', id FROM permissions WHERE name IN
  ('view_clients', 'view_policies', 'view_claims');


  -- Viewer: solo visualizzazione
  INSERT INTO role_permissions (role, permission_id) SELECT
  'viewer', id FROM permissions WHERE name LIKE 'view_%';


  Perfetto. Ho analizzato il nuovo schema.sql e il codice di
  importazione in main.py. La tua lista di cose da fare è
  eccellente e molto pertinente. Il nuovo schema è enormemente più
  ricco e dettagliato, e il processo di import attuale è rimasto
  indietro.

  Ecco un'analisi strutturata e un piano d'azione dettagliato
  basato sui tuoi appunti e sulla mia analisi.

  Analisi della Situazione Attuale


   1. Schema del Database: Il nuovo schema.sql è di livello
      enterprise. Ha introdotto decine di nuovi campi specifici per
      clienti (dati fiscali, legali, bancari), polizze (premi,
      frequenza) e nuove tabelle come policy_subscribers e
      premium_delegates. È un salto di qualità enorme.
   2. Processo di Import (`main.py`): L'attuale funzione
      process_inbox è un prototipo. Estrae solo 4 campi base (name,
      company, email, sector) usando semplici espressioni regolari e
       li inserisce nella tabella clients. C'è un divario enorme tra
       i dati che il DB può ospitare e quelli che l'import
      attualmente gestisce.
   3. Logica di Estrazione (`extract_data.py`): La funzione
      extract_text_from_pdf è il primo passo, ma la vera
      intelligenza (attualmente in main.py con regex) è ancora
      rudimentale.

  Basandomi su questo, ecco un piano d'azione per trasformare il
  processo di import da prototipo a un motore di data entry robusto
   e intelligente.

  ---


  Piano d'Azione per il Nuovo Processo di Ingestione Documenti

  Fase 1: Potenziamento dell'Estrazione e Arricchimento Dati

   * Obiettivo: Far sì che il processo di import legga e salvi
     tutti i nuovi dati previsti dallo schema.


   * Azioni:
       1. Potenziare `extract_data.py`:
           * Trasforma la funzione extract_client_data (attualmente
             in main.py) e spostala in extract_data.py.
           * Sostituisci le regex con un prompt ingegnerizzato per
             un modello AI (GPT-4o). Il prompt dovrà chiedere al
             modello di restituire un JSON strutturato che rispecchi
              fedelmente i campi della tabella clients nel nuovo
             schema.sql (es. vat_number, fiscal_code, address,
             pec_email, etc.).
       2. Aggiornare `main.py`:
           * Modifica la funzione process_inbox per chiamare la
             nuova funzione di estrazione potenziata.
           * Riscrivi la logica di inserimento nel database per
             mappare tutti i campi del JSON estratto dall'AI alle
             rispettive colonne nelle tabelle clients, policies,
             etc.

  Fase 2: Validazione Intelligente dei Dati


   * Obiettivo: Assicurare l'integrità e la correttezza dei dati
     prima che vengano salvati, riducendo gli errori.


   * Azioni:
       1. Creare un Modulo `validators.py`: Crea un nuovo file
          modules/validators.py.
       2. Implementare Funzioni di Validazione: Dentro questo file,
          crea funzioni specifiche come:
           * validate_codice_fiscale(cf): Controlla la correttezza
             formale del codice fiscale.
           * check_codice_fiscale_consistency(cf, name, surname,
             dob, gender): Funzione più avanzata che verifica la
             coerenza tra il CF e i dati anagrafici.
           * validate_iban(iban): Controlla la correttezza formale
             dell'IBAN.
           * validate_vat_number(p_iva): Controlla la Partita IVA.
       3. Integrare la Validazione: In main.py, dopo aver ricevuto
          il JSON dall'AI (Fase 1), passa i dati estratti
          attraverso queste funzioni di validazione.

  Fase 3: Gestione delle Eccezioni e Coda di Revisione Manuale


   * Obiettivo: Creare un sistema per gestire i documenti che l'AI
     non riesce a processare o che falliscono la validazione, senza
     bloccare l'intero flusso.


   * Azioni:
       1. Modificare la Tabella `request_queue`:
           * Aggiungi una colonna status più descrittiva:
             ENUM('pending', 'processed_ok', 'needs_review',
             'failed').
           * Aggiungi una colonna review_notes (TEXT) per salvare
             il motivo della revisione (es. "Codice Fiscale non
             valido", "Dati ambigui").
       2. Aggiornare la Logica in `main.py`:
           * Se un documento viene processato e validato con
             successo, imposta lo stato a processed_ok.
           * Se un documento fallisce la validazione, imposta lo
             stato a needs_review e popola le review_notes.
       3. Creare la Pagina Frontend "Coda di Validazione":
           * Crea un nuovo file frontend/pages/validation_queue.py.
           * Questa pagina dovrà essere accessibile solo a ruoli
             specifici (es. admin, broker).
           * Visualizzerà una tabella con tutti i documenti in
             stato needs_review, mostrando il nome del file e il
             motivo dell'errore.
           * Cliccando su un elemento, l'utente potrà vedere i dati
             estratti dall'AI in una form modificabile, correggerli
             e "approvare" il documento, che verrà quindi inserito
             correttamente nel DB.

  Fase 4: Espansione a Nuovi Tipi di Documenti e Test


   * Obiettivo: Rendere il sistema capace di gestire diversi tipi
     di documenti e testarlo con dati realistici.


   * Azioni:
       1. Brainstorming e Raccolta Documenti:
           * Identifica altri documenti chiave: Fatture di
             quietanza (per tracciare i pagamenti dei premi),
             Attestati di Rischio (per le polizze auto), Moduli di
             constatazione amichevole (per i sinistri).
           * Cerca online template reali (anonimizzati) di questi
             documenti e salvali in una cartella test_documents/.
       2. Creare un Modulo `classify_document.py`:
           * Questo modulo sarà il primo a essere eseguito su un
             nuovo PDF. Il suo unico scopo è classificare il tipo
             di documento: "Richiesta Polizza", "Fattura", "ATR",
             etc.
       3. Generalizzare il Flusso: Modifica main.py in modo che,
          dopo la classificazione, invochi un flusso di estrazione e
           salvataggio specifico per quel tipo di documento. Ad
          esempio, se il documento è una "Fattura", i dati verranno
          salvati nella tabella premiums.


  Seguendo questo piano, trasformerai il semplice import attuale in
   un vero e proprio sistema di data entry intelligente, robusto e
  scalabile.