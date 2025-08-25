import csv
from enum import StrEnum
from pathlib import Path

filename = Path("auth/users.csv")


class Message(StrEnum):
    TITLE = "[АВТОРИЗАЦИЯ]"
    ACCOUNT_SELECTION = "Выберете аккаунт для входа:"
    ENTRY_USERNAME = "Введите имя пользователя: "
    ENTRY_PASSWORD = "Введите пароль: "
    INCORRECT_PASSWORD = "Имя пользователя или пароль указаны неверно"
    SUCCESS_AUTHORIZATION = "Успешная авторизация!"


def get_uuid(users: list[dict[str, str]]) -> str:
    username = input(Message.ENTRY_USERNAME).strip()
    password = input(Message.ENTRY_PASSWORD).strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(Message.SUCCESS_AUTHORIZATION)
            return user["uuid"]
    print(Message.INCORRECT_PASSWORD)
    return get_uuid(users)


def account() -> str:
    users = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        print(f"{Message.TITLE}\n{Message.ACCOUNT_SELECTION}")
        for number, row in enumerate(reader, 1):
            print(f"{number}. {row['username']}")
            users.append(row)

        return get_uuid(users)
