import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Veille Économique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
        }
        .welcome-box {
            background-color: #F3F4F6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #2563EB;
        }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown(
    '<div class="main-header">📊 Plateforme de Veille Économique</div>',
    unsafe_allow_html=True
)

# Message d'accueil
st.markdown("""
<div class="welcome-box">
Bienvenue sur la plateforme de veille économique.

Cette application permet de consulter, analyser et suivre les actualités,
indicateurs et tendances économiques à partir des modules accessibles dans le menu latéral.
</div>
""", unsafe_allow_html=True)

st.write("")

# Colonnes d'information
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Modules disponibles",
        value="Actualités"
    )

with col2:
    st.metric(
        label="Statut",
        value="✅ Opérationnel"
    )

with col3:
    st.metric(
        label="Version",
        value="1.0"
    )

st.divider()

# Informations utilisateur
with st.expander("ℹ️ À propos de la plateforme"):
    st.write("""
    Cette plateforme centralise les informations économiques
    et fournit un accès rapide aux différents outils de suivi
    et d'analyse mis à disposition des utilisateurs.
    """)

# Barre latérale
with st.sidebar:
    st.header("Navigation")
    st.success("Utilisez le menu pour accéder aux différents modules.")
