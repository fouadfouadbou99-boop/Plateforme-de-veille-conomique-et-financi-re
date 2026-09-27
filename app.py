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

generer_commentaire_ia(df)
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
