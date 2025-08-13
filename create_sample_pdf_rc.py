from fpdf import FPDF

# Create a PDF with sample insurance request data for RC Professionale
def create_sample_pdf_rc_professionale(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    content = [
        "Richiesta Preventivo Assicurativo - RC Professionale",
        "",
        "Cliente: Dr. Alessandro Bianchi",
        "Professione: Medico Chirurgo",
        "Studio: Via Roma 50, 00184 Roma (RM)",
        "Telefono: 0688888888",
        "Email: dr.bianchi@studio-medico.it",
        "",
        "Dati Attivita':",
        "- Superficie Studio: 80 mq",
        "- Numero dipendenti: 3",
        "- Fatturato annuo: 250.000 EUR",
        "- Attivita': Visite mediche di base e piccole procedure ambulatoriali",
        "",
        "Note: Richiesta polizza RC Professionale con copertura media/max 500.000 EUR."
    ]
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    pdf.output(filename)

# Create sample PDF
create_sample_pdf_rc_professionale("inbox/sample_rc_professionale.pdf")
print("Sample PDF created: inbox/sample_rc_professionale.pdf")