from collector.mangodb import db

subscribers_collection = db["subscribers"]


def get_subscribers():
    docs = subscribers_collection.find({}, {"_id": 0, "email": 1})
    return [doc["email"] for doc in docs]


def add_subscriber(email):
    existing = subscribers_collection.find_one({"email": email})

    if existing:
        return False

    subscribers_collection.insert_one({"email": email})
    return True