Esatto 👌 hai colto il punto.

* **OCR classico** (Tesseract & co.) → ti dà solo **testo grezzo**, senza struttura, pieno di errori, e non distingue “cos’è cosa”.
* **Donut pre-addestrato** → è addestrato su dataset generici (ricevute, moduli in inglese ecc.), quindi se lo usi così com’è **sul tuo dominio specifico** (es. fatture italiane, contratti, referti sanitari) fa risultati deludenti.
* **Donut fine-tunato** → qui diventa forte: impara il formato dei tuoi documenti e restituisce direttamente un JSON strutturato con i campi che ti interessano.

---

## 🔑 Perché Donut addestrato funziona meglio

Donut non fa solo OCR, ma **OCR + comprensione**:

* vede il documento come immagine,
* impara a riconoscere layout e contenuti,
* ti restituisce già i dati nei campi giusti.

Se gli insegni con esempi del tuo dominio, i risultati migliorano drasticamente (precisione anche >90%).

---

## 🚀 Come addestrare Donut passo passo

### 1. Preparare dataset

* Devi creare coppie: **immagine del documento** + **annotazione JSON**.
  Esempio per una fattura:

  ```json
  {
    "doc_type": "fattura",
    "fields": {
      "numero_fattura": "1234",
      "data": "2025-08-30",
      "cliente": "Mario Rossi",
      "totale": "1500.00"
    }
  }
  ```
* Le immagini possono essere scansioni o PDF convertiti in PNG/JPG.

👉 Più dati hai (anche solo 500–1000 documenti reali o simulati), meglio il modello impara.

---

### 2. Creare processor & tokenizer

```python
from transformers import DonutProcessor

# Se parti da Donut-base o small
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-small")

# Imposta il tuo "prompt" per la struttura del JSON
task_prompt = "<s_invoices>"  # tag che definisce il tipo di documento
```

---

### 3. Preparare dataset in HuggingFace `datasets`

```python
from datasets import load_dataset

# Supponiamo di avere cartelle "train" e "test"
dataset = load_dataset("imagefolder", data_dir="data/")
```

Dove ogni documento ha:

* un file immagine (`.png`)
* un file JSON associato

---

### 4. Definire modello

```python
from transformers import VisionEncoderDecoderModel

model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-small")
```

---

### 5. Allenamento (Trainer)

```python
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
    output_dir="./donut-finetuned",
    per_device_train_batch_size=1,  # se usi solo CPU
    num_train_epochs=10,
    logging_steps=50,
    save_steps=500,
    evaluation_strategy="steps",
    learning_rate=5e-5,
    predict_with_generate=True,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=processor.tokenizer,
)

trainer.train()
```

---

### 6. Uso del modello addestrato

Una volta finito:

```python
from transformers import VisionEncoderDecoderModel, DonutProcessor
from PIL import Image

processor = DonutProcessor.from_pretrained("./donut-finetuned")
model = VisionEncoderDecoderModel.from_pretrained("./donut-finetuned")

image = Image.open("fattura_test.png").convert("RGB")

inputs = processor(image, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
print(result)
```

👉 Ti restituisce direttamente il JSON strutturato che hai definito in fase di training.

---

## ⚠️ Difficoltà

* Serve dataset **annotato bene** (manuale o semi-automatico).
* Serve potenza di calcolo: su **CPU è lentissimo**, con una **GPU (anche consumer)** riesci ad addestrare in ore/giorni.
* Se hai pochi dati, rischi **overfitting** → il modello impara solo i documenti visti, ma non generalizza.

---

Vuoi che ti preparo un **mini-progetto base** (con dataset finto di 5 fatture di esempio) così vedi in pratica come parte il training e come Donut trasforma l’immagine in JSON?



Ottima domanda 👍
Questa è proprio la **differenza chiave** tra “fare inference con un modello già pronto” e **addestrarlo (fine-tuning)** sul tuo caso d’uso. Ti spiego bene:

---

## 🔹 1. Quanti documenti servono?

* **Non basta un solo documento per tipo** (anche se fosse perfetto).
  → Un modello come **Donut** ha bisogno di **diversi esempi per ogni template** (decine → centinaia) per imparare a riconoscerne la struttura e la variabilità.
* Esempio:

  * Se hai **2 tipi di fattura diversi** (es. Enel vs Fastweb), non basta 1 esempio per ognuno → servono più fatture reali o simulate di entrambi i tipi.
  * Idealmente **30-50 documenti per tipo minimo** (meglio 200+ se vuoi robustezza).

---

## 🔹 2. Perché non basta uno?

* I documenti **non sono mai identici**: cambia il font, la posizione dei campi, la qualità della scansione, piccoli rumori.
* Con un solo esempio, il modello rischia di **memorizzare l’immagine specifica** → appena incontra una piccola variazione, fallisce.
* Servono esempi diversi per permettere al modello di **generalizzare**.

---

## 🔹 3. Come si fa ad addestrare Donut

1. **Raccogli dataset** → tanti documenti per ogni tipo (meglio se vari).
2. **Annotazione JSON** → per ogni documento, devi dire al modello:

   ```json
   {
     "doc_type": "fattura",
     "metadata": {
       "numero_fattura": "12345",
       "data": "2025-08-31",
       "totale": "210.50"
     }
   }
   ```

   Questo è ciò che vuoi estrarre.
3. **Preprocessing** → trasformi ogni documento + il suo JSON in un esempio di training.
4. **Fine-tuning** → usi HuggingFace `Trainer` o script ufficiale di Donut.

   * Carichi modello base (`donut-base`)
   * Gli passi il dataset annotato
   * Lo fai allenare qualche epoca (GPU obbligatoria, meglio colab o server).
5. **Inference** → una volta addestrato, Donut legge nuovi documenti e ti restituisce direttamente il JSON strutturato.

---

## 🔹 4. Risultato che puoi aspettarti

* Con abbastanza esempi (50-200 per tipo), Donut può diventare **molto preciso** (accuracy >90% su template stabili).
* Con pochi esempi (5-10 per tipo) → funziona “così così”: può estrarre bene i campi semplici, ma sbaglia su quelli più variabili.
* Con **1 esempio solo per tipo** → praticamente inutile (il modello si overfitta e non generalizza).

---

👉 Quindi: devi considerare **un piccolo dataset per tipo di documento**.
Ti interessa che ti scriva un **piano concreto di raccolta e annotazione** (con tool consigliati per fare dataset per Donut)?


Perfetto 🚀 ottima idea: invece di aspettare documenti reali, puoi **simulare un dataset di fatture sintetiche** per addestrare Donut.
Ti preparo uno script in **Python** che:

1. Genera **5 template diversi di fattura** (cambiando layout, font e disposizione campi).
2. Per ogni template crea **50 varianti** (totale 250 fatture).
3. Salva sia il **PDF/immagine** della fattura sia il **JSON con i dati strutturati**.

---

### 📌 Script Python – Generatore di dataset sintetico fatture

Richiede:

```bash
pip install reportlab faker pillow
```

```python
import os
import random
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

fake = Faker("it_IT")

OUTPUT_DIR = "dataset_fatture"
NUM_TEMPLATES = 5
VARIANTS_PER_TEMPLATE = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_invoice_data():
    """Genera i dati fittizi di una fattura"""
    return {
        "numero_fattura": str(fake.random_int(1000, 9999)),
        "data": str(fake.date_this_decade()),
        "cliente": fake.company(),
        "piva": fake.random_number(11),
        "indirizzo": fake.address().replace("\n", " "),
        "totale": round(random.uniform(50, 2000), 2),
        "iva": "22%",
    }

def draw_template(c, data, template_id):
    """Disegna la fattura su canvas a seconda del template scelto"""
    if template_id == 1:
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 800, f"FATTURA N. {data['numero_fattura']}")
        c.setFont("Helvetica", 12)
        c.drawString(50, 780, f"Data: {data['data']}")
        c.drawString(50, 760, f"Cliente: {data['cliente']}")
        c.drawString(50, 740, f"P.IVA: {data['piva']}")
        c.drawString(50, 720, f"Indirizzo: {data['indirizzo']}")
        c.drawString(50, 700, f"Totale: € {data['totale']} (IVA {data['iva']})")

    elif template_id == 2:
        c.setFont("Courier-Bold", 14)
        c.drawString(300, 800, f"INVOICE #{data['numero_fattura']}")
        c.setFont("Courier", 11)
        c.drawString(300, 780, f"Date: {data['data']}")
        c.drawString(300, 760, f"Company: {data['cliente']}")
        c.drawString(300, 740, f"VAT: {data['piva']}")
        c.drawString(300, 720, f"Address: {data['indirizzo']}")
        c.drawString(300, 700, f"TOTAL: € {data['totale']} (VAT {data['iva']})")

    elif template_id == 3:
        c.setFont("Times-Bold", 18)
        c.drawString(200, 800, f"FATTURA COMMERCIALE")
        c.setFont("Times-Roman", 12)
        c.drawString(50, 760, f"N°: {data['numero_fattura']}   Data: {data['data']}")
        c.drawString(50, 740, f"Cliente: {data['cliente']} - PIVA: {data['piva']}")
        c.drawString(50, 720, f"Indirizzo: {data['indirizzo']}")
        c.drawString(50, 700, f"Totale da pagare: € {data['totale']}")

    elif template_id == 4:
        c.setFont("Helvetica-Oblique", 14)
        c.drawString(100, 800, f"Documento fiscale - Fattura {data['numero_fattura']}")
        c.setFont("Helvetica", 11)
        c.drawString(100, 780, f"Emessa il: {data['data']}")
        c.drawString(100, 760, f"Cliente: {data['cliente']}")
        c.drawString(100, 740, f"Partita IVA: {data['piva']}")
        c.drawString(100, 720, f"Totale imponibile: € {round(data['totale']/1.22, 2)}")
        c.drawString(100, 700, f"IVA {data['iva']} inclusa → Totale: € {data['totale']}")

    elif template_id == 5:
        c.setFont("Helvetica-Bold", 20)
        c.drawString(180, 800, f"INVOICE")
        c.setFont("Helvetica", 12)
        c.drawString(50, 760, f"Invoice N°: {data['numero_fattura']}")
        c.drawString(50, 740, f"Date: {data['data']}")
        c.drawString(50, 720, f"Customer: {data['cliente']} | VAT: {data['piva']}")
        c.drawString(50, 700, f"Address: {data['indirizzo']}")
        c.drawString(50, 680, f"TOTAL DUE: € {data['totale']}")

def generate_dataset():
    for template_id in range(1, NUM_TEMPLATES+1):
        for i in range(1, VARIANTS_PER_TEMPLATE+1):
            data = generate_invoice_data()
            
            # Nome file
            filename_pdf = os.path.join(OUTPUT_DIR, f"fattura_t{template_id}_{i}.pdf")
            filename_json = os.path.join(OUTPUT_DIR, f"fattura_t{template_id}_{i}.json")
            filename_png = filename_pdf.replace(".pdf", ".png")

            # PDF
            c = canvas.Canvas(filename_pdf, pagesize=A4)
            draw_template(c, data, template_id)
            c.save()

            # Converti in PNG (opzionale per Donut)
            with Image.open(filename_pdf) as im:
                im.save(filename_png, "PNG")

            # JSON con i dati target
            import json
            with open(filename_json, "w", encoding="utf-8") as f:
                json.dump({
                    "doc_type": "fattura",
                    "metadata": data
                }, f, ensure_ascii=False, indent=2)

            print(f"Creato {filename_pdf} + {filename_json}")

generate_dataset()
```

---

### 📌 Output

* `dataset_fatture/`

  * `fattura_t1_1.pdf`, `fattura_t1_1.png`, `fattura_t1_1.json`
  * `fattura_t1_2.pdf`, …
  * … fino a `fattura_t5_50.*`
* Ogni file ha il **PDF/PNG della fattura** + il **JSON con i dati strutturati**.

---

👉 Questo dataset puoi usarlo per addestrare **Donut**, perché avrai **immagine + ground truth JSON** per ogni documento.

Vuoi che ti scriva anche lo **script di training Donut su HuggingFace** usando questo dataset sintetico?
