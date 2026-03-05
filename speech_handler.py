from dotenv import load_dotenv
import os 
from groq import Groq

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Chargement de la clé API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Création du client Groq avec la clé API
groq_client = Groq(api_key=GROQ_API_KEY) 

# transcrire l'audio en texte
def transcribe_audio(audio_file):
    response = groq_client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3",
        language="fr"
    )
    return response.text