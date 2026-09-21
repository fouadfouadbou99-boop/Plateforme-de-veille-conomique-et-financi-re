import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.bkam.ma"
URL = "https://www.bkam.ma/Communiques"


def extract_date(text):
    pattern = r"\d{2}-\d{2}-\d{4}"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def get_bam_news(limit=30):

    results = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a")

        seen = set()

        for link in links:

            title = link.get_text(strip=True)

            href = link.get("href")

            if not title:
                continue

            if len(title) < 15:
                continue

            if title in seen:
                continue

            seen.add(title)

            detail_url = urljoin(BASE_URL, href)

            pdf_url = find_pdf(detail_url)

            results.append(
                {
                    "Source": "BAM",
                    "Titre": title,
                    "Date": extract_date(title),
                    "Lien": detail_url,
                    "PDF": pdf_url,
                }
            )

            if len(results) >= limit:
                break

    except Exception as e:

        print(f"BAM ERROR : {e}")

    return results


def find_pdf(page_url):

    try:

        response = requests.get(
            page_url,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for link in soup.find_all("a"):

            href = link.get("href")

            if href and ".pdf" in href.lower():

                return urljoin(
                    BASE_URL,
                    href
                )

    except Exception:

        return ""

    return ""
