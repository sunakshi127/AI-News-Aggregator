from apscheduler.schedulers.background import BackgroundScheduler

from collector.aggregator import get_all_news
from collector.ranker import rank_articles
from collector.mangodb import save_articles


# ---------------------------------
# NEWS COLLECTION JOB
# ---------------------------------

def collect_news():

    print("\n================================")
    print("SCHEDULER: COLLECTING NEWS")
    print("================================")

    try:

        # 1. Collect news
        news = get_all_news()

        print(
            "Articles collected:",
            len(news)
        )
         # Check collected data
        if news is None:
            print("ERROR: get_all_news() returned None")
            return
        # 2. Rank news
        ranked_news = rank_articles(news)

        print("Ranker returned:", type(ranked_news))

        if ranked_news is None:
          print("ERROR: rank_articles() returned None")
          return

        print(
               "Articles ranked:",
                len(ranked_news)
)

        print("Calling save_articles()...") # 3. Save to MongoDB
        save_articles(ranked_news)

        print(
            "News collection completed!"
        )

    except Exception as e:

        print(
            "Scheduler error:",
            e
        )


# ---------------------------------
# CREATE SCHEDULER
# ---------------------------------

scheduler = BackgroundScheduler()


# ---------------------------------
# RUN EVERY 1 HOUR
# ---------------------------------

scheduler.add_job(
    collect_news,
    "interval",
    minutes=10,
    id="news_collection_job",
    replace_existing=True
)


# ---------------------------------
# START SCHEDULER
# ---------------------------------

def start_scheduler():

    if not scheduler.running:

        scheduler.start()

        print(
            "News scheduler started!"
        )
        collect_news() 

# ---------------------------------
# STOP SCHEDULER
# ---------------------------------

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "News scheduler stopped!"
        )