import datetime
from pathlib import Path
import json

PATH = str(Path(__file__).parents[1]) + '/data/stats.json'


def save_stats(users, messages, type, user_id=0, user_msg=0):
    full_stats = load_stats()
    if type == 0:
        stats = full_stats["all_stats"]
        stats["users"] = int(users)
        stats["messages"] = int(messages)
    elif type == 1:
        stats = full_stats["today_stats"]
        stats["users"] = int(users)
        stats["messages"] = int(messages)
    elif type == 2:
        stats = full_stats["requests"]
        days = full_stats["days"]
        date = datetime.date.today()
        days_today = date.toordinal()
        if days != days_today:
            stats.clear()
        stats[str(user_id)] = int(user_msg)
        full_stats["days"] = days_today
    with open(PATH, 'w') as json_file:
        json.dump(full_stats, json_file, ensure_ascii=False)


def load_stats():
    with open(PATH) as json_file:
        stats = json.load(json_file)
    return stats


def update_stats(user_id, new_user=0, new_msg=0):
    update_all(new_user, new_msg)
    update_today(new_user, new_msg)
    update_reqs(user_id, new_user)


def update_all(new_user, new_msg):
    stats = load_stats()["all_stats"]
    users, messages = (int(stats["users"]), int(stats["messages"]))
    save_stats(users + new_user, messages + new_msg, 0)


def update_today(new_user, new_msg):
    stats = load_stats()["today_stats"]
    users, messages = (
        int(stats["users"]),
        int(stats["messages"])
    )
    days = load_stats()["days"]
    date = datetime.date.today()
    days_today = date.toordinal()
    if days == days_today:
        save_stats(users + new_user, messages + new_msg, 1)
    else:
        save_stats(new_user, new_msg, 1)


def update_reqs(user_id, new_user):
    stats = load_stats()["requests"]
    count_msg = stats.get(str(user_id)) or 0
    b = not bool(new_user)
    save_stats(0, 0, 2, user_id=user_id, user_msg=int(count_msg) + int(b))
