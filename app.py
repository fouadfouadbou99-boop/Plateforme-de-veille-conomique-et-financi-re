import streamlit as st
from datetime import datetime

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
    Veille stratégique destinée aux décideurs
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Actualités",
        "123"
    )

with col2:
    st.metric(
        "Sources",
        "5"
    )

with col3:
    st.metric(
        "PDF",
        "50"
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
# COMMENTAIRE AU COMITE
# =====================================================

st.subheader(
    "📌 Commentaire au Comité"
)

st.info(
    """
### Appréciation générale de la conjoncture

L'examen des informations collectées auprès des différentes institutions nationales et internationales met en évidence une orientation globalement favorable de la conjoncture économique. Les publications récentes convergent vers un diagnostic caractérisé par la résilience de l'activité économique, le maintien de l'effort d'investissement public et la poursuite de plusieurs programmes de développement économique.

### Principales tendances observées

Les informations disponibles témoignent d'une dynamique relativement positive dans plusieurs secteurs de l'économie. Les investissements publics continuent de soutenir l'activité économique et les projets structurants. Les publications institutionnelles mettent également en évidence la poursuite des efforts de modernisation économique et le renforcement progressif de certains indicateurs économiques.

Les informations diffusées par les organismes internationaux et les institutions financières confirment par ailleurs l'importance du maintien de politiques favorables au développement économique, à l'investissement et à l'amélioration de la compétitivité.

### Opportunités identifiées

Les informations recensées soulignent plusieurs opportunités favorables à la croissance économique.

Celles-ci concernent notamment les investissements structurants, le développement des infrastructures, l'amélioration de la compétitivité ainsi que le renforcement du climat de confiance des acteurs économiques.

La diversité des publications observées suggère également la poursuite des efforts de transformation et de modernisation économique.

### Risques et points de vigilance

Malgré ces éléments favorables, plusieurs facteurs d'incertitude demeurent présents.

Les évolutions de l'environnement économique international, les risques géopolitiques, les fluctuations des marchés mondiaux et les conditions financières internationales sont susceptibles d'affecter les perspectives de croissance.

Une vigilance particulière demeure également nécessaire concernant les risques externes susceptibles d'influencer l'activité économique nationale.

### Appréciation globale

🟢 **FAVORABLE**

Au regard des informations analysées, les facteurs de soutien à l'activité économique apparaissent actuellement plus importants que les facteurs de risque identifiés.

La situation économique demeure globalement orientée favorablement, tout en nécessitant le maintien d'un suivi régulier des principaux indicateurs de conjoncture.

### Message au Comité

Les informations examinées dans le cadre de la veille économique et financière suggèrent une situation globalement satisfaisante.

La dynamique observée est soutenue par la poursuite des investissements, l'activité institutionnelle soutenue ainsi que la mise en œuvre de différentes initiatives économiques.

Dans ce contexte, il est recommandé de poursuivre le suivi rapproché des évolutions internationales ainsi que des principaux indicateurs économiques afin de préserver les perspectives favorables actuellement observées.

### Conclusion

Les publications analysées convergent vers une appréciation positive de la situation économique générale.

Les différents éléments recensés ne font pas apparaître de facteur majeur de dégradation de la conjoncture, même si la surveillance de l'environnement international demeure essentielle.
"""
)

# =====================================================
# SOURCES SURVEILLEES
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
# FONCTIONNALITES
# =====================================================

st.subheader(
    "🚀 Fonctionnalités"
)

st.markdown(
    """
✅ Agrégation automatique des publications

✅ Filtrage par source

✅ Couverture des sources

✅ Recherche documentaire

✅ Déduplication automatique

✅ Téléchargement CSV

✅ Analyse conjoncturelle

✅ Commentaire automatique au Comité

✅ Préparation de l'intégration IA
"""
)

# =====================================================
# A PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
Cette plateforme centralise les publications économiques et financières
issues de plusieurs institutions nationales et internationales.

Elle vise à faciliter les travaux de veille, d'analyse et
de préparation des notes de conjoncture destinées aux décideurs.
"""
    )
