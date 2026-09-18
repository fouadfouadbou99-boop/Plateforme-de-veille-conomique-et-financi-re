import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Economic Intelligence",
    layout="wide"
)

st.title(
    "📊 Plateforme de Veille Économique"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Actualités", "1 254")

with col2:
    st.metric("Sources", "12")

with col3:
    st.metric("Alertes", "27")

with col4:
    st.metric("Documents", "318")

st.divider()

df = pd.DataFrame({
    "Categorie":[
        "Monétaire",
        "Finances",
        "Marchés",
        "Conjoncture"
    ],
    "Nombre":[87,65,44,96]
})

fig = px.pie(
    df,
    values="Nombre",
    names="Categorie",
    title="Répartition"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
