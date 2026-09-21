import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Veille économique et financière")

df = pd.DataFrame(
    {
        "Source": ["FMI", "Banque Mondiale"],
        "Titre": [
            "Article de test FMI",
            "Article de test Banque Mondiale"
        ]
    }
)

st.dataframe(df, use_container_width=True)
