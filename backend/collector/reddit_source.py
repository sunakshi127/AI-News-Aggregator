
import feedparser

from news_source import create_article


# ---------------------------------
# Reddit RSS sources
# ---------------------------------

REDDIT_SOURCES = {
    "r/artificial": "https://www.reddit.com/r/artificial/new/.rss",
    "r/MachineLearning": "https://www.reddit.com/r/MachineLearning/new/.rss",
    "r/OpenAI": "https://www.reddit.com/r/OpenAI/new/.rss",
    "r/LocalLLaMA": "https://www.reddit.com/r/LocalLLaMA/new/.rss"
}


# ---------------------------------
# Fetch Reddit posts
# ---------------------------------

def get_reddit_posts():

    all_posts = []

    for source_name, feed_url in REDDIT_SOURCES.items():

        print(f"\nFetching: {source_name}")

        try:

            feed = feedparser.parse(feed_url)

            if feed.bozo:
                print("RSS parsing warning:", feed.bozo_exception)

            posts = feed.entries

            print("Posts found:", len(posts))

            for post in posts[:10]:

                title = post.get(
                    "title",
                    ""
                )

                description = post.get(
                    "summary",
                    ""
                )

                published_at = post.get(
                    "published",
                    ""
                )

                url = post.get(
                    "link",
                    ""
                )

                article = create_article(
                    source=source_name,
                    source_type="post",
                    title=title,
                    description=description,
                    published_at=published_at,
                    url=url,
                    channel=""
                )

                all_posts.append(article)

        except Exception as e:

            print(
                f"Error fetching {source_name}:",
                e
            )

    return all_posts


# ---------------------------------
# Test
# ---------------------------------

if __name__ == "__main__":

    posts = get_reddit_posts()

    print("\n================================")
    print("Total Reddit posts:", len(posts))
    print("================================")

    for post in posts:

        print("\n-----------------------------")

        print("Source:", post["source"])

        print("Type:", post["source_type"])

        print("Title:", post["title"])

        print("Description:", post["description"])

        print("Published:", post["published_at"])

        print("URL:", post["url"])

