import csv
from pathlib import Path
from enum import StrEnum
from auth.authorization import account
import uuid

filename = Path("auth/users.csv")


class Message(StrEnum):
    TITLE = "[РЕГИСТРАЦИЯ]"
    INPUT_NAME = "Введите имя: "
    NAME_EXISTS = "Данное имя уже существует"
    INPUT_PASS = "Придумайте пароль: "
    SUCCESS_REGISTER = "Успешная регистрация!"


def choose_name(name: str) -> str | None:
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if name in [row["username"] for row in reader]:
            print(Message.NAME_EXISTS)
            return None
        return name


def registration() -> str:
    print(Message.TITLE)
    username = choose_name(input(Message.INPUT_NAME).strip())

    if username is None:
        return registration()
    else:
        password = input(Message.INPUT_PASS).strip()
        user_id = uuid.uuid4()

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([username, password, user_id])
            print(Message.SUCCESS_REGISTER)
        return account()
