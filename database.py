from pathlib import Path
from dataclasses import dataclass
import sqlite3

BASE_DIR = Path(__file__).parent
filepath = BASE_DIR / "files/time_think.db"


@dataclass(frozen=True, slots=True)
class Request:
    query: str
    param: tuple[str, ...]


def connect_db(request: Request) -> sqlite3.Cursor:
    with sqlite3.connect(filepath) as connect:
        cursor = connect.cursor()
        return cursor.execute(request.query, request.param)
