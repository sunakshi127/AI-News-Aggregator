# ---------------------------------
# NEWS RANKER
# ---------------------------------

def rank_articles(articles):

    ranked_articles = []

    for article in articles:

        # Skip invalid data
        if not isinstance(article, dict):
            continue

        score = 0

        title = article.get("title", "").lower()
        description = article.get("description", "").lower()

        text = title + " " + description

        # ---------------------------------
        # KEYWORDS
        # ---------------------------------

        important_keywords = [
            "artificial intelligence",
            "ai",
            "machine learning",
            "openai",
            "chatgpt",
            "gemini",
            "claude",
            "anthropic",
            "google ai",
            "llm",
            "large language model",
            "generative ai"
        ]

        # ---------------------------------
        # CALCULATE SCORE
        # ---------------------------------

        for keyword in important_keywords:

            if keyword in text:
                score += 1

        # ---------------------------------
        # EXTRA SCORE FOR IMPORTANT WORDS
        # ---------------------------------

        high_priority_words = [
            "launch",
            "released",
            "release",
            "new model",
            "breakthrough",
            "update",
            "acquisition",
            "funding",
            "research",
            "announces",
            "announcement"
        ]

        for keyword in high_priority_words:

            if keyword in text:
                score += 2

        # Store score inside article
        article["score"] = score

        ranked_articles.append(article)

    # ---------------------------------
    # SORT BY SCORE
    # ---------------------------------

    ranked_articles.sort(
        key=lambda article: article.get("score", 0),
        reverse=True
    )

    return ranked_articles


# ---------------------------------
# TEST
# ---------------------------------

if __name__ == "__main__":

    test_articles = [

        {
            "title": "OpenAI releases a new AI model",
            "description": "The new model improves artificial intelligence performance.",
            "source": "TechCrunch",
            "url": "https://example.com/1"
        },

        {
            "title": "Weather forecast for tomorrow",
            "description": "Weather conditions are expected to change.",
            "source": "Example",
            "url": "https://example.com/2"
        },

        {
            "title": "Google announces new Gemini AI update",
            "description": "The new AI model brings improvements to generative AI.",
            "source": "Google AI",
            "url": "https://example.com/3"
        }
    ]

    ranked = rank_articles(test_articles)

    print("\n================================")
    print("RANKED ARTICLES")
    print("================================")

    for article in ranked:

        print("\n-----------------------------")

        print("Score:", article["score"])
        print("Title:", article["title"])
        print("Source:", article["source"])