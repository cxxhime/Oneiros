import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def generate_image(dream_description):
    # Nettoie et raccourcit la description pour l'API
    courte = dream_description.replace('\n', ' ').strip()[:200]
    
    # Appel à l'API Stability AI pour générer l'image
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
        headers={
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        # Configure les paramètres de génération de l'image
        json={
            "text_prompts": [{"text": f"dreamlike, surrealist, ethereal, magical, {courte}"}],
            "height": 1024,
            "width": 1024,
            "steps": 20
        }
    )
    
    # Décode l'image base64 et retourne le contenu binaire
    image_base64 = response.json()["artifacts"][0]["base64"]
    return base64.b64decode(image_base64)