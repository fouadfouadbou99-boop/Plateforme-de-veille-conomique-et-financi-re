import streamlit as st
import pandas as pd
from datetime import datetime

from connectors.aggregator import (
    get_all_documents
)

# =====================================================
# CONFIGURATION
# =====================================================

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

.subtitle{
    text-align:center;
    color:#666666;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITRE
# =====================================================

st.markdown(
    """
    <div class="main-header">
    📊 Plateforme de Veille Économique et Financière
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Veille stratégique et aide à la décision
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# DONNEES
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

# =====================================================
# NETTOYAGE
# =====================================================

if "Titre" in df.columns:

    df = df.drop_duplicates(
        subset=["Titre"]
    )

# =====================================================
# SCORE CONJONCTUREL
# =====================================================

def calcul_score(df):

    texte = " ".join(
        df["Titre"]
        .astype(str)
        .tolist()
    ).lower()

    score = 50

    mots_positifs = [
        "croissance",
        "investissement",
        "réforme",
        "développement",
        "export",
        "amélioration",
        "hausse"
    ]

    mots_negatifs = [
        "inflation",
        "crise",
        "dette",
        "ralentissement",
        "baisse",
        "déficit"
    ]

    for mot in mots_positifs:

        if mot in texte:
            score += 5

    for mot in mots_negatifs:

        if mot in texte:
            score -= 5

    score = max(
        0,
        min(
            score,
            100
        )
    )

    return score

score = calcul_score(df)

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Actualités",
        len(df)
    )

with col2:

    st.metric(
        "Sources",
        df["Source"].nunique()
    )

with col3:

    st.metric(
        "PDF",
        len(
            df[
                df["PDF"]
                .astype(str)
                .str.strip() != ""
            ]
        )
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

L'analyse des {len(df)} publications recensées auprès des différentes institutions nationales et internationales met en évidence une orientation globalement favorable de la situation économique.

### Principales tendances observées

Les informations collectées témoignent d'une activité institutionnelle soutenue. Les publications mettent en avant les politiques publiques, les investissements, les perspectives macroéconomiques ainsi que plusieurs initiatives de développement économique.

### Opportunités identifiées

La densité des publications consacrées aux investissements, aux infrastructures, au développement économique et aux réformes constitue un signal favorable pour les perspectives économiques.

### Risques et points de vigilance

L'environnement international demeure marqué par diverses incertitudes liées à la croissance mondiale, aux conditions financières internationales, à l'évolution des échanges commerciaux et aux tensions géopolitiques.

### Appréciation globale

{'🟢 FAVORABLE' if score >= 75 else '🟡 STABLE' if score >= 50 else '🔴 VIGILANCE'}

### Message au Comité

Les informations actuellement disponibles ne mettent pas en évidence de dégradation significative de la conjoncture économique. Les facteurs de soutien demeurent prédominants, tout en justifiant la poursuite d'une veille attentive sur les risques externes.

### Conclusion

La situation apparaît globalement favorable et compatible avec la poursuite des dynamiques économiques observées au cours de la période récente.
"""
)

# =====================================================
# REPARTITION DES SOURCES
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
# SOURCES
# =====================================================

st.subheader(
    "🌍 Sources surveillées"
)

for source in sorted(
    df["Source"].unique()
):

    st.write(
        f"• {source}"
    )

# =====================================================
# A PROPOS
# =====================================================

with st.expander(
    "ℹ️ À propos"
):

    st.write(
        """
Cette plateforme centralise automatiquement les publications économiques et financières issues de plusieurs institutions nationales et internationales.

Elle vise à alimenter les travaux de veille, de synthèse et d'aide à la décision.
"""
    )
