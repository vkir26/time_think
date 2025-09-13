from auth.config import Accounts


def authid(username: str, password: str) -> bool:
    for account in Accounts().get_accounts():
        if account["username"] == username and account["password"] == password:
            return True
    return False
