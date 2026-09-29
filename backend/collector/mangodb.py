import os

from dotenv import load_dotenv
from pymongo import MongoClient


# ---------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------

load_dotenv(r"C:\AI news aggregator\.env")

MONGODB_URI = os.getenv("MONGODB_URI")

print("MongoDB URI loaded:", MONGODB_URI is not None)


# ---------------------------------
# CONNECT TO MONGODB
# ---------------------------------

client = MongoClient(MONGODB_URI)

db = client["ai_news_aggregator"]

news_collection = db["news"]


# ---------------------------------
# TEST CONNECTION
# ---------------------------------

def test_connection():

    try:

        client.admin.command("ping")

        print("MongoDB connected successfully!")

    except Exception as e:

        print("MongoDB connection error:", e)

# SAVE ARTICLES
# ---------------------------------

def save_articles(articles):

    if not articles:
        print("No articles to save.")
        return

    saved_count = 0
    skipped_count = 0

    for article in articles:

        # -----------------------------
        # CHECK ARTICLE
        # -----------------------------

        if not isinstance(article, dict):
            print("Skipping invalid article:", article)
            continue

        # -----------------------------
        # GET URL
        # -----------------------------

        url = article.get("url", "")

        if not isinstance(url, str):
            url = str(url)

        url = url.strip()

        # -----------------------------
        # URL REQUIRED
        # -----------------------------

        if not url:

            print(
                "Skipping article without URL:",
                article.get("title", "")
            )

            continue

        # -----------------------------
        # PYTHON DUPLICATE CHECK
        # -----------------------------

        existing_article = news_collection.find_one(
            {"url": url}
        )

        if existing_article:

            skipped_count += 1
            continue

        # -----------------------------
        # INSERT NEW ARTICLE
        # -----------------------------

        try:

            news_collection.insert_one(article)

            saved_count += 1

        except Exception as e:

            # MongoDB unique index can catch
            # a duplicate inserted at the same time

            if "duplicate key" in str(e).lower():

                skipped_count += 1

            else:

                print(
                    "Error saving article:",
                    e
                )

    # -----------------------------
    # RESULT
    # -----------------------------

    print("\n================================")
    print("MONGODB SAVE RESULT")
    print("================================")

    print(
        "New articles saved:",
        saved_count
    )

    print(
        "Duplicate articles skipped:",
        skipped_count
    )