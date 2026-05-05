from dataclasses import dataclass
from app.database import connect_db, Request


@dataclass(frozen=True, slots=True)
class Account:
    username: str
    password: str
    uuid: str


class AccountStorage:
    def __init__(self) -> None:
        pass

    def get_usernames(self) -> list[str]:
        request = Request(query=""" SELECT username FROM users """, param=())
        rows = connect_db(request=request).fetchall()
        return [row[0] for row in rows]

    def get_by_username(self, username: str) -> Account:
        request = Request(
            query=""" SELECT id, username, password FROM users WHERE username = ? """,
            param=(username,),
        )
        row = connect_db(request=request).fetchone()
        user_id, name, password = row
        return Account(username=name, password=password, uuid=user_id)
