import google.generativeai as genai

# Configuration de l'IA avec votre clé
genai.configure(api_key="AIzaSyB-TLylVQ9xfqEGOQEBRa0-8qWf36s-7nE")
model = genai.GenerativeModel('gemini-1.5-flash')

def extraire_donnees_reelles(image_upload):
    # On convertit l'image pour l'IA
    img = Image.open(image_upload)
    
    # On envoie l'image avec une instruction précise (le "Prompt")
    prompt = """
    Analyse ce document d'assurance et extrait les informations suivantes sous forme de tableau :
    - Référence de la police
    - Nom de l'assuré
    - Montant de la prime HT
    Indique aussi si tu vois une signature manuscrite.
    """
    
    response = model.generate_content([prompt, img])
    return response.text
