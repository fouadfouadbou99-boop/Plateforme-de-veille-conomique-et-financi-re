import streamlit as st
import pandas as pd

st.title("📰 Actualités")

df = pd.DataFrame(
    columns=[
        "source",
        "title",
        "category",
        "publication_date",
    ]
)

st.dataframe(df, use_container_width=True)
