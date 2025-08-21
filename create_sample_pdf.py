from fpdf import FPDF

# Create a PDF with sample insurance request data
def create_sample_pdf_flotta(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Replace Euro symbol with "EUR" to avoid encoding issues
    content = [
        "Richiesta Preventivo Assicurativo - Flotta Auto",
        "",
        "Cliente: Mario Rossi",
        "Azienda: Rossi Trasporti SRL",
        "Settore: Trasporti",
        "Indirizzo: Via Milano 10, 20100 Milano (MI)",
        "Telefono: 0212345678",
        "Email: mario@rossitrasporti.it",
        "",
        "Dettaglio Veicoli:",
        "- Targa: AB123CD, Tipo: Autocarro, Uso: Trasporto merci, Anno: 2018, Valore: 18.000 EUR",
        "- Targa: EF456GH, Tipo: Autocarro, Uso: Trasporto merci, Anno: 2020, Valore: 22.000 EUR",
        "- Targa: IJ789KL, Tipo: Autocarro, Uso: Trasporto merci, Anno: 2019, Valore: 20.000 EUR",
        "",
        "Note: Richiesta polizza RC Auto per flotta commerciale con copertura furto/incendio."
    ]
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    pdf.output(filename)

# Create sample PDF
create_sample_pdf_flotta("inbox/sample_flotta.pdf")
print("Sample PDF created: inbox/sample_flotta.pdf")