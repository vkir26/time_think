from session import run
from messages import AccessMenuMessage, RegisterMessage, AuthMessage
from auth.config import datafile, create_datafile, Accounts
from auth.access_menu import menu_selector, AccessMenu
from auth.registration import register, name_is_exist, NameExists
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


def assign_username() -> str:
    while username := input(RegisterMessage.INPUT_NAME).strip():
        match name_is_exist(username):
            case NameExists.EXIST:
                print(RegisterMessage.NAME_EXISTS)
            case NameExists.NOT_EXIST:
                break
    return username


def account_selection(usernames: list[str]) -> int:
    while select_index := input(AuthMessage.SELECT_USER_INDEX).strip():
        if select_index.isdigit() and 0 <= int(select_index) < len(usernames):
            break
        else:
            print(AuthMessage.USER_NOT_FOUND)
    return int(select_index)


def authentication(username: str) -> str | None:
    identification = None
    while password := input(AuthMessage.ENTRY_PASSWORD).strip():
        match identification := authid(username=username, password=password).id:
            case user_id if user_id is not None:
                print(AuthMessage.SUCCESS_AUTHORIZATION)
                break
            case _:
                print(AuthMessage.INCORRECT_PASSWORD)
    return identification


def main() -> None:
    print(
        f"{AccessMenuMessage.MENU}\n"
        f"{AccessMenuMessage.AUTHORIZATION}\n"
        f"{AccessMenuMessage.REGISTER}"
    )
    if not datafile.exists():
        create_datafile()

    menu = menu_selection()

    while True:
        match menu:
            case AccessMenu.REGISTER:
                print(RegisterMessage.TITLE)
                username = assign_username()
                password = input(RegisterMessage.INPUT_PASS).strip()
                register(username=username, password=password)
                print(RegisterMessage.SUCCESS_REGISTER)
                menu = AccessMenu.AUTHORIZATION

            case AccessMenu.AUTHORIZATION:
                print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                usernames = Accounts().get_usernames()
                for number, user in enumerate(usernames):
                    print(f"{number}. {user}")
                user_index = account_selection(usernames)
                match user_index:
                    case 0:
                        menu = AccessMenu.REGISTER
                        continue
                    case _:
                        username = usernames[user_index]
                        print(AuthMessage.USER.format(username))
                        identification = authentication(username=username)
                        print(identification)

                run()
                break


if __name__ == "__main__":
    main()
