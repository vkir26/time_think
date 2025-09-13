from enum import IntEnum
from session import run
from messages import AccessMenuMessage, RegisterMessage, AuthMessage
from auth.config import datafile, create_datafile, Accounts
from auth.access_menu import menu_selector, AccessMenu
from auth.registration import register, name_is_exist
from auth.authorization import authid


def menu_selection() -> int:
    while True:
        try:
            select_menu = int(input(AccessMenuMessage.INPUT))
            menu = menu_selector(selected_menu=select_menu)
            break
        except ValueError:
            print(AccessMenuMessage.MENU_NOT_FOUND)
    return menu


def check_username(username: str) -> bool:
    match user := name_is_exist(username):
        case False:
            print(RegisterMessage.NAME_EXISTS)
    return user


def account_selection(usernames: list[str], select_index: str) -> int:
    if select_index.isdigit():
        return 1 <= int(select_index) < len(usernames) or int(select_index) == 0
    return False


def authentication(username: str, password: str) -> bool:
    match identification := authid(username=username, password=password):
        case True:
            print(AuthMessage.SUCCESS_AUTHORIZATION)
        case _:
            print(AuthMessage.INCORRECT_PASSWORD)
    return identification


class AuthAttempts(IntEnum):
    ATTEMPTS = 5


def main() -> None:
    print(AccessMenuMessage.MENU)
    for menu_number, exists_menu in enumerate(AccessMenu, 1):
        print(f"{menu_number}. {AccessMenu.message(exists_menu)}")

    if not datafile.exists():
        create_datafile()

    menu = menu_selection()

    while True:
        match menu:
            case AccessMenu.REGISTER:
                print(RegisterMessage.TITLE)
                point_username = input(RegisterMessage.INPUT_NAME).strip()
                if len(point_username) != 0 and check_username(username=point_username):
                    invent_password = input(RegisterMessage.INPUT_PASS).strip()
                    if len(invent_password) != 0:
                        register(username=point_username, password=invent_password)
                        print(RegisterMessage.SUCCESS_REGISTER)
                        menu = AccessMenu.AUTHORIZATION
                continue

            case AccessMenu.AUTHORIZATION:
                print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                usernames = [RegisterMessage.NEW_USER] + Accounts().get_usernames()
                for number, user in enumerate(usernames):
                    print(f"{number}. {user}")

                select_index = input(AuthMessage.SELECT_USER_INDEX).strip()
                match account_selection(usernames, select_index):
                    case False:
                        print(AuthMessage.USER_NOT_FOUND)
                        menu = AccessMenu.AUTHORIZATION
                        continue

                user_index = int(select_index)
                if user_index == 0:
                    menu = AccessMenu.REGISTER
                    continue
                else:
                    username = usernames[user_index]
                    print(AuthMessage.USER.format(username))
                    attempts = AuthAttempts.ATTEMPTS
                    for input_attempt in range(1, attempts + 1):
                        password = input(AuthMessage.ENTRY_PASSWORD).strip()
                        if authentication(username=username, password=password):
                            print(Accounts().get_user_id(user_index))
                            run()
                            break
                        elif input_attempt == attempts:
                            print(AuthMessage.ATTEMPTS_ENDED)
                    break

            case _:
                print(AccessMenuMessage.MENU_NOT_FOUND)
                main()

        break


if __name__ == "__main__":
    main()
