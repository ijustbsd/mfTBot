from pathlib import Path
import json

PATH = str(Path(__file__).parents[1]) + '/data/users.json'


def add_user(user_id, course, group):
    with open(PATH) as json_file:
        users = json.load(json_file)
    users[str(user_id)] = [{
        "qual": "qual",
        "course": course,
        "group": group
    }]
    with open(PATH, 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False)


def add_schedule(user_id, course, group):
    with open(PATH) as json_file:
        users = json.load(json_file)
    users[str(user_id)].append({
        "qual": "qual",
        "course": course,
        "group": group
    })
    with open(PATH, 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False)


def del_schedule(user_id, qual, course, group):
    with open(PATH) as json_file:
        users = json.load(json_file)
    for u in users[str(user_id)]:
        if u.values() == [str(qual), str(course), str(group)]:
            users[str(user_id)].pop(users[str(user_id)].index(u))
    with open(PATH, 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False)


def load_user(user_id):
    user_id = str(user_id)
    with open(PATH) as json_file:
        users = json.load(json_file)
    return users[user_id] if user_id in users else False
