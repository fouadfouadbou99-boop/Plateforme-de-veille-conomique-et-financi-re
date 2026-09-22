import requests
from bs4 import BeautifulSoup

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

            titre = link.get_text(strip=True)

            if len(titre) < 20:
                continue

            docs.append(
                {
                    "Source": "HCP",
                    "Titre": titre,
                    "Date": "",
                    "Lien": link["href"],
                    "PDF": ""
                }
            )

        return docs[:30]

    except Exception as e:

        print(e)

        return []
