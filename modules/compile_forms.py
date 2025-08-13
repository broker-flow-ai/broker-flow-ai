from PyPDF2 import PdfReader, PdfWriter
import json
import io
from config import TEMPLATE_PATH, OUTPUT_PATH

def compile_form(data, template_name, output_name):
    template_path = TEMPLATE_PATH + template_name
    output_path = OUTPUT_PATH + output_name

    reader = PdfReader(template_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # TODO: Fill form fields with data (requires editable PDF)
    # This is a simplified version - real implementation depends on PDF structure

    with open(output_path, 'wb') as out_file:
        writer.write(out_file)

    return output_path