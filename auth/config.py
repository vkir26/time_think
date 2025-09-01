import csv
from pathlib import Path
from enum import StrEnum


class GetFile(StrEnum):
    FILEPATH = "auth/users.csv"


datafile = Path(GetFile.FILEPATH)


def create_datafile() -> None:
    with open(datafile, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(("uuid", "username", "password"))
