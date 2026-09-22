import feedparser

RSS_URL = "https://www.oecd.org/newsroom/rss/"


def get_oecd_documents():

    docs = []

    try:

        feed = feedparser.parse(RSS_URL)

        for entry in feed.entries:

            docs.append(
                {
                    "Source": "OCDE",
                    "Titre": entry.get("title", ""),
                    "Date": entry.get("published", ""),
                    "Lien": entry.get("link", ""),
                    "PDF": ""
                }
            )

        print(
            f"OCDE: {len(docs)} documents"
        )

        return docs

    except Exception as e:

        print(
            f"OCDE ERROR: {e}"
        )

        return []
