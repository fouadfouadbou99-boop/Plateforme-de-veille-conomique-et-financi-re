import requests
from bs4 import BeautifulSoup

URL = "https://www.bkam.ma/Communiques"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0 Safari/537.36"
    )
}


def get_bam_documents():

    try:

        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=60
        )

        if response.status_code != 200:
            print(
                f"BAM ERROR : HTTP {response.status_code}"
            )
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return [
            {
                "Source": "BAM",
                "Titre": "Connexion BAM réussie",
                "Date": "",
                "Lien": URL,
                "PDF": ""
            }
        ]

    except Exception as e:

        print(f"BAM ERROR : {e}")

        return []
