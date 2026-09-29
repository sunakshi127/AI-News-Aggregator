import json

FILE_PATH = "mailer/subscribers.json"


def get_subscribers():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def add_subscriber(email):
    subscribers = get_subscribers()

    if email not in subscribers:
        subscribers.append(email)

        with open(FILE_PATH, "w") as f:
            json.dump(subscribers, f)

        return True

    return False