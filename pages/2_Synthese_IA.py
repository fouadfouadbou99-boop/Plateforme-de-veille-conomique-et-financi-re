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

from reportlab.lib.styles import getSampleStyleSheet

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
# DONNÉES
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

df = df[
    ~df["Titre"].str.contains(
        "|".join(MOTS_A_EXCLURE),
        case=False,
        na=False
    )
]

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

# Message au Comité

# Recommandations

# Conclusion

Style :
- institutionnel
- analytique
- vocabulaire économique
- 700 à 1200 mots
"""


# =====================================================
# SYNTHÈSE LOCALE
# =====================================================

def synthese_secours():

    nb_docs = len(df)
    nb_sources = df["Source"].nunique()

    top_titles = (
        df["Titre"]
        .head(20)
        .tolist()
    )

    themes = {
        "Investissement": 0,
        "Croissance": 0,
        "Inflation": 0,
        "Commerce": 0,
        "Finances publiques": 0
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
            f"- {nom} : {valeur}"
            for nom, valeur in sorted(
                themes.items(),
                key=lambda x: x[1],
                reverse=True
            )
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

L'analyse couvre {nb_docs} publications provenant de {nb_sources} sources.

## Publications marquantes

{publications_txt}

## Tendances observées

{themes_txt}

## Opportunités

Les publications mettent en avant plusieurs opportunités liées à l'investissement, à la croissance et à la modernisation économique.

## Risques et points de vigilance

Les principaux risques concernent la conjoncture internationale, l'inflation et les marchés financiers.

## Appréciation générale

🟡 STABLE AVEC ORIENTATION FAVORABLE

## Message au Comité

La dynamique observée demeure globalement positive tout en nécessitant une vigilance continue.

## Recommandations

- Renforcer la veille économique.
- Consolider le suivi des investissements.
- Approfondir les analyses sectorielles.
- Suivre les risques internationaux.

## Conclusion

Les publications 
