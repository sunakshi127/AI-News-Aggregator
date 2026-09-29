# ---------------------------------
# IMPORT ALL SOURCES
# ---------------------------------

from collector.youtube import get_youtube_news
from collector.openai_news import get_openai_news
from collector.anthropic import get_anthropic_news
from collector.rss_source import get_rss_news
from collector.reddit_source import get_reddit_posts

# LLM
from collector.llm import send_to_llm


# ---------------------------------
# REMOVE DUPLICATES
# ---------------------------------

def remove_duplicates(news):

    unique_news = []
    seen_urls = set()

    for article in news:

        # Make sure article is a dictionary
        if not isinstance(article, dict):

            print(
                "Skipping invalid article:",
                article
            )

            continue

        # Get URL
        url = article.get("url", "")

        # Make sure URL is a string
        if not isinstance(url, str):
            url = str(url)

        url = url.strip()

        # ---------------------------------
        # If URL already exists → duplicate
        # ---------------------------------

        if url and url in seen_urls:
            continue

        # Remember URL
        if url:
            seen_urls.add(url)

        # Keep article
        unique_news.append(article)

    print("\n================================")
    print("DEDUPLICATION")
    print("================================")

    print(
        "Before:",
        len(news)
    )

    print(
        "After:",
        len(unique_news)
    )

    print(
        "Duplicates removed:",
        len(news) - len(unique_news)
    )

    return unique_news


# ---------------------------------
# COLLECT ALL NEWS
# ---------------------------------

def get_all_news():

    all_news = []

    # =================================
    # YOUTUBE
    # =================================

    print("\nFetching YouTube...")

    try:

        youtube_news = get_youtube_news()

        if isinstance(youtube_news, list):

            all_news.extend(youtube_news)

            print(
                "YouTube articles:",
                len(youtube_news)
            )

        else:

            print(
                "YouTube returned invalid data"
            )

    except Exception as e:

        print(
            "YouTube error:",
            e
        )


    # =================================
    # OPENAI
    # =================================

    print("\nFetching OpenAI...")

    try:

        openai_news = get_openai_news()

        if isinstance(openai_news, list):

            all_news.extend(openai_news)

            print(
                "OpenAI articles:",
                len(openai_news)
            )

        else:

            print(
                "OpenAI returned invalid data"
            )

    except Exception as e:

        print(
            "OpenAI error:",
            e
        )


    # =================================
    # ANTHROPIC
    # =================================

    print("\nFetching Anthropic...")

    try:

        anthropic_news = get_anthropic_news()

        if isinstance(anthropic_news, list):

            all_news.extend(anthropic_news)

            print(
                "Anthropic articles:",
                len(anthropic_news)
            )

        else:

            print(
                "Anthropic returned invalid data"
            )

    except Exception as e:

        print(
            "Anthropic error:",
            e
        )


    # =================================
    # RSS
    # =================================

    print("\nFetching RSS...")

    try:

        rss_news = get_rss_news()

        if isinstance(rss_news, list):

            all_news.extend(rss_news)

            print(
                "RSS articles:",
                len(rss_news)
            )

        else:

            print(
                "RSS returned invalid data"
            )

    except Exception as e:

        print(
            "RSS error:",
            e
        )


    # =================================
    # REDDIT
    # =================================

    print("\nFetching Reddit...")

    try:

        reddit_posts = get_reddit_posts()

        if isinstance(reddit_posts, list):

            all_news.extend(reddit_posts)

            print(
                "Reddit posts:",
                len(reddit_posts)
            )

        else:

            print(
                "Reddit returned invalid data"
            )

    except Exception as e:

        print(
            "Reddit error:",
            e
        )


    # =================================
    # REMOVE DUPLICATES
    # =================================

    all_news = remove_duplicates(all_news)


    # =================================
    # RETURN FINAL NEWS
    # =================================

    return all_news


# ---------------------------------
# MAIN
# ---------------------------------

if __name__ == "__main__":

    print("\n")
    print("================================")
    print("AI NEWS AGGREGATOR")
    print("================================")


    # ---------------------------------
    # STEP 1: COLLECT NEWS
    # ---------------------------------

    news = get_all_news()


    print("\n================================")
    print("COLLECTION COMPLETE")
    print("================================")

    print(
        "Total unique articles:",
        len(news)
    )


    # ---------------------------------
    # STEP 2: SHOW ARTICLES
    # ---------------------------------

    for i, article in enumerate(
        news,
        start=1
    ):

        print("\n-----------------------------")

        print(
            "Article:",
            i
        )

        print(
            "Source:",
            article.get(
                "source",
                ""
            )
        )

        print(
            "Type:",
            article.get(
                "source_type",
                ""
            )
        )

        print(
            "Title:",
            article.get(
                "title",
                ""
            )
        )

        print(
            "Published:",
            article.get(
                "published_at",
                ""
            )
        )

        print(
            "URL:",
            article.get(
                "url",
                ""
            )
        )


    # ---------------------------------
       # ---------------------------------
    # STEP 3: SEND TO LLM
    # ---------------------------------

    if news:

        print("\n================================")
        print("SENDING ARTICLES TO LLM")
        print("================================")

        try:

            result = send_to_llm(news)

            print("\n================================")
            print("LLM RESULT")
            print("================================")

            print(result)

        except Exception as e:

            print("\nLLM error:", e)

    else:

        print("\nNo valid articles found.")

    

    