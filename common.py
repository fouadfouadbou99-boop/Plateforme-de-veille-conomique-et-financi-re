import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_pdf_from_page(page_url):

    try:

        response = requests.get(
            page_url,
            timeout=30,
            headers=HEADERS
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for link in soup.find_all("a"):

            href = link.get("href")

            if href and ".pdf" in href.lower():

                return urljoin(
                    page_url,
                    href
                )

    except Exception:

        pass

    return ""
