import pandas as pd
import streamlit as st

from connectors.aggregator import get_all_documents

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Veille économique et financière")

# Chargement des données
try:
    all_news = get_all_documents()
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    all_news = []

df = pd.DataFrame(all_news)

# Colonnes obligatoires
required_columns = [
    "Source",
    "Titre",
    "Date",
    "Lien",
    "PDF",
]

for col in required_columns:
    if col not in df.columns:
        df[col] = ""

if df.empty:
    st.warning("Aucune donnée récupérée.")
    st.stop()

# KPI
col1, col2, col3 = st.columns(3)

col1.metric(
    "Actualités",
    len(df)
)

col2.metric(
    "Sources",
    df["Source"].nunique()
)

col3.metric(
    "Documents PDF",
    len(
        df[
            df["PDF"].astype(str).str.strip() != ""
        ]
    )
)

st.divider()

# Filtres
sources = sorted(df["Source"].dropna().unique())

selected_sources = st.multiselect(
    "Filtrer par source",
    options=sources,
    default=sources,
)

search = st.text_input(
    "Recherche"
)

df_filtered = df[
    df["Source"].isin(selected_sources)
]

if search:
    df_filtered = df_filtered[
        df_filtered["Titre"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

# Tableau
st.dataframe(
    df_filtered[
        [
            "Source",
            "Titre",
            "Date",
        ]
    ],
    width="stretch",
)

st.divider()

st.subheader("Détail des actualités")

for _, row in df_filtered.iterrows():

    titre = str(row.get("Titre", ""))
    source = str(row.get("Source", ""))
    date = str(row.get("Date", ""))
    lien = str(row.get("Lien", "")).strip()
    pdf = str(row.get("PDF", "")).strip()

    st.markdown(f"### {titre}")

    if source:
        st.write(f"**Source :** {source}")

    if date:
        st.write(f"**Date :** {date}")

    col1, col2 = st.columns(2)

    if lien:
        with col1:
            st.link_button(
                "🔗 Ouvrir la publication",
                lien,
            )

    if pdf:
        with col2:
            st.link_button(
                "📄 Télécharger PDF",
          
