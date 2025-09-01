import os
from openai import OpenAI
from typing import List, Dict

# Configura client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_invoice_fields_with_llm(words: List[str], labels: List[str]) -> Dict:
    # Componi contesto
    text_with_labels = "\n".join([f"{w} [{l}]" for w, l in zip(words, labels)])
    prompt = f"""
    Estrai i seguenti campi da questo documento:

    Campi richiesti:
    - fornitore
    - partita_iva
    - data
    - totale
    - iva

    Testo OCR con etichette:
    {text_with_labels}

    Rispondi solo in JSON, esempio:
    {{
      "fornitore": "Mario Rossi",
      "partita_iva": "01234567890",
      "data": "01/01/2025",
      "totale": "120.00",
      "iva": "22.00"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # oppure "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500
        )
        json_str = response.choices[0].message.content
        import json
        return json.loads(json_str)
    except Exception as e:
        print(f"Errore LLM: {e}")
        return {
            "fornitore": None,
            "partita_iva": None,
            "data": None,
            "totale": None,
            "iva": None
        }