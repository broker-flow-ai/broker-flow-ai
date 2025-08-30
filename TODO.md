# Todo list cose da fare 2025 08 30


## Utenti, Login e autenticazione
- [X] implementare il login 2fa con email (codice otp inviato in email) attivabile e disattivabile in .env
- [X] frontend per il logout
- [X] Rendere bloccate le pagine clienti polizze sinistri se non si è loggati e gestione delle pagine in base al ruolo dell'utente (**non funziona ancora bene**) abbiamo implementato un decoratore che si chiama require_role in utils/auth_decorator.py
- [X] frontend di creazione utenze e set privilegi per gli utenti creati se sei un admin (fatto ma da un errore di aggiornamento [anche se in realtà aggiorna])
- [ ] Pagina di modifica profilo utente (personale per utente)
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


## Problema coockie

- [] Quando si fa refresh delle pagine bisogna che rimanga loggato (ad ora si slogga e bisogna rifare login)
    - ✦ Hai assolutamente ragione. Usare i cookie è la soluzione corretta e sicura, e il problema che descrivi con Docker è un
  classico, ma risolvibile. Non è un problema della libreria in sé, ma di come la rete e i domini vengono percepiti dal
  browser quando si usano i container.


  Analizziamo la situazione per individuare il problema e trovare il workaround.

  La Causa del Problema: Il Conflitto di "Origin"


  Il cuore del problema è quasi certamente un conflitto di "Origin" (origine). Un browser, per ragioni di sicurezza, segue
  regole molto rigide: un cookie impostato da un certo dominio (es. http://localhost:8000) può essere letto solo da
  richieste provenienti da quello stesso dominio.

  Nel tuo setup Docker, probabilmente hai due servizi che, dal punto di vista del browser, sembrano due "siti" diversi:


   1. Il Frontend Streamlit: Che accedi nel browser all'indirizzo http://localhost:8501.
   2. Il Backend FastAPI: Che viene eseguito nel suo container e potrebbe essere esposto (o meno) su un'altra porta, ad esempio
      http://localhost:8000.


  Quando il tuo api_client.py (che gira insieme a Streamlit) fa una chiamata al backend, il browser la vede come una
  richiesta cross-origin (da localhost:8501 a localhost:8000). In questo scenario, i browser moderni sono estremamente
  restrittivi sulla gestione dei cookie.

  Dove si Trova il Problema (I Punti da Controllare)

  Il problema non è in un'unica riga, ma nell'interazione tra 3 componenti:


   1. La Configurazione CORS nel Backend (`api_b2b.py`):
       * Il tuo backend FastAPI deve dire esplicitamente al browser: "Mi fido delle richieste che arrivano da
         http://localhost:8501 e le autorizzo a inviarmi e ricevere cookie".
       * Punto da controllare: La configurazione del CORSMiddleware in api_b2b.py. Deve avere allow_credentials=True e
         allow_origins deve includere l'URL del frontend Streamlit.


   1     # in api_b2b.py
   2     app.add_middleware(
   3         CORSMiddleware,
   4         allow_origins=["http://localhost:8501"], # DEVE contenere l'URL del frontend
   5         allow_credentials=True, # FONDAMENTALE per i cookie
   6         allow_methods=["*"],
   7         allow_headers=["*"],
   8     )



   2. Gli Attributi del Cookie:
       * Quando il cookie viene impostato (dalla libreria streamlit-cookies-controller), potrebbe essere necessario
         specificare degli attributi per il cross-origin, in particolare SameSite='None' e Secure=True. L'attributo Secure
         richiede che il sito sia servito in HTTPS, il che rende le cose difficili in un ambiente di sviluppo locale HTTP.


   3. La Configurazione di Rete (`docker-compose.yml`):
       * La configurazione di Docker definisce come i servizi parlano tra loro e come vengono esposti all'esterno. È qui che
         si può trovare la soluzione più elegante.

  Workaround e Soluzione Definitiva

  Ecco due approcci, uno per lo sviluppo locale e uno, più robusto, per la produzione.


  Workaround 1: Configurazione CORS (Per Sviluppo Locale)


  Assicurati che la configurazione CORS in api_b2b.py sia corretta, come mostrato sopra. Questo è il primo passo
  obbligatorio. A volte questo da solo può bastare in ambienti di sviluppo, ma spesso le policy dei browser su SameSite
  bloccano comunque i cookie.

  Workaround 2: Il Reverse Proxy (La Soluzione Corretta e Definitiva)

  Questa è la soluzione standard e più robusta, che risolve il problema alla radice eliminando il conflitto di "Origin".


   * Come funziona: Invece di esporre le porte di Streamlit e FastAPI direttamente, si introduce un terzo servizio nel
     docker-compose.yml: un reverse proxy (come Nginx o Traefik).
   * Il reverse proxy diventa l'unico punto di contatto con il mondo esterno, ad esempio su http://localhost.
   * Sarà il proxy a "instradare" il traffico:
       * Le richieste per http://localhost/ vengono inviate al container di Streamlit.
       * Le richieste per http://localhost/api/... vengono inviate al container di FastAPI.
   * Perché funziona: Dal punto di vista del browser, tutte le richieste (sia al frontend che al backend) provengono dallo
     stesso dominio (http://localhost). Non c'è più un conflitto cross-origin, e i cookie funzionano in modo naturale e senza
     problemi.

  In sintesi:


  Il problema è che il browser vede frontend e backend come due siti diversi a causa delle porte differenti (8501 e 8000).
  La soluzione a breve termine è sistemare la configurazione CORS, ma potrebbe non bastare. La soluzione definitiva e
  corretta, specialmente in vista della produzione, è introdurre un reverse proxy nel tuo `docker-compose.yml` per servire
  entrambe le applicazioni sotto lo stesso dominio.