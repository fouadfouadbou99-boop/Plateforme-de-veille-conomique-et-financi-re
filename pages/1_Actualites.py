import streamlit as st
import pandas as pd

from connectors.aggregator import get_all_documents

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Veille économique et financière")

data = get_all_documents()

df = pd.DataFrame(data)

if df.empty:

    st.warning(
        "Aucune actualité disponible."
    )

else:

    st.metric(
        "Actualités",
        len(df)
    )

    st.dataframe(
        df,
        width="stretch"
    )
