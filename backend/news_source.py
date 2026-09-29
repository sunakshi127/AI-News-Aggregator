import os
import requests
from dotenv import load_dotenv


# ---------------------------------
# Common article format
# ---------------------------------

def create_article(
    source,
    source_type,
    title,
    description="",
    published_at="",
    url="",
    channel=""
):
    return {
        "source": source,
        "source_type": source_type,
        "title": title,
        "description": description,
        "published_at": published_at,
        "url": url,
        "channel": channel
    }


# ---------------------------------
# Load .env
# ---------------------------------

load_dotenv(r"C:\AI news aggregator\.env")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print("API key loaded:", NEWS_API_KEY is not None)


# ---------------------------------
# Fetch news from NewsAPI
# ---------------------------------

def get_news():

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "artificial intelligence OR AI OR machine learning",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("NewsAPI request failed")
            print(response.text)
            return []

        data = response.json()

        articles = []

        for article in data.get("articles", []):

            news = create_article(
                source=article.get(
                    "source", {}
                ).get("name", "Unknown"),

                source_type="article",

                title=article.get(
                    "title", ""
                ),

                description=article.get(
                    "description", ""
                ),

                published_at=article.get(
                    "publishedAt", ""
                ),

                url=article.get(
                    "url", ""
                )
            )

            articles.append(news)

        return articles

    except requests.exceptions.RequestException as e:

        print("Request error:", e)
        return []

    except Exception as e:

        print("Error:", e)
        return []


# ---------------------------------
# Test
# ---------------------------------

if __name__ == "__main__":

    news_articles = get_news()

    print("\nNumber of articles:", len(news_articles))

    for article in news_articles:

        print("\n-----------------------------")

        print("Source:", article["source"])
        print("Type:", article["source_type"])
        print("Title:", article["title"])
        print("Description:", article["description"])
        print("Published:", article["published_at"])
        print("URL:", article["url"])
        print("Channel:", article["channel"])