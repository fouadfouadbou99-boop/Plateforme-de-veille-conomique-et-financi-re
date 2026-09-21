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

        st.warning(f"Erreur pour {source}: {e}")

df = pd.DataFrame(all_news)

if df.empty:

    st.warning("Aucune actualité récupérée.")

else:

    source_filtre = st.sidebar.multiselect(
        "Sources",
        sorted(df["Source"].unique()),
        default=sorted(df["Source"].unique())
    )

    mot_cle = st.sidebar.text_input(
        "Recherche"
    )

    df_filtre = df[
        df["Source"].isin(source_filtre)
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
        f"{len(df_filtre)} actualités trouvées."
    )

    st.dataframe(
        df_filtre,
        use_container_width=True
    )

    st.subheader("Détail des actualités")

    for _, row in df_filtre.head(20).iterrows():

        st.markdown(
            f"""
### {row['Titre']}

**Source :** {row['Source']}

**Date :** {row['Date']}

{row['Lien']}
"""
        )
