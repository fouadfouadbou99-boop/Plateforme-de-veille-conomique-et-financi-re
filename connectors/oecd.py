import requests
from bs4 import BeautifulSoup

URL = "https://www.oecd.org/newsroom/"

def get_oecd_documents():

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

        links = soup.find_all("a")

        for link in links:

            titre = link.get_text(
                strip=True
            )

            href = link.get(
                "href",
                ""
            )

            if len(titre) < 30:
                continue

            if not href:
                continue

            if href.startswith("/"):

                href = (
                    "https://www.oecd.org"
                    + href
                )

            docs.append(
                {
                    "Source": "OCDE",
                    "Titre": titre,
                    "Date": "",
                    "Lien": href,
                    "PDF": ""
                }
            )

        print(
            f"OCDE : {len(docs)} documents"
        )

        return docs[:50]

    except Exception as e:

        print(
            f"OCDE ERROR : {e}"
        )

        return []
