import csv
from auth.config import datafile, AccountStorage
import uuid


def name_is_exist(name: str) -> bool:
    accounts = AccountStorage().get_usernames()
    return name in accounts


def register(username: str, password: str) -> uuid.UUID:
    user_id = uuid.uuid4()
    with open(datafile, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, username, password])
    return user_id
