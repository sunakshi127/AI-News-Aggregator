from fastapi import APIRouter

from collector.mangodb import news_collection
from collector.llm import send_to_llm


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# ---------------------------------
# AI SUMMARY
# ---------------------------------

@router.get("/summary")
def ai_summary():

    try:

        articles = list(
            news_collection.find(
                {},
                {"_id": 0}
            ).limit(10)
        )

        if not articles:

            return {
                "message": "No articles found in MongoDB"
            }

        result = send_to_llm(
            articles
        )

        return {
            "count": len(articles),
            "summary": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }