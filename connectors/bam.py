import requests
from bs4 import BeautifulSoup


def get_bam_news():

    news = []

    try:

        url = "https://www.bkam.ma"

        response = requests.get(
            url,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a")

        for link in links[:20\]:

            titre = link.get_text(strip=True)

            if len(titre) > 10:

                news.append(
                    {
                        "Source": "BAM",
                        "Titre": titre,
                        "Date": "",
                        "Lien": link.get("href", "")
                    }
                )

    except Exception as e:

        print(e)

    return news
