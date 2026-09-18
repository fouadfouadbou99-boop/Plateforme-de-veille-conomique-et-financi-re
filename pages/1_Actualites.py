import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

# Titre
st.title("📰 Actualités")

# Données temporaires de démonstration
# À remplacer plus tard par la base SQLite

df = pd.DataFrame(
    [
        {
            "Source": "Bank Al-Maghrib",
            "Titre": "Publication du rapport annuel",
            "Catégorie": "Politique monétaire",
            "Date": "2026-09-18"
        },
        {
            "Source": "HCP",
            "Titre": "Nouvelle note de conjoncture",
            "Catégorie": "Conjoncture",
            "Date": "2026-09-17"
        },
        {
            "Source": "OCDE",
            "Titre": "Perspectives économiques mondiales",
            "Catégorie": "Économie internationale",
            "Date": "2026-09-15"
        }
    ]
)

# Filtres

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source",
        ["Toutes"] + sorted(df["Source"].unique().tolist())
    )

with col2:
    categorie = st.selectbox(
        "Catégorie",
        ["Toutes"] + sorted(df["Catégorie"].unique().tolist())
    )

# Application des filtres

df_filtre = df.copy()

if source != "Toutes":
    df_filtre = df_filtre[df_filtre["Source"] == source]

if categorie != "Toutes":
    df_filtre = df_filtre[df_filtre["Catégorie"] == categorie]

# Affichage

st.subheader("Liste des actualités")

st.dataframe(
    df_filtre,
    width="stretch"
)

# Statistiques

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nombre d'actualités",
        len(df_filtre)
    )

with col2:
    st.metric(
        "Sources",
        df_filtre["Source"].nunique()
    )

with col3:
    st.metric(
        "Catégories",
        df_filtre["Catégorie"].nunique()
    )
