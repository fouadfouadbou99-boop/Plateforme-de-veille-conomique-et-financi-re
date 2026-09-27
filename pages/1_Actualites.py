import streamlit as st
import pandas as pd

from connectors.aggregator import (
    get_all_documents
)

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title(
    "📰 Veille économique et financière"
)

# =====================================================
# CHARGEMENT DES DONNÉES
# =====================================================

try:

    data = get_all_documents()

except Exception as e:

    st.error(
        f"Erreur chargement données : {e}"
    )

    data = []

df = pd.DataFrame(data)

# =====================================================
# STRUCTURE MINIMALE
# =====================================================

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

# =====================================================
# AUCUNE DONNÉE
# =====================================================

if df.empty:

    st.warning(
        "Aucune actualité disponible."
    )

    st.stop()

# =====================================================
# SUPPRESSION DES DOUBLONS
# =====================================================

if "Titre" in df.columns:

    df = df.drop_duplicates(
        subset=["Titre"]
    )

# =====================================================
# TRI PAR DATE
# =====================================================

try:

    df["Date_tmp"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df = df.sort_values(
        by="Date_tmp",
        ascending=False
    )

    df.drop(
        columns=["Date_tmp"],
        inplace=True
    )

except Exception:
    pass

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

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

with col4:

    st.metric(
        "Articles uniques",
        len(df)
    )

st.divider()

# =====================================================
# TABLEAU DES SOURCES
# =====================================================

st.subheader(
    "📊 Couverture des sources"
)

resume_sources = (

    df.groupby("Source")
      .size()
      .reset_index(
          name="Documents"
      )
      .sort_values(
          by="Documents",
          ascending=False
      )

)

st.dataframe(
    resume_sources,
    width="stretch"
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
# EXPORT CSV
# =====================================================

csv = df_filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Télécharger CSV",
    data=csv,
    file_name="veille_economique.csv",
    mime="text/csv"
)

# =====================================================
# TABLEAU DES DONNÉES
# =====================================================

st.dataframe(
    df_filtered,
    width="stretch"
)

st.divider()

# =====================================================
# DÉTAIL DES PUBLICATIONS
# =====================================================

st.subheader(
    "📄 Détail des publications"
)

for _, row in df_filtered.iterrows():

    st.markdown(
        f"### {row['Titre']}"
    )

    st.write(
        f"**Source :** {row['Source']}"
    )

    date = str(
        row.get(
            "Date",
            ""
        )
    ).strip()

    if date:

        st.write(
            f"**Date :** {date}"
        )

    lien = str(
        row.get(
            "Lien",
            ""
        )
    ).strip()

    pdf = str(
        row.get(
            "PDF",
            ""
        )
    ).strip()

    c1, c2 = st.columns(2)

    if lien:

        with c1:

            st.link_button(
                "🔗 Ouvrir",
                lien
            )

    if pdf:

        with c2:

            st.link_button(
                "📄 Télécharger PDF",
                pdf
            )

    st.divider()
