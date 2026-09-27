import feedparser

RSS_URL = (
    "https://www.banque-france.fr/rss.xml"
)

def get_bdf_documents():

    docs = []

    try:

        feed = feedparser.parse(
            RSS_URL
        )

        for entry in feed.entries:

            docs.append(
                {
                    "Source": "Banque de France",
                    "Titre": entry.get(
                        "title",
                        ""
                    ),
                    "Date": entry.get(
                        "published",
                        ""
                    ),
                    "Lien": entry.get(
                        "link",
                        ""
                    ),
                    "PDF": ""
                }
            )

    except Exception as e:

        print(
            f"BDF ERROR: {e}"
        )

    return docs
