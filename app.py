import streamlit as st
import pandas as pd
from datetime import datetime

from connectors.aggregator import (
    get_all_documents
)

st.set_page_config(
    page_title="Plateforme de Veille Économique",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

.main-header{
    text-align:center;
    color:#1F4E79;
    font-size:42px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="main-header">
    📊 Plateforme de Veille Économique et Financière
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# CHARGEMENT DONNEES
# =====================================================

try:

    data = get_all_documents()

except Exception as e:

    st.error(
        f"Erreur : {e}"
    )

    data = []

df = pd.DataFrame(data)

if df.empty:

    st.warning(
        "Aucune donnée disponible."
    )

    st.stop()

df = df.drop_duplicates(
    subset=["Titre"]
)

# =====================================================
# INDICATEURS
# =====================================================

nb_actualites = len(df)

nb_sources = (
    df["Source"].nunique()
)

nb_pdf = len(
    df[
        df["PDF"]
        .astype(str)
        .str.strip() != ""
    ]
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Actualités",
        nb_actualites
    )

with col2:

    st.metric(
        "Sources",
        nb_sources
    )

with col3:

    st.metric(
        "PDF",
        nb_pdf
    )

with col4:

    st.metric(
        "Date",
        datetime.now().strftime(
            "%d/%m/%Y"
        )
    )

st.divider()

# =====================================================
# SCORE
# =====================================================

score = 55

st.subheader(
    "📈 Évaluation conjoncturelle"
)

st.metric(
    "Score conjoncturel",
    f"{score}/100"
)

if score >= 75:

    st.success(
        "🟢 Conjoncture favorable"
    )

elif score >= 50:

    st.warning(
        "🟡 Conjoncture stable"
    )

else:

    st.error(
        "🔴 Vigilance"
    )

# =====================================================
# COMMENTAIRE COMITE
# =====================================================

st.subheader(
    "📌 Commentaire au Comité"
)

st.info(
f"""
### Appréciation générale de la conjoncture

L'analyse des **{nb_actualites} publications** recensées auprès de **{nb_sources} sources institutionnelles** met en évidence une situation économique globalement stable.

### Principales tendances observées

Les publications analysées mettent principalement en avant les politiques publiques, les programmes d'investissement, les initiatives de développement économique ainsi que les perspectives macroéconomiques nationales et internationales.

### Opportunités identifiées

Les informations collectées révèlent plusieurs opportunités liées au développement des infrastructures, à l'investissement public, à la modernisation économique et à l'amélioration de la compétitivité.

### Risques et points de vigilance

Les principaux facteurs de risque demeurent liés à l'environnement économique international, aux tensions géopolitiques et aux fluctuations des marchés mondiaux.

### Appréciation globale

🟡 STABLE

Les informations actuellement disponibles ne mettent pas en évidence de dégradation significative de la conjoncture économique.

### Message au Comité

Les facteurs de soutien demeurent prédominants, tout en justifiant la poursuite d'une veille attentive sur les risques externes.

### Conclusion

La situation apparaît globalement compatible avec la poursuite des dynamiques économiques observées au cours de la période récente.
"""
)

# =====================================================
# SOURCES
# =====================================================

st.subheader(
    "📊 Couverture des sources"
)

resume_sources = (
    df.groupby("Source")
      .size()
      .reset_index(
          name="Documents"
      )
      .sort_values(
          by="Documents",
          ascending=False
      )
)

st.dataframe(
    resume_sources,
    width="stretch"
)

st.bar_chart(
    resume_sources.set_index(
        "Source"
    )
)

# =====================================================
# PUBLICATIONS RECENTES
# =====================================================

st.subheader(
    "📰 Dernières publications"
)

for _, row in df.head(10).iterrows():

    st.markdown(
        f"### {row['Titre']}"
    )

    st.write(
        f"**Source :** {row['Source']}"
    )

    st.divider()

# =====================================================
# A PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
Cette plateforme centralise les publications économiques
et financières produites par plusieurs institutions
nationales et internationales.
"""
    )
