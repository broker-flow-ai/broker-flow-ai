from main import extract_client_data
from modules.extract_data import extract_text_from_pdf

# Test extraction for both files
text1 = extract_text_from_pdf('inbox/sample_flotta.pdf')
text2 = extract_text_from_pdf('inbox/sample_rc_professionale.pdf')

print('Flotta:', extract_client_data(text1))
print('RC Prof:', extract_client_data(text2))