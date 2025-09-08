from auth.config import Accounts
from dataclasses import dataclass


@dataclass
class Account:
    id: str | None


# def authid(username: str, password: str) -> Account | None:
#     accounts = Accounts().get_accounts()
#     for account in accounts:
#         if account["username"] == username and account["password"] == password:
#             return Account(account["uuid"])
#     return None


def authid(username: str, password: str) -> Account:
    accounts = Accounts().get_accounts()
    for account in accounts:
        if account["username"] == username and account["password"] == password:
            return Account(account["uuid"])
    return Account(None)
