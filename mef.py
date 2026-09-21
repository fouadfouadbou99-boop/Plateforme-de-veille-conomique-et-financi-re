# connectors/mef.py

import requests
from bs4 import BeautifulSoup

URL = "https://www.finances.gov.ma/fr/Pages/publications.aspx"


def get_mef_documents():

    docs = []

    response = requests.get(URL, timeout=30)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for link in soup.find_all("a"):

        href = link.get("href")

        if not href:
            continue

        if ".pdf" in href.lower():

            docs.append(
                {
                    "Source": "MEF",
                    "Titre": link.get_text(strip=True),
                    "Date": "",
                    "Lien": href,
                    "PDF": href
                }
            )

    return docs[:30]
