import streamlit as st
import pandas as pd

from connectors.aggregator import get_all_documents

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Veille économique et financière")

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
    "PDF",
]

for col in required_columns:

    if col not in df.columns:
        df[col] = ""

if df.empty:

    st.warning(
        "Aucune actualité disponible."
    )

    st.stop()

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

sources = sorted(
    df["Source"].fillna("").unique()
)

selected_sources = st.multiselect(
    "Filtrer par source",
    sources,
    default=sources
)

recherche = st.text_input(
    "Recherche"
)

df_filtre = df[
    df["Source"].isin(selected_sources)
]

if recherche:

    df_filtre = df_filtre[
        df_filtre["Titre"].astype(str).str.contains(
            recherche,
            case=False,
            na=False
        )
    ]

st.dataframe(
    df_filtre[
        [
            "Source",
            "Titre",
            "Date",
            "Lien",
            "PDF"
        ]
    ],
    width="stretch"
)

st.divider()

st.subheader(
    "Détail des publications"
)

for _, row in df_filtre.iterrows():

    titre = str(
        row.get("Titre", "")
    )

    source = str(
        row.get("Source", "")
    )

    date = str(
        row.get("Date", "")
    )

    lien = str(
        row.get("Lien", "")
    ).strip()

    pdf = str(
        row.get("PDF", "")
    ).strip()

    st.markdown(
        f"### {titre}"
    )

    if source:

        st.write(
            f"**Source :** {source}"
        )

    if date:

        st.write(
            f"**Date :** {date}"
        )

    col_a, col_b = st.columns(2)

    if lien:

        with col_a:

            st.link_button(
                "🔗 Ouvrir la publication",
                lien
            )

    if pdf:

        with col_b:

            st.link_button(
                "📄 Télécharger PDF",
                pdf
            )

    st.divider()
