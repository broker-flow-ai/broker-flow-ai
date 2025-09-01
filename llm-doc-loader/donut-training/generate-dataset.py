import os
import random
import json
from faker import Faker
from PIL import Image, ImageDraw, ImageFont

fake = Faker("it_IT")

OUTPUT_DIR = "dataset_fatture"
NUM_TEMPLATES = 5
VARIANTS_PER_TEMPLATE = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Usa font di sistema (su Windows di solito Arial c'è sempre)
try:
    FONT_PATH = "C:/Windows/Fonts/arial.ttf"
    base_font = ImageFont.truetype(FONT_PATH, 20)
except:
    base_font = ImageFont.load_default()

def generate_invoice_data():
    """Genera i dati fittizi di una fattura"""
    return {
        "numero_fattura": str(fake.random_int(1000, 9999)),
        "data": str(fake.date_this_decade()),
        "cliente": fake.company(),
        "piva": str(fake.random_number(11)),
        "indirizzo": fake.address().replace("\n", " "),
        "totale": round(random.uniform(50, 2000), 2),
        "iva": "22%",
    }

def draw_template(draw, data, template_id):
    """Disegna la fattura su immagine a seconda del template scelto"""
    if template_id == 1:
        draw.text((50, 50), f"FATTURA N. {data['numero_fattura']}", font=base_font, fill="black")
        draw.text((50, 100), f"Data: {data['data']}", font=base_font, fill="black")
        draw.text((50, 150), f"Cliente: {data['cliente']}", font=base_font, fill="black")
        draw.text((50, 200), f"P.IVA: {data['piva']}", font=base_font, fill="black")
        draw.text((50, 250), f"Indirizzo: {data['indirizzo']}", font=base_font, fill="black")
        draw.text((50, 300), f"Totale: € {data['totale']} (IVA {data['iva']})", font=base_font, fill="black")

    elif template_id == 2:
        draw.text((300, 50), f"INVOICE #{data['numero_fattura']}", font=base_font, fill="black")
        draw.text((300, 100), f"Date: {data['data']}", font=base_font, fill="black")
        draw.text((300, 150), f"Company: {data['cliente']}", font=base_font, fill="black")
        draw.text((300, 200), f"VAT: {data['piva']}", font=base_font, fill="black")
        draw.text((300, 250), f"Address: {data['indirizzo']}", font=base_font, fill="black")
        draw.text((300, 300), f"TOTAL: € {data['totale']} (VAT {data['iva']})", font=base_font, fill="black")

    elif template_id == 3:
        draw.text((200, 50), f"FATTURA COMMERCIALE", font=base_font, fill="black")
        draw.text((50, 100), f"N°: {data['numero_fattura']}   Data: {data['data']}", font=base_font, fill="black")
        draw.text((50, 150), f"Cliente: {data['cliente']} - PIVA: {data['piva']}", font=base_font, fill="black")
        draw.text((50, 200), f"Indirizzo: {data['indirizzo']}", font=base_font, fill="black")
        draw.text((50, 250), f"Totale da pagare: € {data['totale']}", font=base_font, fill="black")

    elif template_id == 4:
        draw.text((100, 50), f"Documento fiscale - Fattura {data['numero_fattura']}", font=base_font, fill="black")
        draw.text((100, 100), f"Emessa il: {data['data']}", font=base_font, fill="black")
        draw.text((100, 150), f"Cliente: {data['cliente']}", font=base_font, fill="black")
        draw.text((100, 200), f"Partita IVA: {data['piva']}", font=base_font, fill="black")
        draw.text((100, 250), f"Totale imponibile: € {round(data['totale']/1.22, 2)}", font=base_font, fill="black")
        draw.text((100, 300), f"IVA {data['iva']} inclusa → Totale: € {data['totale']}", font=base_font, fill="black")

    elif template_id == 5:
        draw.text((180, 50), f"INVOICE", font=base_font, fill="black")
        draw.text((50, 100), f"Invoice N°: {data['numero_fattura']}", font=base_font, fill="black")
        draw.text((50, 150), f"Date: {data['data']}", font=base_font, fill="black")
        draw.text((50, 200), f"Customer: {data['cliente']} | VAT: {data['piva']}", font=base_font, fill="black")
        draw.text((50, 250), f"Address: {data['indirizzo']}", font=base_font, fill="black")
        draw.text((50, 300), f"TOTAL DUE: € {data['totale']}", font=base_font, fill="black")

def generate_dataset():
    for template_id in range(1, NUM_TEMPLATES + 1):
        for i in range(1, VARIANTS_PER_TEMPLATE + 1):
            data = generate_invoice_data()

            # Nome file
            filename_png = os.path.join(OUTPUT_DIR, f"fattura_t{template_id}_{i}.png")
            filename_json = filename_png.replace(".png", ".json")

            # Crea immagine bianca A4 (2480x3508 px a 300dpi)
            img = Image.new("RGB", (1240, 1754), "white")
            draw = ImageDraw.Draw(img)
            draw_template(draw, data, template_id)
            img.save(filename_png, "PNG")

            # JSON con i dati target
            with open(filename_json, "w", encoding="utf-8") as f:
                json.dump({
                    "doc_type": "fattura",
                    "metadata": data
                }, f, ensure_ascii=False, indent=2)

            print(f"Creato {filename_png} + {filename_json}")

generate_dataset()
