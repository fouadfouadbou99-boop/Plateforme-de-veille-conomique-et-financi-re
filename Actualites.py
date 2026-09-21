import streamlit as st
import pandas as pd
import feedparser

st.title("📰 Actualités")

RSS_URL = "https://rss.cnn.com/rss/edition.rss"

feed = feedparser.parse(RSS_URL)

data = []

for entry in feed.entries[:20\]:
    data.append(
        {
            "source": "CNN",
            "title": entry.title,
            "publication_date": entry.get("published", ""),
        }
    )

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)
