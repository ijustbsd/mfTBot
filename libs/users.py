from pathlib import Path
import json

PATH = str(Path(__file__).parents[1]) + '/data/users.json'


def add_schedule(user_id, qual, course, group):
    with open(PATH) as json_file:
        users = json.load(json_file)
    if not load_user(user_id):
        users[str(user_id)] = ({
            "qual": qual,
            "course": course,
            "group": group
        },)
    else:
        new_schedule = {
            "qual": qual,
            "course": course,
            "group": group
        }
        user = users[str(user_id)]
        if new_schedule in user or len(user) > 4:
            return
        out = tuple(user) + (new_schedule,)
        users[str(user_id)] = out
    with open(PATH, 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False, indent=4)


def del_schedule(user_id, num):
    with open(PATH) as json_file:
        users = json.load(json_file)
    user = tuple(users[str(user_id)])
    out = tuple(i for i in user if i != user[int(num)])
    users[str(user_id)] = out
    with open(PATH, 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False)


def load_user(user_id):
    user_id = str(user_id)
    with open(PATH) as json_file:
        users = json.load(json_file)
    return users[user_id] if user_id in users else False
