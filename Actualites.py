import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Actualités économiques et financières")

df = pd.DataFrame(
    columns=[
        "source",
        "titre",
        "catégorie",
        "date_de_publication"
    ]
)

st.dataframe(df, use_container_width=True)

st.success("Page Actualités opérationnelle")
