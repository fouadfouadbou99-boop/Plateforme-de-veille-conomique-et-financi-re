import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.bkam.ma/Communiques"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0 Safari/537.36"
    )
}


def get_bam_documents():

    docs = []

    try:

        session = requests.Session()

        response = session.get(
            URL,
            headers=HEADERS,
            timeout=60
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for link in soup.find_all("a", href=True):

            titre = link.get_text(strip=True)

            if "Lire la suite" in titre:
                continue

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

        return docs[:30]

    except Exception as e:

        print(f"BAM ERROR: {e}")

        return []
