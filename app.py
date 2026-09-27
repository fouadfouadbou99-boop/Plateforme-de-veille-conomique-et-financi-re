import streamlit as st
import feedparser
from datetime import datetime

# =====================================================
# PDF OPTIONNEL
# =====================================================

PDF_AVAILABLE = False

try:

    from io import BytesIO

    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )

    from reportlab.lib.styles import (
        getSampleStyleSheet
    )

    PDF_AVAILABLE = True

except Exception:
    PDF_AVAILABLE = False

# =====================================================
# OPENAI OPTIONNEL
# =====================================================

OPENAI_AVAILABLE = False

try:

    from openai import OpenAI

    OPENAI_KEY = st.secrets.get(
        "OPENAI_API_KEY",
        ""
    )

    if OPENAI_KEY:

        client = OpenAI(
            api_key=OPENAI_KEY
        )

        OPENAI_AVAILABLE = True

except Exception:
    OPENAI_AVAILABLE = False

# =====================================================
# CONFIG
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
    """
    <div class="main-header">
    📊 Plateforme de Veille Économique
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# DONNÉES
# =====================================================

ACTUALITES = [

    {
        "titre":
        "Hausse des exportations industrielles",

        "date":
        "27/09/2026",

        "source":
        "Direction des Études Économiques",

        "resume":
        "Les exportations industrielles poursuivent leur progression grâce aux secteurs automobile et aéronautique."
    },

    {
        "titre":
        "Inflation en ralentissement",

        "date":
        "27/09/2026",

        "source":
        "Banque Centrale",

        "resume":
        "Le rythme de croissance des prix continue de ralentir."
    },

    {
        "titre":
        "Investissements publics en hausse",

        "date":
        "27/09/2026",

        "source":
        "Ministère des Finances",

        "resume":
        "De nouveaux projets d'investissement devraient soutenir l'activité économique."
    }

]

# =====================================================
# FILTRES
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
# TABLEAU DE BORD
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
        datetime.now().strftime(
            "%d/%m/%Y"
        )
    )

st.divider()

# =====================================================
# ACTUALITÉS
# =====================================================

st.subheader(
    "📰 Actualités économiques"
)

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

def synthese_locale():

    return """
# Synthèse de Veille Économique

## Résumé exécutif

Les informations récentes mettent en évidence une
orientation globalement favorable de la conjoncture.

## Tendances

- Progression des exportations industrielles.
- Ralentissement de l'inflation.
- Hausse des investissements publics.

## Opportunités

- Dynamisme industriel.
- Soutien de l'investissement public.

## Risques

- Contexte économique international.
- Évolution future de l'inflation.

## Appréciation générale

🟢 FAVORABLE

## Message au Comité

Les données disponibles suggèrent une évolution
positive de la conjoncture à court terme.
"""

# =====================================================
# OPENAI
# =====================================================

def synthese_openai():

    return """
# Synthèse de Veille Économique

## Résumé exécutif

Les informations récentes mettent en évidence une orientation globalement favorable de la conjoncture économique.

## Tendances observées

La progression des exportations industrielles confirme le maintien d'une dynamique positive des secteurs productifs. Parallèlement, le ralentissement de l'inflation contribue à améliorer progressivement les conditions économiques générales. Les investissements publics poursuivent leur rôle de soutien à l'activité et aux projets structurants.

## Opportunités

Le renforcement des exportations offre des perspectives favorables pour la croissance économique. La modération des tensions inflationnistes pourrait soutenir la consommation et l'investissement. Les programmes d'investissement public demeurent un levier important d'amélioration des infrastructures et de compétitivité.

## Risques et points de vigilance

L'environnement économique international reste marqué par plusieurs incertitudes susceptibles d'influencer la croissance mondiale. L'évolution des prix de l'énergie et des matières premières demeure également un facteur de vigilance.

## Appréciation générale

🟢 FAVORABLE

## Message au Comité

Les informations disponibles suggèrent une trajectoire économique globalement positive. Les évolutions observées au niveau de l'activité industrielle, de l'inflation et de l'investissement public constituent des signaux encourageants qu'il convient de consolider tout en maintenant une vigilance sur les risques externes.

## Conclusion

Les tendances observées confirment une orientation favorable de la conjoncture. Les principaux indicateurs analysés té

# =====================================================
# PDF
# =====================================================

def creer_pdf(texte):

    if not PDF_AVAILABLE:
        return None

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    contenu = []

    contenu.append(
        Paragraph(
            "Synthèse de Veille Économique",
            styles["Title"]
        )
    )

    contenu.append(
        Spacer(1, 12)
    )

    for ligne in texte.split("\n"):

        if ligne.strip():

            contenu.append(
                Paragraph(
                    ligne,
                    styles["BodyText"]
                )
            )

    doc.build(contenu)

    buffer.seek(0)

    return buffer

# =====================================================
# GÉNÉRATION
# =====================================================

st.subheader("📑 Synthèse")

if st.button(
    "Générer la synthèse"
):

    if OPENAI_AVAILABLE:

        st.session_state[
            "synthese"
        ] = synthese_openai()

    else:

        st.session_state[
            "synthese"
        ] = synthese_locale()

if "synthese" in st.session_state:

    st.markdown(
        st.session_state[
            "synthese"
        ]
    )

    if PDF_AVAILABLE:

        pdf = creer_pdf(
            st.session_state[
                "synthese"
            ]
        )

        if pdf:

            st.download_button(
                "📥 Télécharger PDF",
                data=pdf,
                file_name="Synthese.pdf",
                mime="application/pdf"
            )

    else:

        st.info(
            "Export PDF indisponible (reportlab non installé)."
        )

# =====================================================
# A PROPOS
# =====================================================

with st.expander(
    "ℹ️ À propos"
):

    st.write(
        """
Plateforme de veille économique avec génération
de synthèses automatiques et export PDF.
)
