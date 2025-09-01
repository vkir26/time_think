from pathlib import Path
from messages import AccessMenuMessage, RegisterMessage, AuthMessage
from auth.config import datafile, create_datafile
from auth.access_menu import menu_selector, AccessMenu
from auth.registration import register, choose_name
from auth.authorization import get_usernames, authid

print(
    f"{AccessMenuMessage.MENU}\n"
    f"{AccessMenuMessage.AUTHORIZATION}\n"
    f"{AccessMenuMessage.REGISTER}"
)


def menu_selection() -> int:
    while True:
        try:
            select_menu = int(input(AccessMenuMessage.INPUT))
            menu = menu_selector(selected_menu=select_menu)
        except ValueError:
            print(AccessMenuMessage.MENU_NOT_FOUND)
            continue
        return menu


def assign_username(filepath: Path) -> str:
    while True:
        print(RegisterMessage.TITLE)
        username = input(RegisterMessage.INPUT_NAME).strip()
        if choose_name(username, filepath) is None:
            print(RegisterMessage.NAME_EXISTS)
            continue
        return username


def user_choice(usernames: list[str]) -> str:
    while True:
        select_index = input(AuthMessage.SELECT_USER_INDEX)
        if select_index.isdigit() and 1 <= int(select_index) <= len(usernames):
            user = usernames[int(select_index) - 1]
        else:
            print(AuthMessage.INDEX_NOT_FOUND)
            continue
        print(AuthMessage.USER.format(user))
        return user


def authentication(filepath: Path, username: str) -> str:
    while True:
        password = input(AuthMessage.ENTRY_PASSWORD).strip()
        identification = authid(filepath=filepath, username=username, password=password)
        if identification is not None:
            print(AuthMessage.SUCCESS_AUTHORIZATION)
        else:
            print(AuthMessage.INCORRECT_PASSWORD)
            continue
        return identification.ID


def main() -> None:
    if not datafile.exists():
        create_datafile()

    menu = menu_selection()

    if menu is AccessMenu.REGISTER:
        username = assign_username(filepath=datafile)
        password = input(RegisterMessage.INPUT_PASS).strip()
        register(username=username, password=password, filepath=datafile)
        print(RegisterMessage.SUCCESS_REGISTER)
        menu = AccessMenu.AUTHORIZATION

    if menu is AccessMenu.AUTHORIZATION:
        print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
        usernames = get_usernames(datafile).USERNAMES
        for number, user in enumerate(usernames, 1):
            print(f"{number}. {user}")
        username = user_choice(usernames)
        identification = authentication(filepath=datafile, username=username)
        print(identification)


if __name__ == "__main__":
    main()
