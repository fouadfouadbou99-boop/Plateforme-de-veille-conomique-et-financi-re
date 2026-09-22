import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.bkam.ma/Communiques"


def get_bam_documents():

    docs = []

    try:

        response = requests.get(
            URL,
            timeout=60,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
                )
            }
        )

        if response.status_code != 200:
            print(f"BAM HTTP {response.status_code}")
            return []

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
                    "Source": "BAM",
                    "Titre": titre,
                    "Date": "",
                    "Lien": urljoin(URL, link["href"]),
                    "PDF": ""
                }
            )

        print(f"BAM: {len(docs)} documents")

        return docs[:50]

    except Exception as e:

        print(f"BAM ERROR: {e}")

        return []
