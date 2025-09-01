import csv
from pathlib import Path
import uuid


def choose_name(name: str, filepath: Path) -> str | None:
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        if name in [row["username"] for row in reader]:
            return None
        return name


def register(username: str, password: str, filepath: Path) -> None:
    user_id = uuid.uuid4()
    with open(filepath, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, username, password])
