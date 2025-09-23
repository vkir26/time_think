from auth.config import AccountStorage


def authenticate(user_id: str, password: str) -> bool:
    for account in AccountStorage().get_accounts():
        if account.uuid == user_id and account.password == password:
            return True
    return False
