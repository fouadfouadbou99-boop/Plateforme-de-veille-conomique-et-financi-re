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
        "Clé OpenAI non configurée."
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
# APERÇU
# =====================================================

st.metric(
    "Publications analysées",
    len(df)
)

# =====================================================
# CONSTRUCTION DU CONTEXTE
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

Produisez une note de conjoncture destinée
à un Comité de direction.

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
# IA
# =====================================================

def generer_synthese():

    if client is None:

        return """
OpenAI n'est pas configuré.
"""

    try:

        response = (
            client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role":"user",
                        "content":PROMPT
                    }
                ],
                temperature=0.2
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return (
            f"Erreur OpenAI : {e}"
        )

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
        Spacer(1,12)
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
# GÉNÉRATION
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
            file_name=
            "Synthese_Economique.pdf",
            mime=
            "application/pdf"
        )

    with col2:

        st.download_button(
            "📝 Télécharger Word",
            data=creer_word(
                synthese
            ),
            file_name=
            "Synthese_Economique.docx",
            mime=
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
