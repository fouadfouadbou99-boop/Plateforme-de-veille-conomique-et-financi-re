import feedparser

RSS_URL = "https://www.imf.org/en/News/rss"

def get_imf_documents():

    docs = []

    try:

        feed = feedparser.parse(RSS_URL)

        print(
            f"FMI : {len(feed.entries)} documents"
        )

        for entry in feed.entries:

            docs.append(
                {
                    "Source": "FMI",
                    "Titre": entry.get(
                        "title", ""
                    ),
                    "Date": entry.get(
                        "published", ""
                    ),
                    "Lien": entry.get(
                        "link", ""
                    ),
                    "PDF": ""
                }
            )

    except Exception as e:

        print(
            f"FMI ERROR : {e}"
        )

    return docs
