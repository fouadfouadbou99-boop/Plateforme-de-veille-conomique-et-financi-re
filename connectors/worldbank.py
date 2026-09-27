import requests
from bs4 import BeautifulSoup

URL = "https://www.worldbank.org/en/news"

def get_worldbank_documents():

    docs = []

    try:

        response = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        liens = soup.find_all("a")

        for lien in liens:

            titre = lien.get_text(
                strip=True
            )

            href = lien.get(
                "href",
                ""
            )

            if len(titre) < 30:
                continue

            if not href:
                continue

            if href.startswith("/"):
                href = (
                    "https://www.worldbank.org"
                    + href
                )

            docs.append(
                {
                    "Source":
                    "Banque Mondiale",

                    "Titre":
                    titre,

                    "Date":
                    "",

                    "Lien":
                    href,

                    "PDF":
                    ""
                }
            )

        print(
            f"Banque Mondiale : {len(docs)} documents"
        )

        return docs[:50]

    except Exception as e:

        print(
            f"WORLD BANK ERROR : {e}"
        )

        return []
