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

            if len(titre) < 10:
                continue

            href = link["href"]

            documents.append(
                {
                    "Source": "BAM",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, href),
                    "PDF": ""
                }
            )

        return documents[:20]

    except Exception as e:

        print(f"BAM ERROR : {e}")

        return []
