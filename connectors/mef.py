import requests
from bs4 import BeautifulSoup

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

            titre = link.get_text(strip=True)

            if not titre:
                continue

            docs.append(
                {
                    "Source": "MEF",
                    "Titre": titre,
                    "Date": "",
                    "Lien": link["href"],
                    "PDF": (
                        link["href"]
                        if ".pdf" in link["href"].lower()
                        else ""
                    ),
                }
            )

        return docs[:30]

    except Exception as e:

        print(e)

        return []
