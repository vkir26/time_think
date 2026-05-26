import uuid
from app.database import connect_db, Request
from auth.config import peppered_password
from argon2 import PasswordHasher


def name_is_exist(name: str) -> bool:
    request = Request(
        query=""" SELECT username FROM users WHERE username = ?; """,
        param=(name,),
    )
    return connect_db(request=request).fetchone() is not None


def register(username: str, password: str) -> str:
    user_id = str(uuid.uuid4())
    ph = PasswordHasher()
    hashed_password = ph.hash(peppered_password(password))
    request = Request(
        query=""" INSERT INTO users (id, username, password) VALUES (?, ?, ?); """,
        param=(user_id, username, hashed_password),
    )
    connect_db(request=request)
    return user_id
