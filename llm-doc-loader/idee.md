# Progetto a 2 layer ocr+llm


Esatto ✅ è proprio il modo giusto di approcciarlo.
Se cerchi di fare **OCR + interpretazione in un solo passaggio**, rischi di perdere dati o di avere confusione. Molto meglio **separare i layer**:

---

## 🔹 Architettura a due layer

1. **Layer 1 – OCR puro (estrazione testo grezzo)**

   * Qui usi un motore OCR (Tesseract, EasyOCR, PaddleOCR o Donut in modalità “ocr-only”).
   * Output = testo completo del documento, senza interpretazione.
   * Lo salvi in un JSON con:

     ```json
     {
       "raw_text": "Testo completo della fattura ...",
       "pages": [
         {"page": 1, "text": "contenuto pagina 1"},
         {"page": 2, "text": "contenuto pagina 2"}
       ]
     }
     ```

2. **Layer 2 – Interpretazione / Parsing**

   * Qui prendi il `raw_text` e lo passi a un modello linguistico (Hugging Face o OpenAI).
   * Usi un **prompt o un parser strutturato** per dire al modello cosa estrarre:

     * intestatario
     * partita IVA
     * indirizzo
     * numero fattura
     * data
     * imponibile
     * IVA
     * totale
   * Output = JSON strutturato con i metadati.

---

## 🔹 Vantaggi

* Se l’OCR migliora, non devi ritoccare la logica di parsing.
* Puoi cambiare modello di NLP senza toccare la parte di OCR.
* Puoi anche salvare i **raw\_text** per debug e ri-analisi.
* Più trasparenza → puoi confrontare cosa ha letto l’OCR e cosa ha interpretato il modello.

---

## 🔹 Tecnologie possibili

* **Layer 1 (OCR)**:

  * `pytesseract` (base, leggero)
  * `paddleocr` (più robusto anche per italiano, supporta layout)
  * `donut` in modalità OCR
* **Layer 2 (Interpretazione)**:

  * Hugging Face `bert-base-multilingual-cased` + fine-tuning NER (Named Entity Recognition)
  * Oppure direttamente **OpenAI GPT con uno schema JSON** (zero-shot)

---

👉 Vuoi che ti scriva uno **scheletro di pipeline** in Python (OCR → salvataggio testo → interpretazione → JSON finale) così vedi subito come collegare i due layer?
