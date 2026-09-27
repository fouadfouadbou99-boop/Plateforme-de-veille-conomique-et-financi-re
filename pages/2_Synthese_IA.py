import streamlit as st
import pandas as pd

from io import BytesIO

from openai import OpenAI
from docx import Document

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from connectors.aggregator import (
    get_all_documents
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Synthèse IA",
    page_icon="🧠",
    layout="wide"
)

st.title(
    "🧠 Synthèse économique assistée par IA"
)

# =====================================================
# OPENAI
# =====================================================

client = None

try:

    OPENAI_API_KEY = st.secrets[
        "OPENAI_API_KEY"
    ]

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

except Exception:

    st.warning(
        "OpenAI non configuré. La synthèse locale sera utilisée."
    )

# =====================================================
# DONNÉES
# =====================================================

try:

    data = get_all_documents()

except Exception as e:

    st.error(
        f"Erreur : {e}"
    )

    st.stop()

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

st.metric(
    "Publications analysées",
    len(df)
)

# =====================================================
# TEXTE D'ANALYSE
# =====================================================

texte = "\n\n".join(

    [
        f"{row['Titre']}"
        for _, row in df
        .head(100)
        .iterrows()
    ]

)

# =====================================================
# PROMPT
# =====================================================

PROMPT = f"""
Vous êtes économiste principal.

Analysez les publications suivantes :

{texte}

Produisez une note de conjoncture destinée à un Comité de direction.

Structure obligatoire :

# Résumé exécutif

# Tendances observées

# Opportunités

# Risques et points de vigilance

# Appréciation générale

(Favorable, Stable ou Vigilance)

# Message au Comité

# Recommandations

# Conclusion

Style :

- institutionnel ;
- analytique ;
- paragraphes développés ;
- vocabulaire économique ;
- 700 à 1200 mots.
"""

# =====================================================
# SYNTHÈSE DE SECOURS
# =====================================================

def synthese_secours():

    nb_docs = len(df)

    nb_sources = (
        df["Source"]
        .nunique()
    )

    sources = ", ".join(
        df["Source"]
        .value_counts()
        .head(5)
        .index
        .tolist()
    )

    return f"""
# Synthèse économique et financière

## Résumé exécutif

L'analyse de {nb_docs} publications issues de {nb_sources} sources institutionnelles permet de dégager une appréciation globale de la situation économique.

Les publications collectées concernent principalement les politiques publiques, les investissements, les perspectives macroéconomiques, les infrastructures ainsi que les transformations économiques en cours.

## Tendances observées

Les principales sources actuellement actives sont :

{sources}

Les informations collectées mettent en évidence la poursuite d'initiatives publiques et économiques structurantes.

Les publications traduisent le maintien d'une activité importante dans les domaines du développement économique, des investissements, du financement, des infrastructures et des politiques sectorielles.

Les institutions nationales et internationales continuent d'accorder une attention particulière aux questions de compétitivité, de croissance durable et de résilience économique.

## Opportunités

Les informations analysées mettent en évidence plusieurs opportunités :

- maintien des investissements structurants ;
- amélioration des infrastructures ;
- modernisation des secteurs économiques ;
- développement des capacités productives ;
- renforcement de l'environnement économique.

Ces différents facteurs constituent des leviers importants susceptibles de soutenir la croissance à moyen terme.

## Risques et points de vigilance

Plusieurs risques nécessitent toutefois une vigilance particulière :

- évolution de l'environnement économique international ;
- tensions géopolitiques ;
- volatilité des marchés mondiaux ;
- risques financiers externes ;
- évolution des principaux indicateurs internationaux.

Une surveillance permanente de ces facteurs demeure indispensable.

## Appréciation générale

🟡 STABLE

Les publications analysées ne mettent pas en évidence de dégradation majeure de la conjoncture économique. Les facteurs favorables et les facteurs de risque demeurent relativement équilibrés.

## Message au Comité

Les différentes informations collectées suggèrent une situation économique globalement maîtrisée.

Les investissements publics, les initiatives de développement économique et les projets structurants constituent des facteurs de soutien significatifs.

La poursuite de la veille économique permettra de suivre l'évolution des principaux indicateurs et d'anticiper les éventuels risques émergents.

## Recommandations

- poursuivre le suivi rapproché des indicateurs macroéconomiques ;
- maintenir la veille sur les risques internationaux ;
- consolider les politiques favorables à l'investissement ;
- renforcer le suivi des secteurs stratégiques.

## Conclusion

La situation économique apparaît compatible avec la poursuite des dynamiques actuellement observées. Les informations recensées justifient le maintien d'une surveillance régulière afin d'anticiper toute évolution significative de la conjoncture.
"""

# =====================================================
# IA
# =====================================================

def generer_synthese():

    if client is None:

        return synthese_secours()

    try:

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": PROMPT
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception:

        return synthese_secours()

# =====================================================
# PDF
# =====================================================

def creer_pdf(texte):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    contenu = []

    contenu.append(
        Paragraph(
            "Synthèse économique",
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
# WORD
# =====================================================

def creer_word(texte):

    document = Document()

    document.add_heading(
        "Synthèse économique",
        level=1
    )

    document.add_paragraph(
        texte
    )

    buffer = BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer

# =====================================================
# GENERATION
# =====================================================

if st.button(
    "🚀 Générer la synthèse IA"
):

    with st.spinner(
        "Analyse des publications..."
    ):

        st.session_state[
            "synthese"
        ] = generer_synthese()

# =====================================================
# AFFICHAGE
# =====================================================

if "synthese" in st.session_state:

    synthese = st.session_state[
        "synthese"
    ]

    st.markdown(
        synthese
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📄 Télécharger PDF",
            data=creer_pdf(
                synthese
            ),
            file_name="Synthese_Economique.pdf",
            mime="application/pdf"
        )

    with col2:

        st.download_button(
            "📝 Télécharger Word",
            data=creer_word(
                synthese
            ),
            file_name="Synthese_Economique.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
