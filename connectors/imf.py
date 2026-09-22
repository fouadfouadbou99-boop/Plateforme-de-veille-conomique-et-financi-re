import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.imf.org/en/news"


def get_imf_documents():

    docs = []

    try:

        response = requests.get(
            URL,
            timeout=60,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        seen = set()

        for link in soup.find_all("a", href=True):

            title = link.get_text(strip=True)

            if len(title) < 25:
                continue

            if title in seen:
                continue

            seen.add(title)

            docs.append(
                {
                    "Source": "FMI",
                    "Titre": title,
                    "Date": "",
                    "Lien": urljoin(URL, link["href"]),
                    "PDF": (
                        urljoin(URL, link["href"])
                        if link["href"].lower().endswith(".pdf")
                        else ""
                    )
                }
            )

        return docs[:50]

    except Exception as e:

        print(f"FMI ERROR: {e}")

        return []
