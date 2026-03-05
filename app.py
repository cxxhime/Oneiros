import streamlit as st
import os
import json
from datetime import datetime
from speech_handler import transcribe_audio
from dream_agent import summarize_dream, interpret_dream
from image_generator import generate_image
from dream_journal import save_dream, load_dreams

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Oneiros — Interprète de Rêves",
    page_icon="🌙",
    layout="centered"
)

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ — THÈME ONIRIQUE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Outfit:wght@300;400;500&display=swap');

/* Fond principal */
.stApp {
    background: linear-gradient(135deg, #0a0814 0%, #0d0a1a 40%, #110e24 100%);
    background-attachment: fixed;
}

/* Étoiles en arrière-plan */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 35%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 75%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 55%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 90%, rgba(255,255,255,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* Typographie globale */
html, body, .stApp, p, div, span, label {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 300;
    color: #e8e0f0;
}

/* Titre principal */
h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.2rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.08em;
    color: #c8a97e !important;
    text-align: center;
    margin-bottom: 0.2rem !important;
}

h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 400 !important;
    color: #c8a97e !important;
    letter-spacing: 0.05em;
}

/* Sous-titre */
.subtitle {
    text-align: center;
    color: #9b92b8;
    font-size: 0.95rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Séparateur décoratif */
.divider {
    text-align: center;
    color: #c8a97e;
    font-size: 1.2rem;
    letter-spacing: 0.5em;
    margin: 1.5rem 0;
    opacity: 0.6;
}

/* Onglets */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30, 24, 53, 0.6) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(200, 169, 126, 0.15) !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.08em !important;
    color: #9b92b8 !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(200, 169, 126, 0.15) !important;
    color: #c8a97e !important;
}

/* Zone de texte */
.stTextArea textarea {
    background: rgba(17, 14, 36, 0.8) !important;
    border: 1px solid rgba(200, 169, 126, 0.25) !important;
    border-radius: 12px !important;
    color: #e8e0f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

.stTextArea textarea:focus {
    border-color: rgba(200, 169, 126, 0.6) !important;
    box-shadow: 0 0 20px rgba(200, 169, 126, 0.08) !important;
}

/* Upload fichier */
.stFileUploader {
    background: rgba(17, 14, 36, 0.8) !important;
    border: 1px dashed rgba(200, 169, 126, 0.3) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* Bouton principal */
.stButton > button {
    background: linear-gradient(135deg, rgba(200, 169, 126, 0.2), rgba(126, 106, 173, 0.2)) !important;
    border: 1px solid rgba(200, 169, 126, 0.4) !important;
    color: #c8a97e !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 2.5rem !important;
    border-radius: 50px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(200, 169, 126, 0.35), rgba(126, 106, 173, 0.35)) !important;
    border-color: rgba(200, 169, 126, 0.7) !important;
    box-shadow: 0 0 25px rgba(200, 169, 126, 0.15) !important;
    transform: translateY(-1px) !important;
}

/* Cartes de résultats */
.dream-card {
    background: rgba(17, 14, 36, 0.7);
    border: 1px solid rgba(200, 169, 126, 0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}

.dream-card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: #c8a97e;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    opacity: 0.85;
}

.dream-card-content {
    color: #c8c0d8;
    line-height: 1.8;
    font-size: 0.95rem;
}

/* Historique */
.history-card {
    background: rgba(17, 14, 36, 0.5);
    border: 1px solid rgba(126, 106, 173, 0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.8rem 0;
}

.history-date {
    font-size: 0.75rem;
    color: #7e6aad;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #c8a97e !important;
}

/* Masquer éléments Streamlit par défaut */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem !important; max-width: 780px !important;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────
st.markdown("<h1>✦ Oneiros ✦</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">✦ &nbsp; Interprète intelligent de rêves &nbsp; ✦</p>', unsafe_allow_html=True)
st.markdown('<div class="divider">· · ·</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SAISIE DU RÊVE — DEUX ONGLETS
# ─────────────────────────────────────────────
onglet_texte, onglet_audio = st.tabs(["🖊️  Décrire par écrit", "🎙️  Décrire par audio"])

texte_reve = ""

with onglet_texte:
    st.markdown("<br>", unsafe_allow_html=True)
    texte_reve = st.text_area(
        label="Décris ton rêve...",
        placeholder="Cette nuit, je me trouvais dans une forêt baignée de lumière dorée. Un renard blanc m'observait depuis les ombres...",
        height=180,
        label_visibility="collapsed"
    )

with onglet_audio:
    st.markdown("<br>", unsafe_allow_html=True)
    fichier_audio = st.audio_input(label="Enregistre ton rêve")
    if fichier_audio is not None:
        st.audio(fichier_audio)
        with st.spinner("Transcription en cours..."):
            texte_reve = transcribe_audio(fichier_audio)
        st.markdown(f"""
        <div class="dream-card">
            <div class="dream-card-title">🎙 Transcription</div>
            <div class="dream-card-content">{texte_reve}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# BOUTON D'INTERPRÉTATION
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    lancer = st.button("✦ Interpréter mon rêve ✦")


# ─────────────────────────────────────────────
# RÉSULTATS
# ─────────────────────────────────────────────
if lancer:
    if not texte_reve.strip():
        st.warning("Décris d'abord ton rêve ✦")
    else:
        st.markdown('<div class="divider">· · ·</div>', unsafe_allow_html=True)

        # 1. Résumé
        with st.spinner("Analyse du rêve en cours..."):
            resume = summarize_dream(texte_reve)
        st.markdown(f"""
        <div class="dream-card">
            <div class="dream-card-title">📖 Résumé structuré</div>
            <div class="dream-card-content">{resume}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Interprétation
        with st.spinner("Interprétation symbolique..."):
            interpretation = interpret_dream(resume)
        st.markdown(f"""
        <div class="dream-card">
            <div class="dream-card-title">🔮 Interprétation symbolique</div>
            <div class="dream-card-content">{interpretation}</div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Image
        with st.spinner("Génération de l'illustration..."):
            image_url = generate_image(interpretation)
        st.markdown('<div class="dream-card-title" style="text-align:center; margin-top:1.5rem;">🎨 Illustration du rêve</div>', unsafe_allow_html=True)
        st.image(image_url, width=700)

        # 4. Sauvegarde
        save_dream(texte_reve, resume, interpretation, "image")
        st.success("✦ Rêve sauvegardé dans ton journal ✦")


# ─────────────────────────────────────────────
# JOURNAL DES RÊVES
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="divider">· · ·</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>📖 Journal des rêves</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

try:
    journal = load_dreams()
    reves = journal.get("dreams", [])

    if not reves:
        st.markdown('<p style="text-align:center; color:#9b92b8; font-style:italic;">Aucun rêve enregistré pour le moment...</p>', unsafe_allow_html=True)
    else:
        # Affiche les rêves du plus récent au plus ancien
        for reve in reversed(reves):
            with st.expander(f"🌙 {reve.get('date', 'Date inconnue')}"):
                st.markdown(f"""
                <div class="history-card">
                    <div class="dream-card-title">Description</div>
                    <div class="dream-card-content">{reve.get('texte', '')}</div>
                </div>
                <div class="history-card">
                    <div class="dream-card-title">Résumé</div>
                    <div class="dream-card-content">{reve.get('resume', '')}</div>
                </div>
                <div class="history-card">
                    <div class="dream-card-title">Interprétation</div>
                    <div class="dream-card-content">{reve.get('interpretation', '')}</div>
                </div>
                """, unsafe_allow_html=True)
                if reve.get('image_url'):
                    st.image(reve['image_url'], width=700)
except Exception:
    st.markdown('<p style="text-align:center; color:#9b92b8; font-style:italic;">Journal non trouvé. Il sera créé après ton premier rêve ✦</p>', unsafe_allow_html=True)