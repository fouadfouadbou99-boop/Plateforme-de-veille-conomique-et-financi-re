import feedparser

RSS_URL = "https://www.imf.org/en/Publications/RSS"


def get_imf_documents():

    docs = []

    try:

        feed = feedparser.parse(
            RSS_URL
        )

        for entry in feed.entries:

            docs.append(
                {
                    "Source": "FMI",
                    "Titre": entry.get("title", ""),
                    "Date": entry.get("published", ""),
                    "Lien": entry.get("link", ""),
                    "PDF": ""
                }
            )

        return docs

    except Exception as e:

        print(
            f"IMF ERROR: {e}"
        )

        return []
