import csv
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
import functools

datafile = Path("auth/users.csv")


def create_datafile() -> None:
    with open(datafile, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(("uuid", "username", "password"))


@dataclass(frozen=True, slots=True)
class Account:
    username: str
    password: str
    uuid: str


def caching[**P, T](func: Callable[P, list[T]]) -> Callable[P, list[T]]:
    cache = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[T]:
        key = tuple(func(*args, **kwargs))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


class AccountStorage:
    def __init__(self) -> None:
        self.accounts = self.get_accounts()

    @caching
    def get_accounts(self) -> list[Account]:
        with open(datafile, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            self.accounts = [Account(**account) for account in reader]
        return self.accounts

    def get_usernames(self) -> list[str]:
        return [account.username for account in self.accounts]

    def get_user_id(self, username: str) -> str | None:
        for account in self.accounts:
            if account.username == username:
                return account.uuid
        return None
