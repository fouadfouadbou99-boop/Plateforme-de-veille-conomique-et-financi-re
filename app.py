import streamlit as st
import requests

# =====================================================
# PDF (OPTIONNEL)
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

except Exception:
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
# CLÉS API (FACULTATIVES)
# =====================================================

NEWS_API_KEY = ""

OPENAI_API_KEY = ""

try:
    NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
except Exception:
    pass

try:
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
except Exception:
    pass

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
.main-header {
    font-size: 2.4rem;
    font-weight: bold;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 15px;
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
    "Finance": "finance",
    "Industrie": "industry",
    "Agriculture": "agriculture",
    "Énergie": "energy",
    "Transport": "transport",
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
# NEWS API
# =====================================================

@st.cache_data(ttl=3600)
def get_news(query, limit):

    if not NEWS_API_KEY:
        return []

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

    except Exception:
        pass

    return []

# =====================================================
# SYNTHÈSE
# =====================================================

def generer_synthese(articles):

    if not articles:

        return """
### Aucune synthèse disponible

Aucune actualité n'a été trouvée ou la clé NewsAPI n'est pas configurée.
"""

    textes = []

    for article in articles[:20\]:

        titre = article.get(
            "title",
            ""
        )

        resume = article.get(
            "description",
            ""
        )

        textes.append(
            f"• {titre}\n{resume}"
        )

    return f"""
## Synthèse automatique

Nombre d'articles analysés : {len(articles)}

### Principales informations

{chr(10).join(textes[:10])}

### Commentaire

Les éléments ci-dessus constituent les principales nouvelles économiques
collectées automatiquement. Configurez la clé OpenAI ultérieurement pour
obtenir une synthèse rédigée par intelligence artificielle.
"""

# ====================================================
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
            "Synthèse de Veille Economique",
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
# CHARGEMENT
# =====================================================

requete = SECTEURS[secteur]

articles = get_news(
    requete,
    nombre_articles
)

# =====================================================
# TABLEAU DE BORD
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
        "✅ Application active"
    )

st.divider()

# =====================================================
# INFORMATION CLÉS
# =====================================================

if not NEWS_API_KEY:

    st.warning(
        "NEWS_API_KEY non configurée dans Streamlit Cloud. "
        "L'application fonctionne mais aucune actualité ne peut être chargée."
    )

# =====================================================
# ACTUALITÉS
# =====================================================

st.subheader("📰 Actualités économiques")

if not articles:

    st.info(
        "Aucune actualité disponible."
    )

else:

    for article in articles:

        titre = article.get(
            "title",
            "Titre indisponible"
        )

        description = article.get(
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

        if date:
            date = date[:10]

        st.markdown(
            f"### {titre}"
        )

        st.caption(
            f"📅 {date} | 📰 {source}"
        )

        if description:
            st.write(description)

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

st.subheader("📑 Synthèse")

if st.button(
    "Générer la synthèse"
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

        if pdf:

            st.download_button(
                "📥 Télécharger PDF",
                data=pdf,
                file_name="Synthese_Veille_Economique.pdf",
                mime="application/pdf"
            )

# =====================================================
# À PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
        Plateforme de veille économique avec filtrage sectoriel,
        consultation des actualités et génération d'une synthèse.
        """
    )
