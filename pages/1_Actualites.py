import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Veille économique et financière")

data = [
    {
        "Source": "BAM",
        "Titre": "Publication test BAM",
        "Date": "2026-09-21",
        "Lien": "https://www.bkam.ma",
        "PDF": "",
    },
    {
        "Source": "HCP",
        "Titre": "Publication test HCP",
        "Date": "2026-09-20",
        "Lien": "https://www.hcp.ma",
        "PDF": "",
    },
    {
        "Source": "FMI",
        "Titre": "Publication test FMI",
        "Date": "2026-09-19",
        "Lien": "https://www.imf.org",
        "PDF": "",
    },
]

df = pd.DataFrame(data)

c1, c2, c3 = st.columns(3)

c1.metric("Actualités", len(df))
c2.metric("Sources", df["Source"].nunique())
c3.metric("Dernière date", df["Date"].max())

st.divider()

sources = st.multiselect(
    "Filtrer par source",
    options=sorted(df["Source"].unique()),
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

st.dataframe(
    df_filtre,
    width="stretch",
)

st.subheader("Détail des actualités")

for _, row in df_filtre.iterrows():

    st.markdown(f"### {row['Titre']}")

    st.write(f"Source : {row['Source']}")
    st.write(f"Date : {row['Date']}")

    if row["Lien"\]:
        st.link_button(
            "🔗 Ouvrir",
            row["Lien"],
        )

    if row["PDF"\]:
        st.link_button(
            "📄 Télécharger PDF",
            row["PDF"],
        )

    st.divider()
