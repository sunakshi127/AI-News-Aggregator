
import os

from dotenv import load_dotenv
from google import genai


# ---------------------------------
# Load .env
# ---------------------------------

load_dotenv(r"C:\AI news aggregator\.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(
    "API key loaded:",
    GEMINI_API_KEY is not None
)


# ---------------------------------
# Create Gemini client
# ---------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ---------------------------------
# Send test prompt
# ---------------------------------

response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain artificial intelligence in 3 simple sentences."
)


# ---------------------------------
# Print response
# ---------------------------------

print("\nGemini response:")
print(response.output_text)

