import csv
from messages import RegisterMessage
from dataclasses import dataclass, field
from pathlib import Path

datafile = Path("auth/users.csv")


def create_datafile() -> None:
    with open(datafile, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(("uuid", "username", "password"))
        writer.writerow([None, RegisterMessage.NEW_USER, None])


@dataclass(slots=True)
class Accounts:
    accounts: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        with open(datafile, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            self.accounts = list(reader)

    def get_accounts(self) -> list[dict[str, str]]:
        return self.accounts

    def get_usernames(self) -> list[str]:
        return [user["username"] for user in self.accounts]
