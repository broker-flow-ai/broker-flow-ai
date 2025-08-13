import os
import json
import re
from config import INBOX_PATH, OUTPUT_PATH
from modules.extract_data import extract_text_from_pdf
from modules.classify_risk import classify_risk
from modules.compile_forms import compile_form
from modules.generate_email import generate_email
from modules.db import get_db_connection

def extract_client_data(text):
    """Extract client data from text using regex patterns"""
    # Simple patterns for demonstration - in real implementation, you might use AI
    client_data = {
        "name": None,
        "company": None,
        "email": None
    }
    
    # Try to extract name (looking for patterns like "Sig./Signor" or "Nome:")
    name_patterns = [
        r'(?:Sig\.|Signor|Sig|Nome)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'(?:Cliente|Richiedente)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            client_data["name"] = match.group(1).strip()
            break
    
    # Try to extract company
    company_patterns = [
        r'(?:Azienda|Società|Company)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'(?:Ragione\s+Sociale)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            client_data["company"] = match.group(1).strip()
            break
    
    # Try to extract email
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    email_match = re.search(email_pattern, text)
    if email_match:
        client_data["email"] = email_match.group(0)
    
    return client_data

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

            # Classify risk
            risk = classify_risk(text)
            print(f"Risk classified as: {risk}")

            # Extract client data
            client_data = extract_client_data(text)
            print(f"Client data extracted: {client_data}")

            # Prepare form data with actual extracted information
            form_data = {
                "risk_type": risk,
                "extracted_text": text[:500],  # First 500 characters of extracted text
                "filename": filename,
                "full_text": text,
                "client_data": client_data
            }

            # Compile form with actual data
            output_name = f"compiled_{filename}"
            compiled_path = compile_form(form_data, "template.pdf", output_name)
            print(f"Form compiled at {compiled_path}")

            # Generate email
            subject, body = generate_email("Cliente", [compiled_path])
            print("Email generated.")

            # Save to DB - Complete workflow
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 1. Insert client data if not exists
            client_id = None
            if client_data["email"]:
                cursor.execute(
                    "SELECT id FROM clients WHERE email = %s", 
                    (client_data["email"],)
                )
                result = cursor.fetchone()
                if result:
                    client_id = result[0]
                else:
                    cursor.execute(
                        "INSERT INTO clients (name, company, email) VALUES (%s, %s, %s)",
                        (client_data["name"], client_data["company"], client_data["email"])
                    )
                    client_id = cursor.lastrowid
            else:
                # Insert with placeholder data if no email found
                cursor.execute(
                    "INSERT INTO clients (name, company, email) VALUES (%s, %s, %s)",
                    (client_data["name"] or "Unknown", client_data["company"] or "Unknown", "unknown@example.com")
                )
                client_id = cursor.lastrowid

            # 2. Insert risk data
            risk_details = {
                "extracted_text": text[:200],  # First 200 chars for details
                "classification_confidence": "high"  # Simplified for demo
            }
            cursor.execute(
                "INSERT INTO risks (client_id, risk_type, details) VALUES (%s, %s, %s)",
                (client_id, risk, json.dumps(risk_details))
            )
            risk_id = cursor.lastrowid

            # 3. Insert policy data
            cursor.execute(
                "INSERT INTO policies (risk_id, company, policy_pdf_path) VALUES (%s, %s, %s)",
                (risk_id, "BrokerFlow AI", compiled_path)
            )
            policy_id = cursor.lastrowid

            # 4. Update request_queue (corrected - removed risk_type column)
            cursor.execute(
                "INSERT INTO request_queue (filename, status) VALUES (%s, %s)",
                (filename, 'processed')
            )
            
            conn.commit()
            conn.close()

            print(f"Request saved to DB. Client ID: {client_id}, Risk ID: {risk_id}, Policy ID: {policy_id}")

if __name__ == "__main__":
    process_inbox()