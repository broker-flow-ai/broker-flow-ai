# Flusso di Lavoro del Broker Assicurativo: Onboarding di Nuove Polizze

Questo documento descrive il processo standard seguito da un broker assicurativo per l'acquisizione di un nuovo cliente (o una nuova polizza per un cliente esistente), distinguendo tra il segmento **Privati (Retail)** e **Business (Aziende)**. L'obiettivo è mappare ogni fase per identificare le aree di intervento e le opportunità di automazione per la piattaforma **Broker Flow AI**.

---

## Fase 1: Primo Contatto e Analisi dei Bisogni

Questa è la fase conoscitiva, dove il broker raccoglie le informazioni preliminari per definire il profilo di rischio del cliente.

#### Attività del Broker:
1.  **Primo Contatto:** Riceve una richiesta (telefono, email, form dal sito web, passaparola).
2.  **Intervista Iniziale:** Conduce un'intervista per comprendere le esigenze assicurative.
3.  **Profilazione del Rischio:** Identifica i rischi specifici da coprire.

#### Differenze (Privati vs. Business):
*   **Privati:** L'analisi si concentra su nucleo familiare, patrimonio (casa, auto), professione e salute. Le esigenze sono relativamente standard (RC Auto, Casa, Infortuni, Vita).
*   **Business:** L'analisi è molto più complessa. Richiede la comprensione del modello di business, settore di attività (es. manifatturiero, edile, IT), numero di dipendenti, fatturato, beni strumentali, rischi operativi (es. RC Professionale, D&O, Cyber Risk, Flotte aziendali). Spesso richiede l'analisi di documenti come visure camerali o bilanci.

#### Opportunità per Broker Flow AI:
*   **CRM Iniziale:** Un mini-CRM per tracciare i lead e lo stato del primo contatto.
*   **Questionari Guidati:** Creare questionari dinamici (magari via web form) che il broker può inviare al cliente per raccogliere informazioni strutturate. Il questionario si adatta se il cliente è privato o business.
*   **AI Risk Profiler (`classify_risk.py`):** Un assistente AI che, sulla base delle prime informazioni, suggerisce al broker le domande giuste da porre e le aree di rischio da approfondire, pre-classificando il cliente.

---

## Fase 2: Raccolta Dati e Quotazione

Il broker raccoglie la documentazione necessaria e interroga il mercato assicurativo per ottenere le quotazioni.

#### Attività del Broker:
1.  **Raccolta Documenti:** Richiede al cliente i documenti necessari (documento d'identità, libretto di circolazione, visura camerale, polizze precedenti).
2.  **Richiesta Quotazioni:** Invia le richieste di quotazione a più compagnie assicurative, spesso inserendo manualmente i dati sui portali B2B di ogni compagnia o inviando email standard.
3.  **Gestione Richieste:** Tiene traccia delle compagnie interrogate e delle risposte ricevute.

#### Differenze (Privati vs. Business):
*   **Privati:** Documentazione standard e processi di quotazione spesso veloci e digitalizzati.
*   **Business:** Documentazione complessa e voluminosa. Le quotazioni richiedono più tempo, interazioni con gli assuntori delle compagnie e talvolta sopralluoghi.

#### Opportunità per Broker Flow AI:
*   **Data Extraction (`extract_data.py`):** È il cuore del sistema. Estrazione automatica dei dati dai documenti forniti dal cliente (PDF, immagini) per pre-compilare le richieste di quotazione.
*   **Integrazione B2B (`b2b_integrations.py`):** Sviluppare connettori API per inviare automaticamente le richieste di quotazione ai portali delle principali compagnie assicurative, eliminando l'inserimento manuale.
*   **Dashboard Quotazioni:** Una schermata unica dove il broker vede in tempo reale lo stato delle richieste inviate ("Inviata", "In Lavorazione", "Quotazione Ricevuta") e può confrontare le offerte.

---

## Fase 3: Presentazione Offerta e Negoziazione

Il broker analizza le quotazioni ricevute, le confronta e le presenta al cliente.

#### Attività del Broker:
1.  **Analisi Comparativa:** Crea un documento o una tabella di confronto tra le varie offerte, evidenziando non solo il premio, ma anche franchigie, scoperti, massimali e clausole specifiche.
2.  **Presentazione al Cliente:** Illustra le opzioni al cliente, motivando la sua raccomandazione.
3.  **Negoziazione:** Se necessario, negozia condizioni migliori con la compagnia per conto del cliente.

#### Differenze (Privati vs. Business):
*   **Privati:** La discussione è spesso centrata su prezzo e coperture principali.
*   **Business:** La negoziazione è fondamentale e si concentra su clausole tecniche, limiti di responsabilità e personalizzazioni della polizza.

#### Opportunità per Broker Flow AI:
*   **Report Comparativo Automatico (`dashboard_analytics.py`):** Generazione automatica di un report in PDF, chiaro e personalizzato con il logo del broker, che confronta le 2-3 migliori offerte in modo standardizzato e di facile lettura per il cliente.
*   **AI Policy Analyzer:** Un modulo AI che analizza i testi delle offerte e segnala al broker clausole particolarmente vantaggiose o svantaggiose, aiutandolo nell'analisi.

---

## Fase 4: Emissione e Formalizzazione

Il cliente sceglie l'offerta e il broker finalizza il contratto.

#### Attività del Broker:
1.  **Conferma:** Comunica alla compagnia scelta la volontà di procedere.
2.  **Preparazione Documenti:** Prepara il set documentale pre-contrattuale e contrattuale.
3.  **Firma:** Fa firmare la documentazione al cliente (in ufficio o digitalmente).
4.  **Incasso Premio:** Gestisce l'incasso della prima rata del premio.
5.  **Archiviazione:** Archivia la polizza firmata e tutta la documentazione correlata.

#### Opportunità per Broker Flow AI:
*   **Form Compilation (`compile_forms.py`):** Pre-compilazione automatica di tutta la modulistica richiesta dalla compagnia (es. Modulo di Adeguatezza, Allegati 3-4).
*   **Integrazione Firma Elettronica:** Collegamento a servizi di firma elettronica (es. DocuSign, Aruba Sign) per un processo 100% digitale.
*   **Email Automation (`generate_email.py`):** Invio automatico al cliente dell'email di benvenuto con la polizza firmata e un riepilogo delle coperture.
*   **Archiviazione Intelligente:** Archiviazione automatica della polizza nel database, collegandola al cliente e impostando già la data di scadenza per il rinnovo.

---

## Fase 5: Post-Vendita e Gestione Continuativa

Il lavoro del broker non finisce con la firma, ma continua per tutta la durata del contratto.

#### Attività del Broker:
1.  **Gestione Scadenze:** Monitora le scadenze delle polizze per proporre i rinnovi.
2.  **Gestione Sinistri:** Assiste il cliente in caso di sinistro, dalla denuncia alla liquidazione.
3.  **Adeguamento Periodico:** Ricontatta periodicamente il cliente per verificare se le sue esigenze sono cambiate e se le coperture sono ancora adeguate.

#### Opportunità per Broker Flow AI:
*   **Sistema di Scadenzario Automatico:** Notifiche automatiche al broker (e/o al cliente) in prossimità della scadenza della polizza.
*   **Modulo Gestione Sinistri (`sinistri.py`):** Una sezione dedicata per tracciare lo stato di un sinistro, caricare documenti (foto, denunce) e gestire le comunicazioni con il perito e la compagnia.
*   **AI Cross-selling/Up-selling (`risk_analyzer.py`):** Il sistema può analizzare il profilo del cliente e suggerire proattivamente al broker nuove coperture. Esempio: "Il cliente ha una polizza casa e una RC Auto. Potrebbe essere interessato a una polizza Infortuni."
