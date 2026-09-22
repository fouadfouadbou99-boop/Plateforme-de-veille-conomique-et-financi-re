# connectors/worldbank.py

import requests
from bs4 import BeautifulSoup

URL = "https://www.banquemondiale.org/ext/fr/home"


def get_worldbank_documents():

    docs = []

    response = requests.get(URL, timeout=30)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for link in soup.find_all("a"):

        title = link.get_text(strip=True)

        if len(title) < 20:
            continue

        docs.append(
            {
                "Source": "Banque Mondiale",
                "Titre": title,
                "Date": "",
                "Lien": link.get("href"),
                "PDF": ""
            }
        )

    return docs[:20]
