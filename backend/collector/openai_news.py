import feedparser
from news_source import create_article

def get_openai_news():

    rss_url = "https://openai.com/news/rss.xml"

    feed = feedparser.parse(rss_url)

    news = []

    for entry in feed.entries:

        news.append(
    create_article(
        source="OpenAI",
        source_type="article",
        title=entry.get("title", ""),
        description=entry.get("summary", ""),
        published_at=entry.get("published", ""),
        url=entry.get("link", "")
    )
)

    return news


if __name__ == "__main__":

    news = get_openai_news()

    print("\nOpenAI News")
    print("=" * 60)

    print("Total articles:", len(news))

    for article in news[:20]:

        print("\nTitle:", article["title"])
        print("Published:", article["published_at"])
        print("URL:", article["url"])
        print("-" * 60)