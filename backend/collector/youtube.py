import os
from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from news_source import create_article


# Find .env in the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# Get YouTube API key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

print("API key loaded:", bool(YOUTUBE_API_KEY))


if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env file")


# Connect to YouTube API
youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


def get_youtube_news(query="AI news", max_results=10):

    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        order="date",
        maxResults=max_results
    ).execute()

    news = []

    for item in response["items"]:

        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        news.append(
    create_article(
        source="YouTube",
        source_type="video",
        title=snippet["title"],
        description=snippet["description"],
        published_at=snippet["publishedAt"],
        url=f"https://www.youtube.com/watch?v={video_id}",
        channel=snippet["channelTitle"]
    )
)

    return news


# Test the collector
if __name__ == "__main__":

    news = get_youtube_news(
        query="artificial intelligence news",
        max_results=10
    )

    print("\nYouTube AI News\n")
    print("=" * 60)

    for article in news:

        print("Title:", article["title"])
        print("Channel:", article["channel"])
        print("Published:", article["published_at"])
        print("URL:", article["url"])
        print("-" * 60)