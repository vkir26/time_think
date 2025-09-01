import csv
from pathlib import Path
from dataclasses import dataclass


def read_database(filepath: Path) -> list[dict[str, str]]:
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        accounts = list(reader)
    return accounts


@dataclass(frozen=True, slots=True)
class Accounts:
    USERNAMES: list[str]


def get_usernames(filepath: Path) -> Accounts:
    accounts = read_database(filepath)
    users = [user["username"] for user in accounts]
    return Accounts(users)


@dataclass(frozen=True, slots=True)
class Account:
    ID: str


def authid(filepath: Path, username: str, password: str) -> Account | None:
    accounts = read_database(filepath)
    for account in accounts:
        if account["username"] == username and account["password"] == password:
            return Account(account["uuid"])
    return None
