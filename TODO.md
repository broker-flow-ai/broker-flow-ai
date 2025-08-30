# Todo list cose da fare 2025 08 30


## Utenti, Login e autenticazione
- implementare il login 2fa con email (codice otp inviato in email) attivabile e disattivabile in .env
- frontend per il logout
- frontend di creazione utenze e set privilegi se sei admin
- Pagina di modifica profilo utente
    - implementare il recupero password con email
    - implementare la modifica della password con email


## Inbox pdf Documenti caricati

- verificare se funziona ancora l'import
- arricchire con i nuovi dati che ha il DB l'import
- capire quali tipi di documenti differenti potremmo caricare (polizze, fatture, contratti, o altro non so) e quindi popolare i giusti dati su DB
- cercare template di documenti reali cosi da testare realmente
- gestire contolli tra Codice Fiscale e dati inseriti (nome cognome data nascita ecc) e implementare una validazione codice fiscale e validazione altri campi sensibili come iban
- creare una parte di frontend in cui vengono elencati i documenti caricati che hanno bisogno di gestione manuale (es. incogruenza codice fiscale, campi inseriti o letti ambigui)


## Elaborazioni AI

- guardare il file in compilance/COMPILANCE_DOCUMENT_GENERATION_TODO.md


## Menu frontend

- riorganizzarlo completamente perchè è caotico poco comprensibile e parti spariscono quando si va in alcune pagine