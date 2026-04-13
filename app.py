import streamlit as st
from google import genai
from PIL import Image

# 1. Configuration sécurisée
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Erreur de configuration : {e}")

# 2. Interface Utilisateur
st.set_page_config(page_title="AIP - Production", layout="wide")
st.title("🛡️ AIP : Analyse de Production Réelle")

uploaded_file = st.file_uploader("Déposez un scan pour extraction", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Document chargé", width=400)
    
    if st.button("Lancer l'extraction intelligente"):
        with st.spinner("L'IA analyse le document..."):
            try:
                # Utilisation de la nouvelle syntaxe 2026
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=["Extrait le numéro de police, le nom et le montant de ce document.", img]
                )
                
                st.subheader("Résultat de l'analyse")
                st.info(response.text)
                st.success("Traitement terminé !")
            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
