import streamlit as st
import feedparser
from openai import OpenAI
from datetime import datetime
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Veille Économique",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# OPENAI
# =====================================================

client = None

try:

    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

except:
    pass

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

.main-header{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#1f4e79;
    margin-bottom:30px;
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
# FILTRES
# =====================================================

SECTEURS = [
    "Tous",
    "Industrie",
    "Finance",
    "Agriculture",
    "Énergie",
    "Transport",
    "Tourisme"
]

st.sidebar.header("Filtres")

secteur = st.sidebar.selectbox(
    "Secteur économique",
    SECTEURS
)

nombre_articles = st.sidebar.slider(
    "Nombre d'articles",
    5,
    50,
    20
)

# =====================================================
# RSS
# =====================================================

RSS_SOURCES = {
    "HCP":
        "https://www.hcp.ma/rss.xml",

    "MEF":
        "https://www.finances.gov.ma/rss.xml",

    "BAM":
        "https://www.bkam.ma/rss",

    "IMF":
        "https://www.imf.org/en/News/RSS"
}

# =====================================================
# ACTUALITES
# =====================================================

@st.cache_data(ttl=3600)
def get_news(limit):

    articles = []

    for source, url in RSS_SOURCES.items():

        try:

            feed = feedparser.parse(url)

            for item in feed.entries:

                articles.append({

                    "titre":
                        item.get("title", ""),

                    "resume":
                        item.get(
                            "summary",
                            ""
                        ),

                    "date":
                        item.get(
                            "published",
                            ""
                        ),

                    "source":
                        source,

                    "url":
                        item.get(
                            "link",
                            ""
                        )
                })

        except:
            pass

    return articles[:limit]

# =====================================================
# APPRECIATION
# =====================================================

def evaluer_conjoncture(texte):

    score = 0

    mots_positifs = [
        "croissance",
        "hausse",
        "investissement",
        "progression",
        "amélioration"
    ]

    mots_negatifs = [
        "baisse",
        "crise",
        "recul",
        "inflation",
        "ralentissement"
    ]

    contenu = texte.lower()

    for mot in mots_positifs:

        if mot in contenu:
            score += 1

    for mot in mots_negatifs:

        if mot in contenu:
            score -= 1

    if score >= 2:
        return "🟢 FAVORABLE"

    if score <= -2:
        return "🔴 VIGILANCE"

    return "🟡 STABLE"

# ===============================
