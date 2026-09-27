import streamlit as st
from datetime import datetime

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
    color:#1f4e79;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    font-size:18px;
    color:#666666;
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
    Système d'aide à la décision basé sur la veille économique nationale et internationale
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =====================================================
# TABLEAU DE BORD
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Sources actives",
        "5"
    )

with col2:

    st.metric(
        "Actualités",
        "123"
    )

with col3:

    st.metric(
        "Documents PDF",
        "50"
    )

with col4:

    st.metric(
        "Mise à jour",
        datetime.now().strftime(
            "%d/%m/%Y"
        )
    )

st.divider()

# =====================================================
# SCORE CONJONCTUREL
# =====================================================

score = 78

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
        "🔴 Conjoncture sous vigilance"
    )

# =====================================================
# COMMENTAIRE
# =====================================================

st.subheader(
    "📌 Commentaire au Comité"
)

st.info(
    """
Les informations actuellement collectées suggèrent une orientation globalement favorable de la conjoncture économique.

Les publications récentes mettent en évidence la poursuite de l'investissement public, la résilience de plusieurs secteurs économiques ainsi qu'un environnement globalement porteur.

Une attention particulière demeure néanmoins nécessaire concernant l'évolution de l'environnement économique international.
"""
)

# =====================================================
# SOURCES SURVEILLÉES
# =====================================================

st.subheader(
    "🌍 Sources surveillées"
)

st.markdown(
    """
- Haut-Commissariat au Plan (HCP)
- Ministère de l'Économie et des Finances (MEF)
- Bank Al-Maghrib (BAM)
- Banque Mondiale
- Banque Centrale Européenne (BCE)
"""
)

# =====================================================
# FONCTIONNALITÉS
# =====================================================

st.subheader(
    "🚀 Fonctionnalités"
)

st.markdown(
    """
✅ Agrégation automatique des publications

✅ Filtrage par source

✅ Recherche documentaire

✅ Déduplication automatique

✅ Téléchargement CSV

✅ Indicateurs de couverture des sources

✅ Analyse de la conjoncture

✅ Préparation des synthèses IA
"""
)

# =====================================================
# A PROPOS
# =====================================================

with st.expander(
    "ℹ️ À propos"
):

    st.write(
        """
Cette plateforme centralise les publications économiques et financières issues de plusieurs institutions nationales et internationales.

Les informations collectées sont destinées à alimenter les travaux d'analyse, de veille et de préparation des notes à l'attention des décideurs.
"""
    )
