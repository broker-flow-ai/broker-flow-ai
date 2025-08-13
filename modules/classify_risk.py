import openai
from config import OPENAI_API_KEY

# Inizializza il client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def classify_risk(text):
    prompt = f"""
    Classify the insurance risk in this text:
    {text}
    
    Possible categories:
    - Flotta Auto
    - RC Professionale
    - Fabbricato
    - Rischi Tecnici
    - Altro

    Respond with just the category.
    """

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=50
    )

    return response.choices[0].text.strip()