# connectors/bam.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.bkam.ma/Communiques"


def get_bam_documents():

    docs = []

    response = requests.get(URL, timeout=30)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for link in soup.find_all("a"):

        if "Lire la suite" not in link.get_text():
            continue

        href = link.get("href")

        docs.append(
            {
                "Source": "BAM",
                "Titre": href.split("/")[-1],
                "Date": "",
                "Lien": urljoin(URL, href),
                "PDF": ""
            }
        )

    return docs[:20]
