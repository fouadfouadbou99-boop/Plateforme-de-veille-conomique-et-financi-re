import requests
from bs4 import BeautifulSoup

URL = "https://www.bkam.ma"

def get_bam_documents():

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

        for link in soup.find_all("a"):

            titre = link.get_text(
                strip=True
            )

            href = link.get(
                "href",
                ""
            )

            if len(titre) < 20:
                continue

            docs.append(
                {
                    "Source": "BAM",
                    "Titre": titre,
                    "Date": "",
                    "Lien": href,
                    "PDF": ""
                }
            )

        return docs[:50]

    except Exception as e:

        print(
            f"BAM ERROR : {e}"
        )

        return []
