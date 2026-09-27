import streamlit as st
import requests
from openai import OpenAI
from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Veille Économique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 1rem;
}
.section-title {
    color:#1E3A8A;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-header">📊 Plateforme de Veille Économique</div>',
    unsafe_allow_html=True
)

# =====================================================
# SECTEURS
# =====================================================

SECTEURS = {
    "Tous": "economy",
    "Finance": "bank OR finance",
    "Industrie": "industry OR manufacturing",
    "Agriculture": "agriculture",
    "Énergie": "energy OR oil OR gas",
    "Transport": "transport OR logistics",
    "Tourisme": "tourism",
    "Technologie": "technology OR digital",
    "Immobilier": "real estate",
    "Commerce": "retail OR commerce"
}

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filtres")

secteur = st.sidebar.selectbox(
    "Secteur économique",
    list(SECTEURS.keys())
)

nombre_articles = st.sidebar.slider(
    "Nombre d'articles",
    5,
    50,
    20
)

# =====================================================
# NEWS API
# =====================================================

@st.cache_data(ttl=3600)
def get_news(query):

    url = (
        "https://newsapi.org/v2/everything"
        f"?q={query}"
        "&language=fr"
        "&sortBy=publishedAt"
        f"&pageSize={nombre_articles}"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            return response.json().get("articles", [])

        return []

    except Exception:
        return []

# =====================================================
# IA
# =====================================================

def generer_synthese(articles):

    contenu = []

    for article in articles[:20]:

        titre = article.get("title", "")
        resume = article.get("description", "")

        contenu.append(
            f"Titre : {titre}\nRésumé : {resume}"
        )

    texte = "\n\n".join(contenu)

    prompt = f"""
Tu es un expert en veille économique.

Rédige une synthèse professionnelle destinée à un Comité.

Actualités :

{texte}

Structure :

1. Résumé exécutif
2. Principales tendances
3. Opportunités
4. Risques
5. Appréciation générale
6. Conclusion
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erreur IA : {e}"

# =====================================================
# PDF
# =====================================================

def creer_pdf(synthese):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Synthèse de Veille Économique",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 12))

    for ligne in synthese.split("\n"):

        if ligne.strip():

            story.append(
                Paragraph(
                    ligne,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 4)
            )

    doc.build(story)

    buffer.seek(0)

    return buffer

# =====================================================
# CHARGEMENT DES ACTUALITES
# =====================================================

requete = SECTEURS[secteur]

with st.spinner("Recherche des actualités..."):

    articles = get_news(requete)

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Articles récupérés",
        len(articles)
    )

with col2:
    st.metric(
        "Secteur",
        secteur
    )

with col3:
    st.metric(
        "Statut",
        "✅ Actif"
    )

st.divider()

# =====================================================
# ACTUALITES
# =====================================================

st.subheader("📰 Actualités récentes")

if not articles:

    st.warning(
        "Aucune actualité disponible."
    )

else:

    for article in articles:

        titre = article.get(
            "title",
            "Titre indisponible"
        )

        resume = article.get(
            "description",
            ""
        )

        source = article.get(
            "source",
            {}
        ).get(
            "name",
            "Source inconnue"
        )

        date = article.get(
            "publishedAt",
            ""
        )

        if len(date) >= 10:
            date = date[:10]

        with st.container():

            st.markdown(f"### {titre}")

            st.caption(
                f"📅 {date} | 📰 {source}"
            )

            if resume:
                st.write(resume)

            url = article.get("url")

            if url:
                st.link_button(
                    "Lire l'article",
                    url
                )

            st.divider()

# =====================================================
# SYNTHESE
# =====================================================

st.subheader("📑 Synthèse automatique")

if st.button("Générer la synthèse IA"):

    with st.spinner(
        "Analyse des nouvelles en cours..."
    ):

        synthese = generer_synthese(articles)

        st.session_state["synthese"] = synthese

if "synthese" in st.session_state:

    st.markdown(
        st.session_state["synthese"]
    )

    pdf = creer_pdf(
        st.session_state["synthese"]
    )

    st.download_button(
        label="📥 Télécharger la synthèse PDF",
        data=pdf,
        file_name="Synthese_Veille_Economique.pdf",
        mime="application/pdf"
    )

# =====================================================
# A PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
        Cette plateforme collecte automatiquement
        les actualités économiques, les filtre par secteur,
        génère une synthèse assistée par IA et permet
        l'export PDF pour diffusion aux décideurs.
        """
    )
