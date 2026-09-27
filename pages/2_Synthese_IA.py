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

from connectors.aggregator import get_all_documents

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Synthèse IA",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Synthèse économique assistée par IA")

# =====================================================
# OPENAI
# =====================================================

client = None

try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)

except Exception:
    st.warning(
        "OpenAI non configuré. Utilisation de la synthèse locale."
    )

# =====================================================
# DONNEES
# =====================================================

@st.cache_data(ttl=1800)
def charger_donnees():
    return get_all_documents()


try:
    data = charger_donnees()

except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.stop()

df = pd.DataFrame(data)

if df.empty:
    st.warning("Aucune donnée disponible.")
    st.stop()

if "Titre" not in df.columns:
    st.error("La colonne 'Titre' est absente.")
    st.stop()

if "Source" not in df.columns:
    df["Source"] = "Non renseignée"

df["Titre"] = df["Titre"].fillna("").astype(str)
df["Source"] = df["Source"].fillna("Non renseignée").astype(str)

df = df.drop_duplicates(subset=["Titre"])

# =====================================================
# FILTRAGE
# =====================================================

MOTS_A_EXCLURE = [
    "Tout sur",
    "Vidéothèque",
    "Galerie",
    "Accueil",
    "Contact",
    "Classement",
    "Nomenclature"
]

masque = ~df["Titre"].str.contains(
    "|".join(MOTS_A_EXCLURE),
    case=False,
    na=False
)

df = df[masque]

if df.empty:
    st.warning(
        "Aucune publication exploitable après filtrage."
    )
    st.stop()

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Publications analysées",
        len(df)
    )

with col2:
    st.metric(
        "Sources",
        df["Source"].nunique()
    )

with col3:
    st.metric(
        "Titres uniques",
        len(df)
    )

# =====================================================
# TEXTE SOURCE
# =====================================================

texte = "\n\n".join(
    df["Titre"]
    .head(100)
    .tolist()
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
- institutionnel
- analytique
- paragraphes développés
- vocabulaire économique
- 700 à 1200 mots
"""

# =====================================================
# SYNTHESE DE SECOURS
# =====================================================

def synthese_secours():

    nb_docs = len(df)
    nb_sources = df["Source"].nunique()

    top_titles = (
        df["Titre"]
        .head(10)
        .tolist()
    )

    themes = {
        "Investissement": 0,
        "Croissance": 0,
        "Inflation": 0,
        "Commerce": 0,
        "Finances publiques": 0,
    }

    for titre in df["Titre"\]:

        t = str(titre).lower()

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

    themes_txt = "\n".join(
        [
            f"- {k} : {v}"
            for k, v in sorted(
                themes.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
    )

    publications_txt = "\n".join(
        [f"- {t}" for t in top_titles]
    )

    return f"""
# Synthèse économique et financière

## Résumé exécutif

L'analyse couvre {nb_docs} publications
issues de {nb_sources} sources institutionnelles.

## Publications marquantes

{publications_txt}

## Tendances observées

{themes_txt}

Les publications analysées montrent
une activité soutenue autour des enjeux
de croissance, d'investissement,
de financement et de compétitivité.

## Opportunités

Les programmes d'investissement
et les projets structurants constituent
les principales opportunités observées.

## Risques et points de vigilance

La conjoncture mondiale,
les tensions inflationnistes
et l'environnement financier international
appellent une vigilance continue.

## Appréciation générale
🟡 STABLE AVEC ORIENTATION FAVORABLE

## Message au Comité

La dynamique globale observée reste positive
tout en nécessitant un suivi régulier
des risques externes.

## Recommandations

- Renforcer la veille économique.
- Suivre les investissements stratégiques.
- Consolider l'analyse sectorielle.
- Surveiller les risques internationaux.

## Conclusion

Les publications analysées traduisent
une dynamique institutionnelle soutenue
et une orientation globalement favorable.
"""

# =====================================================
# IA OPENAI
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

    except Exception as e:

        st.warning(
            f"Erreur OpenAI : {e}"
        )

        return synthese_secours()

# =====================================================
# EXPORT PDF
# =====================================================

def creer_pdf(texte):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    contenu = [
        Paragraph(
            "Synthèse économique",
            styles["Title"]
        ),
        Spacer(1, 12)
    ]

    for ligne in texte.split("\n"):

        if ligne.strip():

            contenu.append(
                Paragraph(
                    ligne.replace("&", "&amp;"),
                    styles["BodyText"]
                )
            )

    doc.build(contenu)

    buffer.seek(0)

    return buffer

# =====================================================
# EXPORT WORD
# =====================================================

def creer_word(texte):

    document = Document()

    document.add_heading(
        "Synthèse économique",
        level=1
    )

    document.add_paragraph(texte)

    buffer = BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return buffer

# =====================================================
# GENERATION
# =====================================================

if st.button(
    "🚀 Générer la synthèse IA",
    use_container_width=True
):

    with st.spinner(
        "Analyse des publications..."
    ):

        st.session_state["synthese"] = (
            generer_synthese()
        )

# =====================================================
# AFFICHAGE
# =====================================================

if "synthese" in st.session_state:

    synthese = st.session_state["synthese"]

    st.markdown(synthese)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📄 Télécharger PDF",
            data=creer_pdf(synthese),
            file_name="Synthese_Economique.pdf",
            mime="application/pdf"
        )

    with col2:

        st.download_button(
            "📝 Télécharger Word",
            data=creer_word(synthese),
            file_name="Synthese_Economique.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
