import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actualités",
    layout="wide"
)

st.title("📰 Actualités")

df = pd.DataFrame(
    columns=[
        "source",
        "title",
        "category",
        "publication_date",
    ]
)

st.dataframe(
    df,
    use_container_width=True
)
