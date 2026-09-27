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
### Appréciation générale de la conjoncture

L'examen des informations collectées auprès des différentes institutions nationales et internationales met en évidence une orientation globalement favorable de la conjoncture économique. Les publications récentes convergent vers un diagnostic caractérisé par la résilience de l'activité économique, le maintien de l'effort d'investissement public et la poursuite de plusieurs programmes de développement économique.

### Principales tendances observées

Les informations disponibles témoignent d'une dynamique relativement positive dans plusieurs secteurs de l'économie. Les investissements publics continuent de soutenir l'activité économique et les projets structurants. Les publications institutionnelles mettent également en évidence la poursuite des efforts de modernisation économique et le renforcement progressif de certains indicateurs économiques.

Les informations diffusées par les organismes internationaux et les institutions financières confirment par ailleurs l'importance du maintien de politiques favorables au développement économique, à l'investissement et à l'amélioration de la compétitivité.

### Opportunités identifiées

La poursuite des investissements publics constitue un facteur important de soutien à l'activité économique. Les programmes en cours contribuent à renforcer les infrastructures, à améliorer l'attractivité économique et à soutenir l'investissement privé.

Parallèlement, les perspectives de développement de plusieurs secteurs productifs ainsi que le maintien de conditions relativement favorables à l'activité économique offrent des opportunités supplémentaires pour la croissance et l'emploi.

### Risques et points de vigilance

Malgré ces éléments favorables, plusieurs facteurs d'incertitude demeurent présents. L'évolution de la conjoncture internationale, les fluctuations des marchés mondiaux, les tensions géopolitiques ainsi que les risques liés à la croissance mondiale continuent de nécessiter un suivi attentif.

Une vigilance particulière demeure également recommandée concernant l'évolution des prix, des conditions financières internationales et des principaux facteurs susceptibles d'affecter les perspectives économiques à moyen terme.

### Appréciation globale

🟢 **FAVORABLE**

Au regard des informations analysées, les facteurs de soutien à l'activité économique apparaissent actuellement plus importants que les facteurs de risque identifiés. La situation économique demeure globalement orientée favorablement, tout en justifiant le maintien d'une veille permanente sur l'environnement international.

### Message au Comité

Les éléments recensés dans le cadre de la veille économique suggèrent une situation globalement satisfaisante. Les différents indicateurs suivis mettent en évidence une dynamique économique relativement robuste, soutenue notamment par l'investissement, la modernisation des infrastructures et la résilience observée dans plusieurs secteurs économiques.

Il est recommandé de poursuivre le suivi des évolutions internationales tout en consolidant les leviers de croissance identifiés afin de préserver les perspectives favorables observées au cours de la période récente.
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
