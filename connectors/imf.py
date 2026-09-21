# connectors/imf.py

import requests
from bs4 import BeautifulSoup

URL = "https://www.imf.org/en/news"


def get_imf_documents():

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
                "Source": "FMI",
                "Titre": title,
                "Date": "",
                "Lien": link.get("href"),
                "PDF": ""
            }
        )

    return docs[:20]
