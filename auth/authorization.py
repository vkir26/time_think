from auth.config import Account, PASSWORD_HASHER
from argon2.exceptions import VerifyMismatchError


def authenticate(password: str, account: Account) -> str | None:
    """Проверяет пароль пользователя.

    Args:
        password: пароль уже с pepper (через peppered_password).
        account: аккаунт из хранилища.
    Returns:
        uuid пользователя, если пароль верный;
        None, если пароль неверный.
    """
    try:
        PASSWORD_HASHER.verify(account.password, password)
        return account.uuid
    except VerifyMismatchError:
        return None
