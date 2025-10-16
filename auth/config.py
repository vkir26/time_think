import csv
from dataclasses import dataclass
from pathlib import Path

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


class AccountStorage:
    if not datafile.exists():
        create_datafile()

    def __init__(self) -> None:
        self.accounts = self.get_accounts()

    def get_accounts(self) -> list[Account]:
        with open(datafile, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            self.accounts = [Account(**account) for account in reader]
        return self.accounts

    def get_usernames(self) -> list[str]:
        return [account.username for account in self.accounts]

    def get_by_username(self, username: str) -> str | None:
        for account in self.accounts:
            if account.username == username:
                return account.uuid
        return None
