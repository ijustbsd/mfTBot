from pathlib import Path
import json

PATH = str(Path(__file__).parents[1]) + '/data/stats.json'


def save_stats(users, messages):
    stats = {
        "users": int(users),
        "messages": int(messages)
    }
    with open(PATH, 'w') as json_file:
        json.dump(stats, json_file, ensure_ascii=False)


def load_stats():
    with open(PATH) as json_file:
        stats = json.load(json_file)
    return (stats["users"], stats["messages"])


def update_stats(new_user=0, new_msg=0):
    users, messages = load_stats()
    save_stats(users + new_user, messages + new_msg)
