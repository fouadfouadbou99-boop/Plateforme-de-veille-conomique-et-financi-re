import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.imf.org/en/news"

def get_imf_documents():

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
                    "Source": "FMI",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, link["href"]),
                    "PDF": ""
                }
            )

        return docs[:50]

    except Exception as e:

        print(e)

        return []
