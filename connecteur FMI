import requests
from bs4 import BeautifulSoup


def get_imf_news():

    news = []

    try:

        url = "https://www.imf.org/en/News"

        response = requests.get(
            url,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        articles = soup.find_all("a")[:20]

        for article in articles:

            titre = article.get_text(strip=True)

            if titre:

                news.append(
                    {
                        "Source": "FMI",
                        "Titre": titre,
                        "Date": "",
                        "Lien": article.get("href", "")
                    }
                )

    except Exception as e:

        print(e)

    return news
