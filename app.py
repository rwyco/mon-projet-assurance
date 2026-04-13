import streamlit as st
import pandas as pd
from PIL import Image
import time

# Configuration de la page
st.set_page_config(page_title="Assurance Intelligence Processor", layout="wide")

# Style personnalisé pour l'interface
st.title("🛡️ AIP : Module de Production Intelligent")
st.markdown("---")

# Barre latérale (Sidebar) pour simuler les réglages IT
st.sidebar.header("⚙️ Paramètres du Système")
mode_test = st.sidebar.toggle("Mode Démonstration", value=True)
seuil_signature = st.sidebar.slider("Sensibilité détection signature", 0, 100, 80)

# Zone principale : Chargement du document
st.subheader("1. Ingestion du document")
uploaded_file = st.file_uploader("Glissez votre scan (Image) ou votre fichier de production (Excel)", type=['png', 'jpg', 'jpeg', 'xlsx'])

if uploaded_file is not None:
    # Simulation du temps de traitement (Nettoyage + IA)
    with st.status("Traitement en cours...", expanded=True) as status:
        st.write("🧼 Nettoyage de l'image (OpenCV)...")
        time.sleep(1)
        st.write("🔍 Extraction des données (OCR)...")
        time.sleep(1)
        st.write("🤖 Mapping intelligent des colonnes...")
        time.sleep(1)
        status.update(label="Traitement terminé !", state="complete", expanded=False)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.info("🖼️ Aperçu du document")
        if uploaded_file.name.endswith(('png', 'jpg', 'jpeg')):
            st.image(uploaded_file, use_container_width=True)
        else:
            st.write(f"📁 Fichier Excel détecté : {uploaded_file.name}")

    with col2:
        st.success("📊 Données extraites et prêtes pour validation")
        
        # Données de démonstration basées sur votre projet
        data = {
            'Champ Standard': ['Référence Police', 'Nom Assuré', 'Prime HT', 'Statut Signature'],
            'Valeur Détectée': ['POL-2026-AFRIQUE', 'Marc Durand', '1 250,00 €', '✅ Présente'],
            'Confiance IA': ['100%', '98%', '95%', '100%']
        }
        
        df_result = pd.DataFrame(data)
        
        # Affichage du tableau modifiable
        edited_df = st.data_editor(df_result, use_container_width=True)
        
        st.warning("⚠️ Vérifiez les champs surlignés en cas de doute avant validation.")
        
        if st.button("🚀 Valider et Intégrer en Base de Données"):
            st.balloons()
            st.toast("Données envoyées avec succès vers le système central !")

else:
    st.info("👋 En attente d'un document pour commencer le test.")
