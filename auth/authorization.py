from auth.config import Account
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def authenticate(password: str, account: Account) -> str | None:
    ph = PasswordHasher()
    try:
        ph.verify(account.password, password)
        return account.uuid
    except VerifyMismatchError:
        return None
