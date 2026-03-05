from dotenv import load_dotenv
import os 
from groq import Groq

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Chargement de la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Création du client Groq avec la clé API
groq_client = Groq(api_key=GROQ_API_KEY)

# Résumé structuré du rêve
def summarize_dream(dream_description):
    prompt = f"Voici la description du rêve : {dream_description}"
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en interprétation des rêves. Résume les rêves de manière structurée, en mettant en évidence les éléments clés, les émotions ressenties et les symboles présents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# Interprétation du rêve
def interpret_dream(dream_description):
    prompt = f"Voici la description du rêve : {dream_description}"
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You turn French dream interpretations into a concise English prompt for Stable Diffusion XL. Output only the prompt, no explanations."},
            {"role": "user", "content": prompt}
        ],
        temperature= 1.0,
    )
    return response.choices[0].message.content