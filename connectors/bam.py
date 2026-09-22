import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://www.bkam.ma/fr"


def get_bam_documents():

    documents = []

    try:

        response = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for link in soup.find_all("a", href=True):

            titre = link.get_text(strip=True)

            href = link["href"]

            if not titre:
                continue

            if len(titre) < 15:
                continue

            documents.append(
                {
                    "Source": "BAM",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, href),
                    "PDF": href if href.lower().endswith(".pdf") else ""
                }
            )

        return documents[:50]

    except Exception as e:

        print(f"BAM ERROR : {e}")

        return []
