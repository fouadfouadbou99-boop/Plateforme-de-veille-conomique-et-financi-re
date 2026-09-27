import streamlit as st
import pandas as pd

from connectors.aggregator import (
    get_all_documents
)

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title(
    "📰 Veille économique et financière"
)

try:

    data = get_all_documents()

except Exception as e:

    st.error(
        f"Erreur chargement données : {e}"
    )

    data = []

df = pd.DataFrame(data)

required_columns = [
    "Source",
    "Titre",
    "Date",
    "Lien",
    "PDF"
]

for col in required_columns:

    if col not in df.columns:
        df[col] = ""

if df.empty:

    st.warning(
        "Aucune actualité disponible."
    )

    st.stop()

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Actualités",
        len(df)
    )

with col2:

    st.metric(
        "Sources",
        df["Source"].nunique()
    )

with col3:

    st.metric(
        "PDF",
        len(
            df[
                df["PDF"]
                .astype(str)
                .str.strip() != ""
            ]
        )
    )

st.divider()

# =====================================================
# FILTRES
# =====================================================

sources = sorted(
    df["Source"]
    .fillna("")
    .unique()
)

selected_sources = st.multiselect(
    "Filtrer par source",
    sources,
    default=sources
)

search = st.text_input(
    "Recherche"
)

df_filtered = df[
    df["Source"].isin(
        selected_sources
    )
]

if search:

    df_filtered = df_filtered[
        df_filtered["Titre"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

# =====================================================
# TABLEAU
# ====================================
