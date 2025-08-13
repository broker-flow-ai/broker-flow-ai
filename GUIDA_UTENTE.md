# BrokerFlow AI - Guida Utente

## 🎯 Obiettivo
BrokerFlow AI automatizza il processo di creazione di preventivi assicurativi per broker, riducendo il tempo di elaborazione da ore a minuti.

## 🚀 Come Iniziare

### 1. Preparazione dell'Ambiente
1. Clona il repository
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Configura le variabili d'ambiente nel file `.env`

### 2. Preparazione dei File
1. Posiziona i PDF con richieste assicurative nella cartella `inbox/`
2. Aggiungi i moduli PDF delle compagnie assicurative nella cartella `templates/`

### 3. Avvio del Sistema
- Per testare con dati reali: `python main.py`
- Per testare in modalità demo: `python main_simulated.py`

## 📥 Input del Sistema

### Tipi di PDF Supportati
1. **PDF Digitali**: File con testo selezionabile
2. **PDF Scansionati**: Immagini di documenti cartacei

### Struttura dei PDF
I PDF devono contenere informazioni chiare su:
- Dati del cliente
- Tipo di rischio
- Dettagli specifici (es. targhe per flotte, superficie per fabbricati)

## 📤 Output del Sistema

### File Generati
1. **Preventivi Compilati**: Moduli PDF compilati con i dati
2. **Email**: Testo dell'email da inviare al cliente
3. **Registrazione**: Traccia della richiesta nel database

### Cartella di Output
Tutti i file generati vengono salvati in `output/` con nomi che riflettono il file originale:
- `compiled_nomefile.pdf`: Preventivo compilato
- `email_nomefile.txt`: Email generata

## 🔧 Configurazione Avanzata

### Personalizzazione dei Template
1. Crea template PDF editabili per ogni compagnia
2. Posizionali in `templates/` con nomi significativi
3. Modifica `compile_forms.py` per gestire i campi specifici

### Aggiunta di Nuovi Tipi di Rischio
1. Aggiorna `classify_risk.py` con le nuove categorie
2. Crea template specifici per il nuovo rischio
3. Modifica `compile_forms.py` per la compilazione

## 📊 Monitoraggio e Reportistica

### Stato delle Richieste
Le richieste vengono tracciate nel database con:
- Data di ricezione
- Stato di elaborazione
- Risultati generati

### Report Disponibili
- Elenco richieste elaborate
- Tempo medio di elaborazione
- Statistiche per tipo di rischio

## 🔒 Sicurezza e Privacy

### Protezione dei Dati
- Tutti i dati sono processati localmente
- Nessun dato viene inviato a server esterni (tranne OpenAI se configurato)
- I PDF vengono eliminati dopo l'elaborazione (opzionale)

### Conformità
- I dati sono trattati in conformità con il GDPR
- I clienti possono richiedere la cancellazione dei loro dati

## 🆘 Risoluzione dei Problemi

### Problemi Comuni
1. **PDF non riconosciuti**: Verifica che il PDF contenga testo o sia un'immagine chiara
2. **Classificazione errata**: Controlla che i PDF seguano il formato atteso
3. **Template non compilati**: Verifica che i template siano PDF editabili

### Log e Debug
- I messaggi di log vengono stampati durante l'elaborazione
- Per debug avanzato, abilita il logging dettagliato nel codice

## 📈 Scalabilità

### Elaborazione in Batch
Il sistema può elaborare più PDF contemporaneamente posizionandoli tutti in `inbox/`

### Integrazione con Altri Sistemi
- Possibilità di integrazione con CRM
- API REST per integrazione con siti web
- Connessione diretta a mailbox per elaborazione automatica

## 🔄 Aggiornamenti e Manutenzione

### Aggiornamento delle Regole
- Le regole di classificazione possono essere aggiornate modificando i moduli
- I template PDF possono essere sostituiti senza modifiche al codice

### Backup e Ripristino
- I dati vengono archiviati nel database
- Esegui backup regolari del database per sicurezza

## 💡 Suggerimenti per l'Uso

1. **Standardizza i PDF in ingresso** per migliorare l'accuratezza
2. **Aggiorna regolarmente i template** con i moduli più recenti
3. **Monitora le statistiche** per identificare aree di miglioramento
4. **Forma il personale** sull'uso del sistema per massimizzare i benefici