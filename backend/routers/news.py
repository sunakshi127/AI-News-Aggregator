from fastapi import APIRouter

from collector.mangodb import news_collection


# ---------------------------------
# CREATE ROUTER
# ---------------------------------

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


# ---------------------------------
# GET ALL NEWS
# ---------------------------------

@router.get("/")
def get_news():

    articles = list(
        news_collection.find(
            {},
            {"_id": 0}
        ).limit(20)
    )

    return {
        "count": len(articles),
        "articles": articles
    }


# ---------------------------------
# GET LATEST NEWS
# ---------------------------------

@router.get("/latest")
def get_latest_news():

    articles = list(
        news_collection.find(
            {},
            {"_id": 0}
        )
        .sort("published_at", -1)
        .limit(10)
    )

    return {
        "count": len(articles),
        "articles": articles
    }