import feedparser

class RSSClient:

    @staticmethod
    def fetch(url):

        feed = feedparser.parse(url)

        articles = []

        for entry in feed.entries:

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(
                    entry,
                    "published",
                    None
                )
            })

        return articles
