from collector.mangodb import news_collection

print("Finding duplicates...")
pipeline = [
    {"$group": {"_id": "$url", "id": {"$first": "$_id"}, "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]

duplicates = list(news_collection.aggregate(pipeline))
print(f"Found {len(duplicates)} duplicate URLs to clean.")

for doc in duplicates:
    url_to_clean = doc["_id"]
    keep_id = doc["id"]
    # Delete all documents matching this URL except the one we want to keep
    result = news_collection.delete_many({
        "url": url_to_clean, 
        "_id": {"$ne": keep_id}
    })
    print(f"Cleaned URL: {url_to_clean} (Removed {result.deleted_count} duplicates)")

print("Database cleanup complete!")