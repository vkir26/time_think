from auth.config import AccountStorage, peppered_password
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def authenticate(username: str, password: str) -> str | None:
    account = AccountStorage().get_by_username(username=username)
    ph = PasswordHasher()
    hashed_password = peppered_password(password)
    try:
        ph.verify(account.password, hashed_password)
        return account.uuid
    except VerifyMismatchError:
        return None
