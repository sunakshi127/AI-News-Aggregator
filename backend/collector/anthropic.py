import requests
from bs4 import BeautifulSoup
from news_source import create_article

url = "https://www.anthropic.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_anthropic_news():

    news = []

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print("Status:", response.status_code)

        if response.status_code != 200:

            print("Anthropic request failed")
            return []

        # -----------------------------------------
        # Parse HTML
        # -----------------------------------------

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # -----------------------------------------
        # Find links from the news page
        # -----------------------------------------

        links = soup.find_all("a", href=True)

        seen_urls = set()

        for link in links:

            href = link.get("href", "")

            # Only process Anthropic news links
            if "/news/" not in href:
                continue

            # Convert relative URL to full URL
            if href.startswith("/"):
                article_url = "https://www.anthropic.com" + href
            else:
                article_url = href

            # Avoid duplicate articles
            if article_url in seen_urls:
                continue

            seen_urls.add(article_url)

            # -----------------------------------------
            # Extract title
            # -----------------------------------------

            title = link.get_text(
                " ",
                strip=True
            )

            if not title:
                continue

            # -----------------------------------------
            # Create common article format
            # -----------------------------------------

            article = create_article(
                source="Anthropic",
                source_type="article",
                title=title,
                description="",
                published_at="",
                url=article_url,
                channel=""
            )

            news.append(article)

        return news

    except requests.exceptions.RequestException as e:

        print("Request error:", e)

        return []

    except Exception as e:

        print("Error:", e)

        return []


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    news_articles = get_anthropic_news()

    print(
        "\nNumber of articles:",
        len(news_articles)
    )

    for article in news_articles[:10]:

        print("\n-----------------------------")

        print(
            "Source:",
            article["source"]
        )

        print(
            "Type:",
            article["source_type"]
        )

        print(
            "Title:",
            article["title"]
        )

        print(
            "Description:",
            article["description"]
        )

        print(
            "Published:",
            article["published_at"]
        )

        print(
            "URL:",
            article["url"]
        )