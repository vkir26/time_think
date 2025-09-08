import csv
from enum import Enum
from auth.config import datafile, Accounts
import uuid


class NameExists(Enum):
    EXIST = True
    NOT_EXIST = False


def name_is_exist(name: str) -> NameExists:
    accounts = Accounts().get_usernames()
    return NameExists(name in accounts)


def register(username: str, password: str) -> None:
    user_id = uuid.uuid4()
    with open(datafile, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, username, password])
