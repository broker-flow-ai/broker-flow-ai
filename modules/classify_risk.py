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

    Respond with just the category name, nothing else.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an insurance expert that classifies insurance risks. Respond only with the category name, nothing else."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.1
    )

    # Estrai solo la categoria e rimuovi testo extra
    category = response.choices[0].message.content.strip()
    
    # Rimuovi eventuali frasi come "The category is" o "The insurance risk is"
    if "Flotta Auto" in category:
        return "Flotta Auto"
    elif "RC Professionale" in category:
        return "RC Professionale"
    elif "Fabbricato" in category:
        return "Fabbricato"
    elif "Rischi Tecnici" in category:
        return "Rischi Tecnici"
    else:
        return "Altro"