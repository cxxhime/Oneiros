import json
from datetime import datetime

# "r" read, "w" write, "a" append

# en majuscule pour indiquer que c'est une constante qui ne doit pas être modifiée
JOURNAL_PATH = "dreams_data/journal.json"

# Sauvegarde du rêve dans le journal au format JSON
def save_dream(texte, resume, interpretation, image_url):
    # Vérifie si le fichier journal.json existe, sinon crée-le avec une structure de base
    with open(JOURNAL_PATH, "r") as fichier_lecture:
        dreams_dict = json.load(fichier_lecture)
    # Ajoute le nouveau rêve à la liste des rêves dans le dictionnaire
    dreams_dict["dreams"].append({
        "texte": texte,
        "resume": resume,
        "interpretation": interpretation,
        "image_url": "image_generee",
        "date": datetime.now().isoformat()
    })
    # Sauvegarde le dictionnaire mis à jour dans le fichier journal.json
    with open(JOURNAL_PATH, "w") as fichier_ecriture:
        json.dump(dreams_dict, fichier_ecriture, indent=4)
  
  
# Charge les rêves depuis le fichier journal.json
def load_dreams(): 
    with open(JOURNAL_PATH, "r") as journal_file:
        journal_dict = json.load(journal_file)
    return journal_dict