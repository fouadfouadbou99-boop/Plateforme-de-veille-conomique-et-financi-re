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

    return f"""
# Synthèse économique et financière

## Résumé exécutif

L'analyse couvre {nb_docs} publications
issues de {nb_sources} sources.

## Tendances observées

Les publications analysées mettent en évidence
une activité économique soutenue et une diversité
des thématiques suivies.

## Opportunités

Les projets d'investissement et les réformes
économiques constituent les principales opportunités.

## Risques

La conjoncture internationale et les tensions
inflationnistes demeurent des facteurs de vigilance.

## Appréciation générale

🟡 STABLE AVEC ORIENTATION FAVORABLE

## Recommandations

- Renforcer la veille.
- Consolider l'analyse sectorielle.
- Suivre les indicateurs macroéconomiques.

## Conclusion

La dynamique observée reste globalement favorable.
"""
