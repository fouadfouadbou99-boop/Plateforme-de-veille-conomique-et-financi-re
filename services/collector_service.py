from connectors.rss.rss_client import RSSClient

class CollectorService:

    def collect_all(self):

        news = []

        sources = [
            {
                "name": "OCDE",
                "rss": "https://www.oecd.org/rss/"
            }
        ]

        for source in sources:

            try:

                articles = RSSClient.fetch(
                    source["rss"]
                )

                news.extend(articles)

            except Exception as ex:

                print(ex)

        return news
