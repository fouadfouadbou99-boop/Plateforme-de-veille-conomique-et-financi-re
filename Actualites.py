import feedparser
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Veille économique et financière")

RSS_FEEDS = {
    "FMI": "https://www.imf.org/en/News/RSS",
    "Banque Mondiale": "https://blogs.worldbank.org/en/feed",
}

all_news = []

for source, url in RSS_FEEDS.items():

    try:

        feed = feedparser.parse(url)

        for entry in feed.entries[:20\]:

            all_news.append(
                {
                    "Source": source,
                    "Titre": entry.get("title", ""),
                    "Date": entry.get("published", ""),
                    "Lien": entry.get("link", ""),
                }
            )

    except Exception as e:

        st.warning(
            f"Erreur lors de la récupération des données depuis {source} : {e}"
        )

df = pd.DataFrame(all_news)

if df.empty:

    st.warning(
        "Aucune actualité récupérée."
    )

else:

    st.sidebar.header("Filtres")

    sources_selectionnees = st.sidebar.multiselect(
        "Sources",
        options=sorted(df["Source"].unique()),
        default=sorted(df["Source"].unique())
    )

    mot_cle = st.sidebar.text_input(
        "Recherche par mot-clé"
    )

    df_filtre = df[
        df["Source"].isin(sources_selectionnees)
    ]

    if mot_cle:

        df_filtre = df_filtre[
            df_filtre["Titre"].str.contains(
                mot_cle,
                case=False,
                na=False
            )
        ]

    st.success(
        f"{len(df_filtre)} actualités trouvées"
    )

    st.dataframe(
        df_filtre,
        use_container_width=True
    )

    st.subheader("Détail des actualités")

    for _, row in df_filtre.head(20).iterrows():

        st.markdown(f"### {row['Titre']}")

        st.write(
            f"**Source :** {row['Source']}"
        )

        st.write(
            f"**Date :** {row['Date']}"
        )

        if row["Lien"\]:

            st.markdown(
                f"{row['Lien']}"
            )

        st.divider()
