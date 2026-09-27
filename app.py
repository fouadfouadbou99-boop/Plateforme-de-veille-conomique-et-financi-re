import streamlit as st
import requests
from openai import OpenAI

# =====================================================
# IMPORT PDF (OPTIONNEL)
# =====================================================

PDF_AVAILABLE = False

try:
    from io import BytesIO
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )
    from reportlab.lib.styles import getSampleStyleSheet

    PDF_AVAILABLE = True

except ImportError:
    PDF_AVAILABLE = False

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Veille Économique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CLÉS API
# =====================================================

try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

except Exception:

    st.error(
        "Impossible de charger les clés API depuis secrets.toml"
    )

    st.stop()

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
.main-header{
    font-size:2.4rem;
    font-weight:bold;
    color:#1E3A8A;
    text-align:center;
}
.metric-card{
    border-radius:10px;
    padding:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-header">📊 Plateforme de Veille Économique</div>',
    unsafe_allow_html=True
)

# =====================================================
# FILTRES
# =====================================================

SECTEURS = {
    "Tous": "economy",
    "Finance": "finance OR banking",
    "Industrie": "industry",
    "Agriculture": "agriculture",
    "Énergie": "energy OR oil OR gas",
    "Transport": "transport OR logistics",
    "Tourisme": "tourism",
    "Technologie": "technology",
    "Immobilier": "real estate",
    "Commerce": "retail"
}

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
# ACTUALITÉS
# =====================================================

@st.cache_data(ttl=3600)
def get_news(query, limit):

    url = (
        "https://newsapi.org/v2/everything"
        f"?q={query}"
        "&language=fr"
        "&sortBy=publishedAt"
        f"&pageSize={limit}"
        f"&apiKey={NEWS_API_KEY}"
    )

    try:

        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code == 200:

            return response.json().get(
                "articles",
                []
            )

        return []

    except Exception:
        return []

# =====================================================
# SYNTHÈSE IA
# =====================================================

def generer_synthese(articles):

    if not articles:
        return "Aucune actualité disponible."

    contenu = []

    for article in articles[:20]:

        titre = article.get(
            "title",
            ""
        )

        resume = article.get(
            "description",
            ""
        )

        contenu.append(
            f"Titre : {titre}\nRésumé : {resume}"
        )

    texte = "\n\n".join(contenu)

    prompt = f"""
Vous êtes un expert en veille économique.

Préparez une note destinée à un comité.

Actualités :

{texte}

Structure :

1. Résumé exécutif
2. Tendances observées
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

    except Exception as erreur:

        return f"Erreur lors de la génération : {erreur}"

# =====================================================
# PDF
# =====================================================

def creer_pdf(synthese):

    if not PDF_AVAILABLE:
        eturn None

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Synthèse de Veille Économique",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    for ligne in synthese.split("\n"):

        if ligne.strip():

            elements.append(
                Paragraph(
                    ligne,
                    styles["BodyText"]
                )
            )

            elements.append(
                Spacer(1, 5)
            )

    doc.build(elements)

    buffer.seek(0)

    return buffer

# =====================================================
# RÉCUPÉRATION DES DONNÉES
# =====================================================

requete = SECTEURS[secteur]

with st.spinner(
    "Recherche des actualités..."
):

    articles = get_news(
        requete,
        nombre_articles
    )

# =====================================================
# INDICATEURS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Articles",
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
# AFFICHAGE DES NOUVELLES
# =====================================================

st.subheader(
    "📰 Actualités économiques"
)

if not articles:

    st.warning(
        "Aucune actualité trouvée."
    )

else:

    for article in articles:

        titre = article.get(
            "title",
            "Titre indisponible"
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

        description = article.get(
            "description",
            ""
        )

        st.markdown(
            f"### {titre}"
        )

        st.caption(
            f"📅 {date} | 📰 {source}"
        )

        if description:
            st.write(
                description
            )

        url = article.get("url")

        if url:

            st.link_button(
                "Lire l'article",
                url
            )

        st.divider()

# =====================================================
# SYNTHÈSE
# =====================================================

st.subheader(
    "📑 Synthèse automatique"
)

if st.button(
    "Générer la synthèse"
):

    with st.spinner(
        "Analyse économique en cours..."
    ):

        st.session_state["synthese"] = (
            generer_synthese(
                articles
            )
        )

if "synthese" in st.session_state:

    st.markdown(
        st.session_state["synthese"]
    )

    if PDF_AVAILABLE:

        pdf = creer_pdf(
            st.session_state["synthese"]
        )

        st.download_button(
            label="📥 Télécharger PDF",
            data=pdf,
            file_name="Synthese_Veille_Economique.pdf",
            mime="application/pdf"
        )

    else:

        st.warning(
            "ReportLab n'est pas installé. Export PDF désactivé."
        )

        st.download_button(
            label="📥 Télécharger TXT",
            data=st.session_state["synthese"],
            file_name="Synthese_Veille_Economique.txt",
            mime="text/plain"
        )

# =====================================================
# À PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
        Cette application collecte les nouvelles
        économiques, permet leur filtrage par secteur,
        génère une synthèse automatique par IA
        et produit un export PDF ou texte.
        """
    )
