import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actualités",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Veille économique et financière")

try:
    from connectors.aggregator import get_all_documents

    data = get_all_documents()

except Exception as e:
    st.error(f"Erreur chargement données : {e}")
    data = []

df = pd.DataFrame(data)

st.write(df)

if not df.empty:

    for _, row in df.iterrows():

        st.markdown(f"### {row.get('Titre','')}")

        lien = row.get("Lien", "")

        if lien:
            st.link_button(
                "🔗 Ouvrir",
                lien
            )

        pdf = row.get("PDF", "")

        if pdf:
            st.link_button(
                "📄 PDF",
                pdf
            )

        st.divider()
