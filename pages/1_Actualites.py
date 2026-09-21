import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Veille économique et financière")

df = pd.DataFrame(
    [
        {
            "Source": "BAM",
            "Titre": "Communiqué de politique monétaire",
            "Date": "2026-09-21",
            "Lien": "https://www.bkam.ma",
        },
        {
            "Source": "HCP",
            "Titre": "Publication de l'indice des prix",
            "Date": "2026-09-20",
            "Lien": "https://www.hcp.ma",
        },
        {
            "Source": "FMI",
            "Titre": "Perspectives économiques mondiales",
            "Date": "2026-09-19",
            "Lien": "https://www.imf.org",
        },
    ]
)

col1, col2, col3 = st.columns(3)

col1.metric("Actualités", len(df))
col2.metric("Sources", df["Source"].nunique())
col3.metric("Dernière date", df["Date"].max())

st.divider()

sources = st.multiselect(
    "Filtrer par source",
    sorted(df["Source"].unique()),
    default=sorted(df["Source"].unique()),
)

recherche = st.text_input("Recherche")

df_filtre = df[df["Source"].isin(sources)]

if recherche:
    df_filtre = df_filtre[
        df_filtre["Titre"].str.contains(
            recherche,
            case=False,
            na=False,
        )
    ]

st.dataframe(df_filtre, use_container_width=True)

st.subheader("Détail des actualités")

for _, row in df_filtre.iterrows():
    st.markdown(f"### {row['Titre']}")
    st.write(f"Source : {row['Source']}")
    st.write(f"Date : {row['Date']}")
    st.write(row["Lien"])
    st.divider()
