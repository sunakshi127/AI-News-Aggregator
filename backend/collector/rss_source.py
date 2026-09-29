import feedparser

from news_source import create_article


# ---------------------------------
# RSS SOURCES
# ---------------------------------

RSS_SOURCES = {

    "TechCrunch":
        "https://techcrunch.com/feed/",

    "MIT Technology Review":
        "https://www.technologyreview.com/feed/",

    "VentureBeat":
        "https://venturebeat.com/feed/",

    "The Verge AI":
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",

    "Google AI":
        "https://blog.google/technology/ai/rss/"
}


# ---------------------------------
# GET RSS NEWS
# ---------------------------------

def get_rss_news():

    all_news = []

    # Loop through every RSS source
    for source_name, feed_url in RSS_SOURCES.items():

        print(
            f"\nFetching RSS: {source_name}"
        )

        try:

            # Read RSS feed
            feed = feedparser.parse(feed_url)

            # Get posts/articles
            posts = feed.entries

            print(
                "Posts found:",
                len(posts)
            )

            # Take first 10 articles
            for entry in posts[:10]:

                article = create_article(

                    source=source_name,

                    source_type="article",

                    title=entry.get(
                        "title",
                        ""
                    ),

                    description=entry.get(
                        "summary",
                        ""
                    ),

                    published_at=entry.get(
                        "published",
                        ""
                    ),

                    url=entry.get(
                        "link",
                        ""
                    ),

                    channel=""
                )

                all_news.append(article)

        except Exception as e:

            print(
                f"RSS error for {source_name}:",
                e
            )

    return all_news


# ---------------------------------
# TEST
# ---------------------------------

if __name__ == "__main__":

    news = get_rss_news()

    print("\n================================")
    print("TOTAL RSS ARTICLES:", len(news))
    print("================================")

    for article in news:

        print("\n-----------------------------")

        print(
            "Source:",
            article["source"]
        )

        print(
            "Title:",
            article["title"]
        )

        print(
            "Published:",
            article["published_at"]
        )

        print(
            "URL:",
            article["url"]
        )