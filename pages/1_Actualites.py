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

st.dataframe(
    df_filtered,
    width="stretch"
)

st.divider()

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
                "📄 PDF",
                pdf
            )

    st.divider()
