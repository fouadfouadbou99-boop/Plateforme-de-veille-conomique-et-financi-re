import streamlit as st
import pandas as pd

st.title("📰 Actualités")

df = pd.DataFrame(
    columns=[
        "source",
        "titre",
        "catégorie",
        "date_de_publication",
    ]
)

st.dataframe(df, use_container_width=True)
