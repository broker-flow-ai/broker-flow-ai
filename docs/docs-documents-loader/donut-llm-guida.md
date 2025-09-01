Perfetto — ti do **una guida completa e passo-passo** per usare **DONUT** partendo da zero, incluso **come funziona Hugging Face**, come fare inferenza locale/Colab, e le basi per il fine-tuning. Ti spiego tutto con comandi pronti da incollare e codice Python che funziona (o quasi — qualche path andrà adattato).

Segui i passi nell’ordine: 1) capire cosa è DONUT, 2) preparare ambiente e account HF, 3) inferenza rapida, 4) parsing del risultato, 5) base per fine-tuning, 6) deployment e trucchi.

> Nota rapida: Donut è un modello **OCR-free**: prende l’immagine del documento e genera direttamente testo/JSON, quindi molto comodo per prototipi rapidi. ([Hugging Face][1])

---

# 1) Che cos’è Hugging Face e DONUT (breve)

* **Hugging Face (HF)** è il marketplace / ecosistema per modelli, dataset e librerie (`transformers`, `datasets`, `huggingface_hub`). Ti serve per scaricare modelli pre-addestrati, versionare e fare push/pull.
  (Login e token: si crea da Settings → Access Tokens). ([Hugging Face][2])

* **DONUT (Document Understanding Transformer)** è un Vision→Text encoder-decoder (encoder: Swin, decoder: BART) che **non richiede OCR**: immagine in input → JSON/testo in output. Modelli ufficiali (es. `naver-clova-ix/donut-base`) sono su Hugging Face. ([Hugging Face][3])

---

# 2) Prerequisiti (hardware/software)

* Python 3.9+ (consigliato 3.10/3.11)
* GPU (NVIDIA + CUDA) consigliata per inferenza/fine-tuning; su CPU si può provare ma va più lento.
* Account Hugging Face (per salvare modelli o scaricare modelli gated). ([Hugging Face][4])

---

# 3) Setup ambiente (locale o Colab)

## Locale (Linux/Mac/Windows WSL)

```bash
# crea venv
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# install essentials
pip install --upgrade pip
# install torch: qui scegli CPU o CUDA: https://pytorch.org/get-started/locally/
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# install HF + utils
pip install transformers datasets accelerate sentencepiece pillow huggingface_hub opencv-python
```

> Se hai GPU CUDA, installa la versione di `torch` con CUDA (vedi sito PyTorch).

## Google Colab (rapido)

* Runtime → Change runtime type → GPU
* Esegui in una cella:

```bash
!pip install transformers datasets accelerate sentencepiece pillow huggingface_hub
```

---

# 4) Autenticarsi su Hugging Face (necessario per modelli privati / push)

1. Crea account su huggingface.co → Settings → Access Tokens → New token (consiglio role `read` o `write` se vuoi pushare).
2. In terminale:

```bash
huggingface-cli login   # ti chiederà di incollare il token
# oppure in notebook:
from huggingface_hub import notebook_login
notebook_login()   # popup per incollare token
```

(Se non hai `huggingface-cli`, `pip install huggingface_hub`). ([Hugging Face][5])

---

# 5) Inferenza rapida con DONUT (script minimo)

Questo è il **primo script**: prende un’immagine e restituisce un dict Python estratto.

```python
# donut_infer.py
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch, re

# 1) Carica processor e modello (usa la checkpoint ufficiale)
MODEL = "naver-clova-ix/donut-base"   # per test, o usa fine-tuned flavors come ...-cord-v2
processor = DonutProcessor.from_pretrained(MODEL)
model = VisionEncoderDecoderModel.from_pretrained(MODEL)

# 2) device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# 3) carica immagine
image = Image.open("sample_invoice.png").convert("RGB")

# 4) prepara prompt per il task (esempio: parsing CORD)
task_prompt = "<s_cord-v2>"   # cambialo in base al fine-tuned model, o usa <s_docvqa> per Q/A
decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

# 5) pixel inputs
inputs = processor(image, return_tensors="pt").to(device)

# 6) genera
outputs = model.generate(
    inputs.pixel_values,
    decoder_input_ids=decoder_input_ids.to(device),
    max_length=512,
    pad_token_id=processor.tokenizer.pad_token_id,
    eos_token_id=processor.tokenizer.eos_token_id,
    use_cache=True,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

# 7) decode & convert to json/dict
sequence = processor.batch_decode(outputs.sequences)[0]
sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
# rimuove primo token di task e pulisce tag
sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
# utilità Donut: token2json (restituisce dict se la stringa è in formato json-like)
result = processor.token2json(sequence)

print("Parsed result:", result)
```

* Questo flusso è preso direttamente dalla documentazione e funziona con i checkpoint pre-addestrati (es. `...-cord-v2`, `...-docvqa`). ([Hugging Face][1])

---

# 6) Alternative rapida: usare `pipeline` (meno codice)

```python
from transformers import pipeline
pipe = pipeline("document-question-answering", model="naver-clova-ix/donut-base-finetuned-docvqa", device=0)
# dataset di esempio disponibile su HF per test
from datasets import load_dataset
d = load_dataset("hf-internal-testing/example-documents", split="test")
img = d[0]["image"]
print(pipe(image=img, question="What time is the coffee break?"))
```

(`pipeline` è comoda per Q/A su documenti senza dover gestire token/decoder). ([Hugging Face][1])

---

# 7) Capire l’output: parsing & post-processing

* Donut genera sequenze che contengono tag speciali; la `processor.token2json()` converte la sequenza in oggetti Python (se la sequenza è strutturata come JSON-like). Usa `result["field"]` per estrarre campi. ([Hugging Face][1])
* Se `token2json` fallisce, `sequence` è comunque una stringa che puoi pulire con regex e `json.loads()` (se è JSON valido) o usare parsing custom.

---

# 8) Fine-tuning (bozza rapida e consigli)

> Nota: il fine-tuning richiede dataset di coppie `(image, target_text)` dove `target_text` è una stringa che rappresenta l’output desiderato (per Donut spesso è `"<s_task>{\"campo\":\"valore\", ...}</s_task>"`). Molti tutorial mostrano come creare dataset sintetici o usare CORD/DocVQA per iniziare. ([Phil Schmid][6], [GitHub][7])

## Flusso sintetico per fine-tuning

1. **Preparare dataset**: immagini + target JSON stringate. Formato `.jsonl` es.:

```json
{"image_path": "images/0001.png", "text": "<s_cord-v2>{\"vendor\":\"ACME\",\"total\":\"123.45\"}</s_cord-v2>"}
```

2. **Implementare Dataset PyTorch/HF** che carichi immagine e ritorni `pixel_values` (usando `processor`) e `labels` (tokenized target).
3. **Caricare modello base**:

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")
```

4. **Trainer / accelerate**: crea `TrainingArguments` e `Trainer` (o usa `accelerate` per multi-GPU). Piccoli suggerimenti:

   * lr: 1e-5 ÷ 5e-5, batch small (2–8) per memoria GPU, num\_train\_epochs 3–10.
   * image size: mantieni coerente con quello del processor (es. 224 o 384).
   * valida frequentemente; salva checkpoint.
5. **Valutazione:** confronta stringa risultante con gold JSON (exact match, token-level F1).

Tutorial dettagliati con codice di esempio sono disponibili (es. philschmid blog / Niels Rogge notebook) e sono utilissimi per seguire passo-passo il fine-tuning. ([Phil Schmid][6], [GitHub][7])

---

# 9) Deployment e ottimizzazioni

* **Salvare / pushare** il modello su HF Hub:

```python
model.push_to_hub("tuo-username/donut-invoices")
processor.push_to_hub("tuo-username/donut-invoices")
```

(occhio al token/login). ([Hugging Face][4])

* **Quantizzazione / riduzione memoria**: HF docs mostrano approcci per quantizzazione (int4 etc.) e riduzione footprint per CPU. Se vuoi distribuire su CPU, quantizzare è quasi obbligatorio per modelli grandi. ([Hugging Face][1])

* **API**: puoi esporre inference via FastAPI che carica `processor`+`model` in memoria e risponde JSON.

---

# 10) Troubleshooting (errori comuni)

* **OOM (CUDA out of memory)** → riduci batch, riduci `image_size`, usa mixed precision (`torch.float16`) o quantizzazione.
* **`token2json` restituisce errore** → probabilmente l’output non è in formato JSON-like; stampa `sequence` raw e capisci il pattern.
* **huggingface-cli login non funziona** → prova `huggingface-cli login --token <HF_TOKEN>` oppure `notebook_login()` in notebook. Se il CLI non è trovato, `pip install huggingface_hub`. ([Hugging Face Forums][8], [Stack Overflow][9])

---

# 11) Esempio Colab “copy & run” (minimo)

In Colab, apri GPU runtime e incolla:

```bash
!pip install transformers datasets accelerate sentencepiece pillow huggingface_hub
```

Poi copia lo script di inference (vedi sezione 5). Se vuoi testare con dataset di esempio HF:

```python
from datasets import load_dataset
d = load_dataset("hf-internal-testing/example-documents", split="test")
img = d[0]["image"]
# usa pipeline or DonutProcessor+model as sopra
```

(Il notebook di esempio con Donut è pubblico su GitHub/Colab — vedi i tutorial di NielsRogge). ([Google Colab][10])

---

# 12) Risorse utili (per leggere e approfondire)

* Pagina ufficiale DONUT in Transformers (documentazione + esempi): Hugging Face Docs. ([Hugging Face][1])
* Checkpoint ufficiale: `naver-clova-ix/donut-base`. ([Hugging Face][3])
* Tutorial fine-tuning (pratico): philschmid blog + NielsRogge notebook. ([Phil Schmid][6], [GitHub][7])

---

# 13) Consiglio pratico per partire (in breve)

1. Crea account HF e token. ([Hugging Face][4])
2. In Colab / locale installa packages e prova lo script di inference (sezione 5). ([Hugging Face][1])
3. Valuta i risultati su 10–30 documenti reali: se ok, procedi a generare dataset `.jsonl` per fine-tuning; se no, guarda dove sbaglia e crea correzioni/sintetici. ([Phil Schmid][6])

---

Se vuoi, faccio subito una (scegli una):

1. Ti preparo un **notebook Colab pronto** (con tutto installato e una cella che esegue inference su un esempio) — ti do link pronto da aprire.
2. Oppure ti genero uno **script locale completo** (`donut_infer.py`) già pronto da eseguire sul tuo PC (tu mi dici se hai GPU o solo CPU).

Dimmi quale vuoi e lo preparo subito (Colab è il modo più rapido per vedere risultati senza dipendenze locali).

[1]: https://huggingface.co/docs/transformers/model_doc/donut "Donut"
[2]: https://huggingface.co/docs/hub/en/security-tokens?utm_source=chatgpt.com "User access tokens - Hugging Face"
[3]: https://huggingface.co/naver-clova-ix/donut-base?utm_source=chatgpt.com "naver-clova-ix/donut-base - Hugging Face"
[4]: https://huggingface.co/docs/huggingface_hub/en/quick-start?utm_source=chatgpt.com "Quickstart - Hugging Face"
[5]: https://huggingface.co/docs/huggingface_hub/en/guides/cli?utm_source=chatgpt.com "Command Line Interface (CLI) - Hugging Face"
[6]: https://www.philschmid.de/fine-tuning-donut?utm_source=chatgpt.com "Document AI: Fine-tuning Donut for document-parsing using ..."
[7]: https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Donut/DocVQA/Quick_inference_with_DONUT_for_DocVQA.ipynb?utm_source=chatgpt.com "Transformers-Tutorials/Donut/DocVQA ... - GitHub"
[8]: https://discuss.huggingface.co/t/cant-login-to-huggingface-cli/139741?utm_source=chatgpt.com "Can't login to Huggingface CLI - Beginners - Hugging Face Forums"
[9]: https://stackoverflow.com/questions/75773085/subprocess-runhuggingface-cli-login-token-token-works-on-mac-but?utm_source=chatgpt.com "subprocess.run([\"huggingface-cli\", \"login\", \"--token ... - Stack Overflow"
[10]: https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials/blob/master/Donut/CORD/Quick_inference_with_DONUT_for_Document_Parsing.ipynb?utm_source=chatgpt.com "Quick inference with DONUT for Document Parsing.ipynb - Colab"



# Non funziona bene



Sì Antonio, ci sono modelli già **pre-addestrati su documenti** e che funzionano bene anche con l’italiano su Hugging Face. Non devi partire da zero 🚀

Ecco alcune categorie e modelli che puoi valutare:

---

### 🔎 **Modelli OCR (solo estrazione testo)**

Se il documento è un PDF/scansione e prima di tutto serve "leggere" il testo:

* **`microsoft/trocr-base-printed`** → OCR Transformer (buono per testi stampati, multilingua).
* **`tesseract-ocr`** (già lo stai usando) → supporta l’italiano (`-l ita`).
* **`naver-clova-ix/donut-base`** → già OCR + comprensione layout (molto meglio di OCR se vuoi anche semantica).

---

### 📄 **Modelli per comprensione di layout e documenti**

Questi leggono sia testo sia struttura (tabelle, intestazioni, campi):

* **`naver-clova-ix/donut-base-finetuned-docvqa`**
  🔥 Specializzato in **Document Question Answering**, multilingua (anche italiano se il testo è OCR leggibile).

* **`microsoft/layoutlmv3-base`**
  Uno dei più usati per **estrazione di campi da fatture, scontrini, contratti**. Funziona bene anche su dataset non inglesi se fai fine-tuning.

* **`microsoft/layoutlmv2-base-uncased`**
  Simile a v3, molto usato per Information Extraction su fatture.

* **`impira/layoutlm-document-qa`**
  Addestrato per **estrarre risposte da documenti** (tipo: “Qual è la Partita IVA?” → risponde).

---

### 📑 **Modelli già fine-tuned su fatture / ricevute**

* **`naver-clova-ix/donut-base-finetuned-cord-v2`**
  Addestrato sul dataset CORD (ricevute). Funziona bene anche su fatture semplici.
* **`microsoft/layoutlmv3-finetuned-funsd`**
  Fine-tuned su FUNSD (moduli e forms), utile per documenti strutturati.

---

### ⚠️ Nota sull’italiano

La maggior parte dei modelli **non è specificamente addestrata sull’italiano**, ma funzionano perché:

* l’OCR (Tesseract o TrOCR) estrae correttamente il testo in italiano,
* il modello lavora poi sul testo + layout.

Se però vuoi qualcosa **specializzato per fatture italiane**, conviene:

1. Prendere **LayoutLMv3 o Donut**,
2. Fare **fine-tuning su un dataset di fatture italiane** (anche poche decine possono già migliorare molto).

---

👉 Domanda per capire come ti conviene muoverti:
Vuoi solo **leggere in chiaro i testi** della fattura (OCR) o vuoi anche **estrarre i campi strutturati** tipo `Partita IVA`, `Totale`, `Data` in JSON?
