from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
import json
import io
from config import TEMPLATE_PATH, OUTPUT_PATH
import os

def compile_form(data, template_name, output_name):
    # Create a new PDF with the extracted data
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="BrokerFlow AI - Report", ln=True, align='C')
    pdf.ln(10)
    
    # Add risk classification
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Risk Classification: {data.get('risk_type', 'Not classified')}", ln=True)
    pdf.ln(5)
    
    # Add filename
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"File: {data.get('filename', 'Unknown')}", ln=True)
    pdf.ln(5)
    
    # Add extracted text
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt="Extracted Text:")
    pdf.ln(5)
    
    # Add the extracted text (truncated to reasonable length)
    extracted_text = data.get('extracted_text', 'No text extracted')
    # Split text into lines to avoid overflow
    lines = extracted_text.split('\n')
    for line in lines[:20]:  # Limit to first 20 lines
        pdf.multi_cell(0, 5, txt=line[:100])  # Limit line length
    
    if len(lines) > 20:
        pdf.cell(200, 10, txt="... (text truncated)", ln=True)
    
    # Save the PDF
    output_path = OUTPUT_PATH + output_name
    pdf.output(output_path)
    
    return output_path