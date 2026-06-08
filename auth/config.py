import os
from dotenv import load_dotenv
from dataclasses import dataclass
from app.database import connect_db, Request
from datetime import datetime, timezone, timedelta
from jose import jwt

ALGORITHM = "HS256"


def jwt_secret_key() -> str:
    load_dotenv()
    jwt_key = os.environ["JWT_SECRET_KEY"]
    return jwt_key


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": user_id, "exp": expire}
    load_dotenv()
    jwt_data = str(
        jwt.encode(claims=payload, key=jwt_secret_key(), algorithm=ALGORITHM)
    )
    return jwt_data


def peppered_password(password: str) -> str:
    load_dotenv()
    pepper = os.environ["PASSWORD_PEPPER"]
    return password + pepper


@dataclass(frozen=True, slots=True)
class Account:
    username: str
    password: str
    uuid: str


class AccountStorage:
    def __init__(self) -> None:
        pass

    def get_usernames(self) -> list[str]:
        request = Request(
            query=""" SELECT username
                      FROM users """,
            param=(),
        )
        rows = connect_db(request=request).fetchall()
        return [row[0] for row in rows]

    def get_by_username(self, username: str) -> Account:
        request = Request(
            query=""" SELECT id, username, password
                      FROM users
                      WHERE username = ? """,
            param=(username,),
        )
        row = connect_db(request=request).fetchone()
        user_id, name, password = row
        return Account(username=name, password=password, uuid=user_id)
