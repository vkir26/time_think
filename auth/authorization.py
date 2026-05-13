from auth.config import AccountStorage


def authenticate(username: str, password: str | int) -> str | None:
    account = AccountStorage().get_by_username(username=username)
    if account.password == password:
        return account.uuid
    return None
