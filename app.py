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

def synthese_locale():

    return """
# Synthèse de Veille Économique

## Résumé exécutif

Les informations collectées au cours de la période récente mettent en évidence une orientation globalement favorable de la conjoncture économique. Cette évolution repose principalement sur la progression des exportations industrielles, le ralentissement progressif des tensions inflationnistes et la poursuite des programmes d'investissement public. Ensemble, ces facteurs contribuent à soutenir l'activité économique et à renforcer les perspectives de croissance à court terme.

## Tendances observées

L'analyse des informations disponibles fait ressortir le maintien d'une dynamique positive des secteurs exportateurs. La progression des exportations industrielles témoigne de la résilience de l'appareil productif et de sa capacité à saisir les opportunités offertes par les marchés extérieurs.

Parallèlement, les pressions inflationnistes semblent poursuivre leur phase d'atténuation. Cette évolution contribue à améliorer les conditions économiques générales et à renforcer progressivement la confiance des agents économiques.

Enfin, l'accélération des investissements publics confirme le rôle central de la dépense publique dans le soutien de l'activité, notamment à travers le financement de projets structurants susceptibles d'améliorer la compétitivité économique à moyen terme.

## Opportunités

Les développements observés offrent plusieurs perspectives favorables. Le renforcement des exportations constitue un levier important de croissance et de diversification économique. La détente progressive de l'inflation pourrait favoriser une amélioration du pouvoir d'achat ainsi qu'un environnement plus propice à l'investissement privé.

Par ailleurs, la poursuite des investissements publics devrait soutenir l'activité dans plusieurs secteurs économiques et favoriser la modernisation des infrastructures.

## Risques et points de vigilance

Malgré ces évolutions encourageantes, certains facteurs d'incertitude demeurent présents. L'évolution de l'environnement économique international, les fluctuations des marchés des matières premières ainsi que les tensions géopolitiques pourraient affecter les perspectives économiques.

Une vigilance particulière demeure également nécessaire quant à l'évolution future de l'inflation et aux risques susceptibles d'influencer la demande extérieure.

## Appréciation générale

🟢 **FAVORABLE**

Les informations analysées convergent vers une appréciation globalement positive de la situation économique. Les signaux observés témoignent d'un contexte relativement porteur soutenu par les exportations, l'investissement et une amélioration progressive des conditions de prix.

## Message au Comité

Au regard des éléments recensés, la conjoncture économique apparaît globalement favorable. Les performances enregistrées par les secteurs exportateurs, combinées à la modération progressive de l'inflation et au maintien de l'effort d'investissement public, constituent des facteurs de soutien importants pour l'activité économique. Dans ce contexte, il conviendrait de poursuivre le suivi des risques externes tout en consolidant les leviers de croissance identifiés.

## Conclusion

Les informations récentes confirment une dynamique économique encourageante. Si certaines incertitudes persistent, les tendances actuellement observées demeurent compatibles avec un scénario de croissance soutenue et d'amélioration graduelle des principaux équilibres économiques.
"""

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
"""
    )
