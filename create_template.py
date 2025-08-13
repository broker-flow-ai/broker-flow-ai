# Dummy template PDF - just a placeholder for now
# In a real scenario, this would be a fillable PDF form from an insurance company

from fpdf import FPDF

def create_dummy_template(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    content = [
        "MODULO PREVENTIVO ASSICURATIVO",
        "",
        "CLIENTE: ___________________________",
        "AZIENDA: __________________________",
        "TIPO RISCHIO: _____________________",
        "",
        "DETTAGLIO RISCHIO:",
        "__________________________________",
        "__________________________________",
        "__________________________________",
        "",
        "COMPAGNIA: ________________________",
        "IMPORTO PREVENTIVO: _______________",
        "",
        "FIRMA: ____________________________",
        "DATA: _____________________________"
    ]
    
    for line in content:
        pdf.cell(0, 10, txt=line, ln=True)
    
    pdf.output(filename)

# Create dummy template
create_dummy_template("templates/template.pdf")
print("Dummy template created: templates/template.pdf")