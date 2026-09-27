import streamlit as st
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Veille Économique",
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
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-header">📊 Plateforme de Veille Économique</div>',
    unsafe_allow_html=True
)

# =====================================================
# DONNÉES DE DÉMONSTRATION
# =====================================================

ACTUALITES = [

    {
        "titre": "Hausse des exportations industrielles",
        "date": "27/09/2026",
        "source": "Direction des Études Économiques",
        "resume": "Les exportations industrielles poursuivent leur progression grâce aux secteurs automobile et aéronautique."
    },

    {
        "titre": "Inflation en ralentissement",
        "date": "27/09/2026",
        "source": "Banque Centrale",
        "resume": "Le rythme de croissance des prix continue de ralentir sous l'effet de la baisse des coûts énergétiques."
    },

    {
        "titre": "Investissements publics en hausse",
        "date": "27/09/2026",
        "source": "Ministère des Finances",
        "resume": "De nouveaux projets d'investissement devraient soutenir l'activité économique."
    }

]

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filtres")

secteur = st.sidebar.selectbox(
    "Secteur économique",
    [
        "Tous",
        "Industrie",
        "Finance",
        "Agriculture",
        "Énergie",
        "Transport",
        "Tourisme"
    ]
)

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Articles",
        len(ACTUALITES)
    )

with col2:
    st.metric(
        "Secteur",
        secteur
    )

with col3:
    st.metric(
        "Date",
        datetime.now().strftime("%d/%m/%Y")
    )

st.divider()

# =====================================================
# ACTUALITÉS
# =====================================================

st.subheader("📰 Actualités économiques")

for article in ACTUALITES:

    st.markdown(
        f"### {article['titre']}"
    )

    st.caption(
        f"📅 {article['date']} | 📰 {article['source']}"
    )

    st.write(
        article["resume"]
    )

    st.divider()

# =====================================================
# SYNTHÈSE
# =====================================================

st.subheader("📑 Synthèse")

if st.button("Générer la synthèse"):

    synthese = """
### Synthèse automatique

L'analyse des informations disponibles met en évidence
une orientation globalement favorable de la conjoncture.

Les exportations industrielles affichent une progression
soutenue tandis que les tensions inflationnistes
continuent de s'atténuer.

Les investissements publics demeurent un facteur
important de soutien de l'activité économique.

Appréciation générale : Favorable.
"""

    st.session_state["synthese"] = synthese

if "synthese" in st.session_state:

    st.markdown(
        st.session_state["synthese"]
    )

# =====================================================
# À PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
Cette plateforme de veille économique permet de
consulter les nouvelles économiques et de produire
une synthèse destinée aux décideurs.
"""
    )
