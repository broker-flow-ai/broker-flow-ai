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
        "email": None,
        "sector": None
    }
    
    # Try to extract name with improved patterns
    # Look for "Cliente: Dr. Name Surname" pattern
    dr_match = re.search(r'Cliente:\s*(Dr\.\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text, re.IGNORECASE)
    if dr_match:
        client_data["name"] = dr_match.group(1).strip()
    else:
        # Look for "Cliente: Name Surname" pattern
        name_match = re.search(r'Cliente:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', text, re.IGNORECASE)
        if name_match:
            # Take only the first line
            name = name_match.group(1).strip()
            if "\n" in name:
                name = name.split("\n")[0]
            client_data["name"] = name
        else:
            # Fallback patterns
            sig_match = re.search(r'(?:Sig\.|Signor)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text, re.IGNORECASE)
            if sig_match:
                client_data["name"] = sig_match.group(1).strip()
    
    # Special handling for Dr. names that might have extra text
    if client_data["name"] and "\n" in client_data["name"]:
        client_data["name"] = client_data["name"].split("\n")[0].strip()
    
    # Try to extract company/studio
    # Look for "Azienda:" or "Studio:" followed by company name
    company_match = re.search(r'(?:Azienda|Studio|Societa|Company):\s*([^\n]+)', text, re.IGNORECASE)
    if company_match:
        company = company_match.group(1).strip()
        # Remove any text after phone/email patterns
        parts = re.split(r'Telefono:|Email:|Tel:|E-mail:', company)
        client_data["company"] = parts[0].strip()
    else:
        # Special handling for address pattern in flotta case
        address_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+\d+,.*\d{5})', text)
        if address_match:
            client_data["company"] = address_match.group(1).strip()
    
    # Try to extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        client_data["email"] = email_match.group(0)
    
    # Try to extract sector
    sector_match = re.search(r'Settore:\s*([^\n]+)', text, re.IGNORECASE)
    if sector_match:
        client_data["sector"] = sector_match.group(1).strip()
    
    return client_data

def process_inbox():
    try:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

        # Connect to DB to check already processed files
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get list of already processed files
        cursor.execute("SELECT filename FROM request_queue WHERE status = 'processed'")
        processed_files = set(row[0] for row in cursor.fetchall())
        
        conn.close()

        for filename in os.listdir(INBOX_PATH):
            if filename.endswith(".pdf"):
                # Skip already processed files
                if filename in processed_files:
                    print(f"Skipping {filename} - already processed")
                    continue
                    
                print(f"Processing {filename}...")
                filepath = os.path.join(INBOX_PATH, filename)
                
                # Extract text
                text = extract_text_from_pdf(filepath)
                print("Text extracted.")
                print(f"Extracted text preview: {text[:200]}...")

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
                            "INSERT INTO clients (name, company, email, sector) VALUES (%s, %s, %s, %s)",
                            (client_data["name"], client_data["company"], client_data["email"], client_data["sector"])
                        )
                        client_id = cursor.lastrowid
                else:
                    # Insert with placeholder data if no email found
                    cursor.execute(
                        "INSERT INTO clients (name, company, email, sector) VALUES (%s, %s, %s, %s)",
                        (client_data["name"] or "Unknown", client_data["company"] or "Unknown", "unknown@example.com", client_data["sector"] or "Unknown")
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
    except Exception as e:
        print(f"Error processing inbox: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        while True:
            process_inbox()
            # Wait for 30 seconds before checking for new files
            import time
            print("Waiting for new files...")
            time.sleep(30)
    except Exception as e:
        print(f"Error in main process: {str(e)}")
        import traceback
        traceback.print_exc()