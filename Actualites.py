import streamlit as st
import pandas as pd
import feedparser

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Actualités économiques et financières")

RSS_FEEDS = {
    "Bank Al-Maghrib": "https://www.bkam.ma/rss",
    "OCDE": "https://www.oecd.org/newsroom/rss.xml",
}

data = []

for source, url in RSS_FEEDS.items():
    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:20\]:
            data.append(
                {
                    "source": source,
                    "titre": entry.get("title", ""),
                    "date_de_publication": entry.get("published", ""),
                    "lien": entry.get("link", ""),
                }
            )

    except Exception as e:
        st.warning(f"Erreur lors du chargement de {source} : {e}")

df = pd.DataFrame(data)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    st.subheader("Détail des actualités")

    for _, row in df.head(20).iterrows():
        st.markdown(f"### {row['titre']}")
        st.write(f"**Source :** {row['source']}")
        st.write(f"**Date :** {row['date_de_publication']}")

        if row["lien"\]:
            st.markdown(f"{row['lien']}")

        st.divider()

else:
    st.info("Aucune actualité disponible.")
