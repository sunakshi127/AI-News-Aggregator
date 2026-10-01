from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from collector.aggregator import get_all_news
from pydantic import BaseModel
from mailer.sender import send_news_email
from mailer.subscriber_store import add_subscriber, get_subscribers

app = FastAPI()


# ---------------------------------
# CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://ai-news-aggregator-banjara1.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------
# HOME
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "AI News Aggregator API is running"
    }


# ---------------------------------
# GET NEWS
# ---------------------------------

@app.get("/news")
def get_news():

    news = get_all_news()

    return {
        "count": len(news),
        "articles": news
    }
class SubscribeRequest(BaseModel):
    email: str


@app.post("/subscribe")
def subscribe(data: SubscribeRequest):
    added = add_subscriber(data.email)
    return {"success": added}


@app.post("/send-digest")
def send_digest():
    news = get_all_news()
    subscribers = get_subscribers()

    sent_count = 0

    for email in subscribers:
        if send_news_email(email, news):
            sent_count += 1

    return {"sent_to": sent_count}