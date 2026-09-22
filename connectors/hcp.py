import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.hcp.ma/"


def get_hcp_documents():

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

            href = link["href"]
            titre = link.get_text(strip=True)

            if "_a" not in href:
                continue

            if len(titre) < 15:
                continue

            docs.append(
                {
                    "Source": "HCP",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, href),
                    "PDF": ""
                }
            )

        return docs[:50]

    except Exception as e:

        print(f"HCP ERROR: {e}")

        return []
