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
    "OCDE": "https://www.oecd.org/newsroom/rss.xml",
    "Banque Mondiale": "https://blogs.worldbank.org/en/rss.xml",
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
    st.success(f"{len(df)} actualités récupérées.")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Détails")

    for _, row in df.head(20).iterrows():

        st.markdown(
            f"""
### {row['Titre']}

**Source :** {row['Source']}

**Date :** {row['Date']}

🔗 {row['ien']}
"""
        )
