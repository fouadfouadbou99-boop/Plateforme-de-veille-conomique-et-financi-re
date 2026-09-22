# connectors/imf.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.imf.org/en/News"


def get_imf_documents():

    docs = []

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

            title = link.get_text(strip=True)

            if not title:
                continue

            if len(title) < 20:
                continue

            docs.append(
                {
                    "Source": "FMI",
                    "Titre": title,
                    "Date": "",
                    "Lien": urljoin(URL, link["href"]),
                    "PDF": link["href"]
                    if link["href"].lower().endswith(".pdf")
                    else ""
                }
            )

        return docs[:50]

    except Exception as e:

        print(f"FMI ERROR: {e}")

        return []
``
