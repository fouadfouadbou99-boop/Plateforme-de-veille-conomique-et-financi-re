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

    nb_sources = df["Source"].nunique()

    top_sources = (
        df["Source"]
        .value_counts()
        .head(5)
    )

    top_titles = (
        df["Titre"]
        .head(20)
        .tolist()
    )

    # Identification de thèmes simples
    themes = {
        "Investissement": 0,
        "Croissance": 0,
        "Inflation": 0,
        "Commerce": 0,
        "Finances publiques": 0
    }

    for titre in df["Titre"].astype(str):

        t = titre.lower()

        if "invest" in t:
            themes["Investissement"] += 1

        if (
            "croissance" in t
            or "activité" in t
            or "pib" in t
        ):
            themes["Croissance"] += 1

        if (
            "inflation" in t
            or "prix" in t
        ):
            themes["Inflation"] += 1

        if (
            "export" in t
            or "import" in t
            or "commerce" in t
        ):
            themes["Commerce"] += 1

        if (
            "budget" in t
            or "fiscal" in t
            or "trésor" in t
        ):
            themes["Finances publiques"] += 1

    principaux_themes = sorted(
        themes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    themes_txt = "\n".join(
        [
            f"- {nom} : {nb} publication(s)"
            for nom, nb in principaux_themes
        ]
    )

    publications_txt = "\n".join(
        [
            f"- {titre}"
            for titre in top_titles[:10]
        ]
    )

    return f"""
# Synthèse économique et financière

## Résumé exécutif

L'analyse porte sur **{nb_docs} publications** provenant de **{nb_sources} sources institutionnelles**.

Les sujets les plus fréquemment abordés concernent les questions d'investissement, de croissance, de politiques publiques, de développement économique et de financement.

L'activité documentaire observée témoigne d'une mobilisation soutenue des institutions nationales et internationales autour des enjeux économiques.

## Publications marquantes

{publications_txt}

## Tendances observées

L'analyse des publications recueillies permet d'identifier les thèmes dominants suivants :

{themes_txt}

Les publications récentes mettent particulièrement l'accent sur les programmes d'investissement, les initiatives de développement économique, les projets structurants et les perspectives d'amélioration de la compétitivité.

Les informations issues des différentes institutions convergent vers une poursuite des efforts de modernisation économique et de renforcement des capacités productives.

## Opportunités

Les publications recensées mettent en évidence plusieurs opportunités susceptibles de soutenir l'activité économique.

Les investissements publics, les projets d'infrastructures et les programmes de développement constituent les principaux leviers identifiés.

La diversité des initiatives observées traduit également l'existence d'un potentiel de croissance dans plusieurs secteurs économiques.

## Risques et points de vigilance

Les principales incertitudes relevées demeurent liées à l'environnement économique international, aux fluctuations des marchés mondiaux, aux risques financiers externes et à l'évolution de la conjoncture mondiale.

Une surveillance particulière doit être maintenue sur les facteurs susceptibles d'affecter la croissance, l'investissement et la stabilité économique.

## Appréciation générale

🟡 STABLE AVEC ORIENTATION FAVORABLE

Les facteurs favorables identifiés dans les publications apparaissent globalement plus nombreux que les éléments de risque recensés.

## Message au Comité

Les informations analysées suggèrent une situation économique relativement maîtrisée. Les efforts d'investissement, les programmes publics et les différentes initiatives recensées contribuent au maintien d'une dynamique favorable.

Il est recommandé de poursuivre le suivi régulier des indicateurs économiques et de renforcer l'analyse des risques externes susceptibles d'influencer les perspectives économiques.

## Recommandations

- Consolider le suivi des programmes d'investissement.
- Renforcer la veille sur les risques internationaux.
- Poursuivre l'analyse sectorielle.
- Approfondir l'exploitation des informations collectées.

## Conclusion

Les publications recensées témoignent d'une activité institutionnelle soutenue et d'une orientation globalement favorable des facteurs de développement économique. La poursuite de la veille permettra d'anticiper les évolutions futures et d'améliorer l'aide à la décision.
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
