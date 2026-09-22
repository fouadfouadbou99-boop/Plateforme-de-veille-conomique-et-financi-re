import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.finances.gov.ma/fr/Pages/publications.aspx"


def get_mef_documents():

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

            if len(titre) < 15:
                continue

            if (
                ".pdf" not in href.lower()
                and "publication" not in href.lower()
            ):
                continue

            docs.append(
                {
                    "Source": "MEF",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, href),
                    "PDF": (
                        urljoin(URL, href)
                        if ".pdf" in href.lower()
                        else ""
                    )
                }
            )

        return docs[:50]

    except Exception as e:

        print(f"MEF ERROR: {e}")

        return []
``
