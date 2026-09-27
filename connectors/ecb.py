import feedparser

RSS_URL = (
    "https://www.ecb.europa.eu/rss/press.html"
)

def get_ecb_documents():

    docs = []

    try:

        feed = feedparser.parse(
            RSS_URL
        )

        for entry in feed.entries:

            docs.append(
                {
                    "Source": "BCE",
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

        print(
            f"BCE : {len(docs)} documents"
        )

    except Exception as e:

        print(
            f"BCE ERROR: {e}"
        )

    return docs
