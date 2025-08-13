import os
import json
from config import INBOX_PATH, OUTPUT_PATH
from modules.extract_data import extract_text_from_pdf
from modules.classify_risk import classify_risk
from modules.compile_forms import compile_form
from modules.generate_email import generate_email
from modules.db import get_db_connection

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

            # Compile form (example)
            output_name = f"compiled_{filename}"
            compiled_path = compile_form({}, "template.pdf", output_name)
            print(f"Form compiled at {compiled_path}")

            # Generate email
            subject, body = generate_email("Cliente", [compiled_path])
            print("Email generated.")

            # Save to DB
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO request_queue (filename, status) VALUES (%s, %s)",
                (filename, 'processed')
            )
            conn.commit()
            conn.close()

            print("Request saved to DB.")

if __name__ == "__main__":
    process_inbox()