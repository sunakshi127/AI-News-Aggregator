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

client = MongoClient(
    MONGODB_URI,
    tls=True,
    serverSelectionTimeoutMS=10000
)

# ---------------------------------
# DATABASE
# ---------------------------------

db = client["ai_news_aggregator"]

# ---------------------------------
# NEWS COLLECTION
# ---------------------------------

news_collection = db["news"]


# ---------------------------------
# TEST CONNECTION
# ---------------------------------

def test_connection():
    try:
        result = client.admin.command("ping")
        print("MongoDB connection successful!")
        print(result)
        return True

    except Exception as e:
        print("MongoDB connection failed:")
        print(e)
        return False