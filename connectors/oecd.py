import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.oecd.org/newsroom/"


def get_oecd_documents():

    docs = []

    try:

        response = requests.get(
            URL,
            timeout=60,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for link in soup.find_all("a", href=True):

            titre = link.get_text(strip=True)

            if len(titre) < 20:
                continue

            docs.append(
                {
                    "Source": "OCDE",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, link["href"]),
                    "PDF": ""
                }
            )

        return docs[:50]

    except Exception as e:

        print(f"OECD ERROR: {e}")

        return []
``
