# Todo list cose da fare 2025 08 30


## Utenti, Login e autenticazione
- [X] implementare il login 2fa con email (codice otp inviato in email) attivabile e disattivabile in .env
- [X] frontend per il logout
- [] Quando si fa refresh delle pagine bisogna che rimanga loggato (ad ora si slogga e bisogna rifare login)
- [X] Rendere bloccate le pagine clienti polizze sinistri se non si è loggati e gestione delle pagine in base al ruolo dell'utente (**non funziona ancora bene**) abbiamo implementato un decoratore che si chiama require_role in utils/auth_decorator.py
- [X] frontend di creazione utenze e set privilegi per gli utenti creati se sei un admin (fatto ma da un errore di aggiornamento [anche se in realtà aggiorna])
- Pagina di modifica profilo utente (personale per utente)
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

-  Analisi Rischio Avanzata non funziona (errore nell'endpoin Errore nella chiamata API: 404 Client Error: Not Found for url: http://api:8000/api/v1/insurance/risk-analysis)
    - Siccome è per compagnia nel frontend migliorare la selezione al posto di compagnia id va creato un filtro adeguato
- Compilance non scarica il file dice file non trovato ma in realtà c'è perchè la mail la invia con allegato un file
- guardare il file in compilance/COMPILANCE_DOCUMENT_GENERATION_TODO.md


## Menu frontend

- riorganizzarlo completamente perchè è caotico poco comprensibile e parti spariscono quando si va in alcune pagine



## Pulizia da file obsoleti

- tutti i vecchi file di import DB o altro deve essere eliminato perchè inutile e sporca il progetto