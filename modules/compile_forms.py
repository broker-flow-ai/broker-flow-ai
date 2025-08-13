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
    pdf.cell(200, 10, txt="BrokerFlow AI - Insurance Quote", ln=True, align='C')
    pdf.ln(10)
    
    # Add client information
    client_data = data.get('client_data', {})
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Client Information", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {client_data.get('name', 'Not provided')}", ln=True)
    pdf.cell(200, 10, txt=f"Company: {client_data.get('company', 'Not provided')}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {client_data.get('email', 'Not provided')}", ln=True)
    pdf.ln(10)
    
    # Add risk classification
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Risk Assessment", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Risk Type: {data.get('risk_type', 'Not classified')}", ln=True)
    pdf.ln(10)
    
    # Add filename
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Source Document: {data.get('filename', 'Unknown')}", ln=True)
    pdf.ln(5)
    
    # Add extracted text summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Document Summary:", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    # Add the extracted text (truncated to reasonable length)
    extracted_text = data.get('extracted_text', 'No text extracted')
    # Split text into lines to avoid overflow
    lines = extracted_text.split('\n')
    for line in lines[:30]:  # Limit to first 30 lines
        # Clean up line and limit length
        clean_line = line.strip()[:120]
        if clean_line:  # Only add non-empty lines
            pdf.multi_cell(0, 5, txt=clean_line)
    
    if len(lines) > 30:
        pdf.ln(5)
        pdf.cell(200, 10, txt="... (document truncated)", ln=True)
    
    # Save the PDF
    output_path = OUTPUT_PATH + output_name
    pdf.output(output_path)
    
    return output_path