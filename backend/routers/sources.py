from fastapi import APIRouter

from collector.youtube import get_youtube_news
from collector.openai_news import get_openai_news
from collector.anthropic import get_anthropic_news
from collector.rss_source import get_rss_news
from collector.reddit_source import get_reddit_posts


router = APIRouter(
    prefix="/sources",
    tags=["Sources"]
)


# ---------------------------------
# YOUTUBE
# ---------------------------------

@router.get("/youtube")
def youtube_news():

    try:

        articles = get_youtube_news()

        return {
            "source": "YouTube",
            "count": len(articles),
            "articles": articles
        }

    except Exception as e:

        return {
            "source": "YouTube",
            "error": str(e)
        }


# ---------------------------------
# OPENAI
# ---------------------------------

@router.get("/openai")
def openai_news():

    try:

        articles = get_openai_news()

        return {
            "source": "OpenAI",
            "count": len(articles),
            "articles": articles
        }

    except Exception as e:

        return {
            "source": "OpenAI",
            "error": str(e)
        }


# ---------------------------------
# ANTHROPIC
# ---------------------------------

@router.get("/anthropic")
def anthropic_news():

    try:

        articles = get_anthropic_news()

        return {
            "source": "Anthropic",
            "count": len(articles),
            "articles": articles
        }

    except Exception as e:

        return {
            "source": "Anthropic",
            "error": str(e)
        }


# ---------------------------------
# RSS
# ---------------------------------

@router.get("/rss")
def rss_news():

    try:

        articles = get_rss_news()

        return {
            "source": "RSS",
            "count": len(articles),
            "articles": articles
        }

    except Exception as e:

        return {
            "source": "RSS",
            "error": str(e)
        }


# ---------------------------------
# REDDIT
# ---------------------------------

@router.get("/reddit")
def reddit_news():

    try:

        articles = get_reddit_posts()

        return {
            "source": "Reddit",
            "count": len(articles),
            "articles": articles
        }

    except Exception as e:

        return {
            "source": "Reddit",
            "error": str(e)
        }