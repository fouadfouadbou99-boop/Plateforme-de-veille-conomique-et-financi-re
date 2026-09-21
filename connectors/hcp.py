# connectors/hcp.py

import requests
from bs4 import BeautifulSoup

URL = "https://www.hcp.ma/"


def get_hcp_documents():

    docs = []

    response = requests.get(URL, timeout=30)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for link in soup.find_all("a"):

        href = link.get("href")

        title = link.get_text(strip=True)

        if len(title) < 20:
            continue

        docs.append(
            {
                "Source": "HCP",
                "Titre": title,
                "Date": "",
                "Lien": href,
                "PDF": ""
            }
        )

    return docs[:20]
