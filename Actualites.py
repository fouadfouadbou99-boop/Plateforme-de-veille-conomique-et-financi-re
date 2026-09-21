import streamlit as st
import pandas as pd
import feedparser

st.set_page_config(page_title="Actualités", layout="wide")

st.title("📰 Actualités économiques et financières")

RSS_FEEDS = {
    "Bank Al-Maghrib": "https://www.bkam.ma/rss",
}

data = []

for source, url in RSS_FEEDS.items():
    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:20\]:
            data.append(
                {
                    "source": source,
                    "title": entry.get("title", ""),
                    "publication_date": entry.get("published", ""),
                }
            )

    except Exception as e:
        st.warning(f"Erreur lors du chargement du flux {source} : {e}")

df = pd.DataFrame(data)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune actualité disponible.")
