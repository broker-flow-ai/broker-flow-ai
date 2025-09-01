# LLM Document Loader

API per analisi di documenti tramite DONUT (OCR-free). Estrae informazioni strutturate da immagini di documenti.

## 🔐 Configurazione

Crea un file `.env` con il seguente contenuto:

```env
HF_TOKEN=hf_xxxxYYYYZZZZ...
LOG_LEVEL=INFO
HF_HOME=/root/.cache/huggingface
```

> Non committare `.env` su Git.

## 🧪 Test locale senza Docker

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export HF_TOKEN=hf_xxxx...
uvicorn app.main:app --reload
```

## 🐳 Avvio con Docker

```bash
docker compose up --build
```

Visita: http://localhost:8000/docs

## Gestione docker containers

Perfetto, vediamo passo passo come gestire lo spazio senza perdere la tua cache dei modelli.

---

### 1️⃣ Vedere tutti i container

```bash
docker ps -a
```

* Qui vedi **tutti i container**, anche quelli fermati.
* I container “vecchi” creati durante le build precedenti e mai avviati o fermati **possono essere eliminati**.
* Il container corrente con la tua app (quello che funziona) **non va eliminato** finché vuoi tenerlo.

Per eliminare un container fermo:

```bash
docker rm <container_id>
```

---

### 2️⃣ Vedere tutte le immagini

```bash
docker images
```

* Ti mostra tutte le immagini Docker presenti sul disco.
* Quelle “<none>” o vecchie versioni della tua app possono essere eliminate senza problemi.

Per eliminare un’immagine non più usata:

```bash
docker rmi <image_id>
```

---

### 3️⃣ Controllare i volumi

```bash
docker volume ls
```

* Qui vedi i volumi persistenti.
* **NON eliminare `llm-document-loader_hf_cache`**, contiene la cache dei modelli HuggingFace.
* Volumi vecchi, non collegati a nessun container, puoi eliminarli con:

```bash
docker volume prune
```

---

### 4️⃣ Pulizia veloce senza rischi

Se vuoi fare una pulizia “sicura” senza toccare la cache:

```bash
# rimuove tutti i container fermati
docker container prune

# rimuove immagini inutilizzate
docker image prune -a

# rimuove volumi non collegati a nessun container (ma lascia quelli attivi)
docker volume prune
```

> Con questo comando, il volume della tua cache HuggingFace **rimane intatto**, e recuperi spazio liberando vecchie immagini e container “incompleti”.

---

Se vuoi, posso scriverti **un comando unico che pulisce tutto tranne la cache dei modelli**, così lo fai in un colpo solo senza errori. Vuoi che lo faccia?


## Endpoint

POST `/process-document/`

Carica un file immagine (es. PNG, JPG), ricevi in risposta:

```json
{
  "document_type": "Fattura",
  "extracted_data": { ... }
}
```



# Svuota tutti gli ambienti docker

Perfetto 👍 se vuoi fare una pulizia completa di **Docker** (contenitori, immagini, volumi, network inutilizzati) e partire da zero, ti lascio una guida passo-passo. ⚠️ Occhio: questo eliminerà **tutto** quello che hai dentro Docker, quindi se hai altri progetti attivi salvali prima.

---

### 1. Stoppa e rimuovi tutti i container

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls | grep -v "bridge\|host\|none" | awk '{print $1}')
docker system prune -a --volumes -f
# rigenera
docker compose up
```

---

🔍 Dopo puoi verificare che sia davvero tutto vuoto:

```bash
docker ps -a      # nessun container
docker images -a  # nessuna immagine
docker volume ls  # nessun volume
docker network ls # solo bridge/host/none
```

---

Vuoi che ti scrivo anche uno **script unico** (tipo `clean_docker.sh`) così lo lanci e fa tutto in automatico?
