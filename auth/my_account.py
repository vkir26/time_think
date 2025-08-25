import csv
from pathlib import Path
from enum import StrEnum, IntEnum
from auth.register import registration
from auth.authorization import account

filename = Path("auth/users.csv")


class Menu(IntEnum):
    AUTHORIZATION = 1
    REGISTER = 2


class Message(StrEnum):
    AUTHORIZATION = "Авторизоваться"
    REGISTER = "Зарегистрироваться"
    INFO = "Выберете что необходимо сделать:"


def create_csv() -> None:
    if not filename.exists():
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(("username", "password", "uuid"))


def identification() -> str | None:
    create_csv()
    select_menu = Menu.REGISTER

    print(
        f"{Message.INFO}\n"
        f"{Menu.AUTHORIZATION}. {Message.AUTHORIZATION}\n"
        f"{Menu.REGISTER}. {Message.REGISTER}\n"
    )
    if select_menu == Menu.REGISTER:
        return registration()
    if select_menu == Menu.AUTHORIZATION:
        return account()
    return None
