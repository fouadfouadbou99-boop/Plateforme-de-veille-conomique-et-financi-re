import streamlit as st
import pandas as pd

st.title("📰 Actualités")

df = pd.read_sql(
    """
    select *
    from news
    order by publication_date desc
    """,
    conn
)

st.dataframe(
    df,
    use_container_width=True
)

source = st.selectbox(
    "Source",
    df["source"].unique()
)

categorie = st.selectbox(
    "Catégorie",
    df["category"].unique()
)
