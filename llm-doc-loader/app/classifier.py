def classify_document(json_result: dict) -> str:
    text = str(json_result).lower()
    if "invoice" in text or "total" in text or "amount" in text or "bill" in text or "price" in text:
        return "Fattura"
    elif "id" in text or "identity" in text or "nome" in text or "surname" in text or "date of birth" in text:
        return "Documento d'identit\u00e0"
    else:
        return "Altro"