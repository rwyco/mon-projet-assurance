import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import io

# 1. Configuration et Sécurité
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Erreur de configuration des secrets.")

st.set_page_config(page_title="AIP - Flux de Production", layout="wide")

# --- ÉTAPE 1 : RÉCEPTION ---
st.title("🛡️ AIP : Chaîne de Production Automatisée")
st.markdown("---")

col_upload, col_result = st.columns([1, 1])

with col_upload:
    st.subheader("📥 1. Réception & Ingestion")
    uploaded_file = st.file_uploader("Scanner un document (PNG, JPG)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with col_upload:
        st.image(img, caption="Document source reçu", use_container_width=True)

    # --- ÉTAPE 2 & 3 : TRAITEMENT & EXTRACTION ---
    if st.button("🚀 Lancer le Traitement IA"):
        with st.spinner("Analyse et extraction en cours..."):
            try:
                # Prompt structuré pour obtenir un format prévisibles
                prompt = """Analyse ce document d'assurance. 
                Extrait : Numéro de Police, Nom du Client, Montant HT. 
                Réponds strictement sous ce format :
                Police: [valeur]
                Nom: [valeur]
                Montant: [valeur]
                Signature: [Oui/Non]"""
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt, img]
                )
                
                # Simulation de structuration des données pour le tableau
                # (On transforme le texte de l'IA en dictionnaire Python)
                lines = response.text.split('\n')
                data_extracted = {}
                for line in lines:
                    if ":" in line:
                        key, val = line.split(":", 1)
                        data_extracted[key.strip()] = val.strip()

                # --- ÉTAPE 4 : VALIDATION (Human-in-the-loop) ---
                with col_result:
                    st.subheader("📊 2. Validation des données")
                    df = pd.DataFrame([data_extracted])
                    # Le tableau est éditable pour permettre la correction humaine
                    edited_df = st.data_editor(df, use_container_width=True)
                    
                    st.success("Données extraites avec succès. Veuillez vérifier avant archivage.")

                    # --- ÉTAPE 5 : ARCHIVAGE (Sortie) ---
                    st.subheader("💾 3. Archivage & Sortie")
                    
                    # Transformation du tableau en fichier Excel (en mémoire)
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        edited_df.to_excel(writer, index=False, sheet_name='Production')
                    
                    excel_data = output.getvalue()

                    st.download_button(
                        label="📥 Télécharger le Bordereau d'Injection (Excel)",
                        data=excel_data,
                        file_name=f"export_production_{data_extracted.get('Police', 'inconnue')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    if st.button("✅ Valider et Envoyer vers l'ERP"):
                        st.balloons()
                        st.toast("Données transmises au système central !")

            except Exception as e:
                st.error(f"Erreur lors du traitement : {e}")
