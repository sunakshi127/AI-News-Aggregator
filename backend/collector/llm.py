
import os
import json

from dotenv import load_dotenv
from google import genai


# ---------------------------------
# Load API key
# ---------------------------------

load_dotenv(r"C:\AI news aggregator\.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ---------------------------------
# Create Gemini client
# ---------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------
# Send articles to Gemini
# ---------------------------------
def send_to_llm(articles):

    # Remove MongoDB ObjectId before converting to JSON
    clean_articles = []

    for article in articles:

        if not isinstance(article, dict):
            continue

        clean_article = {
            key: value
            for key, value in article.items()
            if key != "_id"
        }

        clean_articles.append(clean_article)

    # Convert cleaned articles to JSON
    articles_text = json.dumps(
        clean_articles,
        indent=2,
        ensure_ascii=False,
        default=str
    )

    prompt = f"""
You are an AI news editor.

I collected the following news articles
from multiple sources.

Analyze them and select the most important
AI-related news.

For each selected article provide:

1. Title
2. Source
3. Short summary
4. Why it is important
5. URL

Rules:

- Do not invent information.
- Use only the information provided.
- Prefer important and useful AI news.
- Remove stories that are clearly repetitive.
- Keep the summaries concise.

News articles:

{articles_text}
"""

    try:

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        print("LLM API error:", e)

        return "" 

