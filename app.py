import streamlit as st
import feedparser
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Veille Économique",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
.main-header{
    text-align:center;
    color:#1f4e79;
    font-size:42px;
    font-weight:bold;
    margin-bottom:20px;
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

SECTEURS = [
    "Tous",
    "Finance",
    "Industrie",
    "Agriculture",
    "Énergie",
    "Transport",
    "Tourisme",
    "Technologie",
    "Immobilier",
    "Commerce"
]

# =====================================================
# SIDEBAR
# =====================================================

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

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.oecd.org/newsroom/rss.xml"
]

# =====================================================
# ACTUALITÉS
# =====================================================

@st.cache_data(ttl=3600)
def get_news(limit):

    articles = []

    for rss_url in RSS_FEEDS:

        try:

            feed = feedparser.parse(rss_url)

            for item in feed.entries:

                articles.append({
                    "title": item.get("title", ""),
                    "description": item.get("summary", ""),
                    "publishedAt": item.get("published", ""),
                    "url": item.get("link", ""),
                    "source": rss_url
                })

        except Exception:
            pass

    return articles[:limit]

# =====================================================
# SYNTHÈSE
# =====================================================

def generer_synthese(articles):

    if len(articles) == 0:
        return """
## Aucune synthèse disponible

Aucune actualité économique n'a été récupérée.
"""

    titres = []

    for article in articles[:20]:

        titre = article.get("title", "")

        if titre:
            titres.append(f"• {titre}")

    texte = "\n".join(titres)

    return f"""
## Synthèse automatique

Nombre d'articles analysés : {len(articles)}

### Principales nouvelles

{texte}

### Commentaire

Les nouvelles recensées mettent en évidence les principaux
événements économiques publiés récemment par les sources suivies.

Cette synthèse est générée automatiquement à partir des titres
des articles collectés.
"""

# =====================================================
# DONNÉES
# =====================================================

articles = get_news(nombre_articles)

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
        "Date",
        datetime.now().strftime("%d/%m/%Y")
    )

st.divider()

# =====================================================
# ACTUALITÉS
# =====================================================

st.subheader("📰 Actualités économiques")

if len(articles) == 0:

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

        date = article.get(
            "publishedAt",
            ""
        )

        source = article.get(
            "source",
            ""
        )

        st.markdown(
            f"### {titre}"
        )

        st.caption(
            f"📅 {date}"
        )

        st.caption(
            f"📰 Source : {source}"
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

if st.button("Générer la synthèse"):

    st.session_state["synthese"] = (
        generer_synthese(articles)
    )

if "synthese" in st.session_state:

    st.markdown(
        st.session_state["synthese"]
    )

# =====================================================
# A PROPOS
# =====================================================

with st.expander("ℹ️ À propos"):

    st.write(
        """
Cette plateforme récupère automatiquement des actualités
économiques depuis plusieurs flux RSS publics et génère
une synthèse simplifiée des principales nouvelles.
"""
    )
