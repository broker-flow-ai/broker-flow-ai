import os
import json
from config import INBOX_PATH, OUTPUT_PATH
from modules.extract_data import extract_text_from_pdf

# Dummy modules to simulate OpenAI and DB
def classify_risk_dummy(text):
    # Simple heuristic to classify risk based on keywords
    if "flotta" in text.lower() or "autocarro" in text.lower():
        return "Flotta Auto"
    elif "rc professionale" in text.lower() or "medico" in text.lower():
        return "RC Professionale"
    elif "fabbricato" in text.lower() or "studio" in text.lower():
        return "Fabbricato"
    else:
        return "Altro"

def compile_form_dummy(data, template_name, output_name):
    # For now, just create a dummy compiled PDF
    from fpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    content = [
        "PREVENTIVO ASSICURATIVO - COMPILATO DA BROKERFLOW AI",
        "",
        f"CLIENTE: {data.get('cliente', 'N/A')}",
        f"AZIENDA: {data.get('azienda', 'N/A')}",
        f"TIPO RISCHIO: {data.get('rischio', 'N/A')}",
        "",
        "DETTAGLIO RISCHIO:",
    ]
    
    # Add extracted details
    if 'dettagli' in data:
        for detail in data['dettagli']:
            content.append(f"- {detail}")
    
    content.extend([
        "",
        "COMPAGNIA: Allianz",
        "IMPORTO PREVENTIVO: 1.250 EUR",
        "",
        "FIRMA: ____________________________",
        "DATA: _____________________________"
    ])
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    output_path = os.path.join(OUTPUT_PATH, output_name)
    pdf.output(output_path)
    
    return output_path

def generate_email_dummy(client_name, policy_paths):
    subject = "Il tuo preventivo assicurativo"
    body = f"""
    Gentile {client_name},

    in allegato trova il preventivo richiesto.

    Per qualsiasi dubbio, siamo a disposizione.

    Cordiali saluti,
    BrokerFlow AI
    """
    return subject, body

def save_request_dummy(filename, status):
    # Simulate saving to DB with a JSON file
    db_file = "request_queue.json"
    
    # Load existing data
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            data = json.load(f)
    else:
        data = []
    
    # Add new request
    data.append({
        "filename": filename,
        "status": status,
        "timestamp": str(__import__('datetime').datetime.now())
    })
    
    # Save updated data
    with open(db_file, 'w') as f:
        json.dump(data, f, indent=2)

def process_inbox():
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    for filename in os.listdir(INBOX_PATH):
        if filename.endswith(".pdf"):
            print(f"Processing {filename}...")
            filepath = os.path.join(INBOX_PATH, filename)
            
            # Extract text
            text = extract_text_from_pdf(filepath)
            print("Text extracted.")
            
            # Extract basic data (simplified)
            lines = text.split('\n')
            data = {
                "cliente": "N/A",
                "azienda": "N/A",
                "rischio": "N/A",
                "dettagli": []
            }
            
            for line in lines:
                if line.startswith("Cliente:"):
                    data["cliente"] = line.split(":", 1)[1].strip()
                elif line.startswith("Azienda:"):
                    data["azienda"] = line.split(":", 1)[1].strip()
                elif line.startswith("Dettaglio") or line.startswith("- Targa") or line.startswith("- Superficie"):
                    data["dettagli"].append(line.strip())
            
            # Classify risk
            risk = classify_risk_dummy(text)
            data["rischio"] = risk
            print(f"Risk classified as: {risk}")

            # Compile form (example)
            output_name = f"compiled_{filename}"
            compiled_path = compile_form_dummy(data, "template.pdf", output_name)
            print(f"Form compiled at {compiled_path}")

            # Generate email
            subject, body = generate_email_dummy(data["cliente"], [compiled_path])
            print("Email generated.")
            
            # Save email to file
            email_path = os.path.join(OUTPUT_PATH, f"email_{filename.replace('.pdf', '.txt')}")
            with open(email_path, 'w') as f:
                f.write(f"Subject: {subject}\n\n{body}")
            print(f"Email saved to {email_path}")

            # Save to DB (simulated)
            save_request_dummy(filename, 'processed')
            print("Request saved to DB.")

if __name__ == "__main__":
    process_inbox()