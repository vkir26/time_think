from enum import IntEnum, Enum
from typing import Type, TypeVar
from menu import Menu, SessionMenu
from session import run, ModeSelection
from messages import (
    MenuMessage,
    SessionMessage,
    AccessMenuMessage,
    RegisterMessage,
    AuthMessage,
)
from auth.config import datafile, create_datafile, AccountStorage
from auth.access_menu import AccessMenu
from auth.registration import register, name_is_exist
from auth.authorization import authenticate

T = TypeVar("T", bound=Enum)


def menu_selection(menu_type: Type[T]) -> T:
    while True:
        try:
            select_menu = int(input(MenuMessage.INPUT))
            return menu_type(select_menu)
        except ValueError:
            print(MenuMessage.MENU_NOT_FOUND)


def check_username(username: str) -> bool:
    match user := name_is_exist(username):
        case False:
            print(RegisterMessage.NAME_EXISTS)
    return user


def check_index(usernames: list[str], select_index: str) -> int:
    if select_index.isdigit():
        return 1 <= int(select_index) < len(usernames) or int(select_index) == 0
    return False


def authentication(user_id: str, password: str) -> bool:
    match identification := authenticate(user_id=user_id, password=password):
        case True:
            print(AuthMessage.SUCCESS_AUTHORIZATION)
        case _:
            print(AuthMessage.INCORRECT_PASSWORD)
    return identification


class State(Enum):
    MENU = Menu
    ACCESS = AccessMenu
    SESSION = SessionMenu


class AuthAttempts(IntEnum):
    ATTEMPTS = 5


def main() -> None:
    if not datafile.exists():
        create_datafile()

    current_menu = State.MENU
    user_registration = False
    user_authorization = False

    while True:
        match current_menu:
            case State.MENU:
                print(MenuMessage.MENU)
                for menu in Menu:
                    print(f"{menu}. {Menu.message(menu)}")
                match menu_selection(Menu):
                    case Menu.START_GAME:
                        current_menu = State.ACCESS
                    case Menu.HOW_TO_PLAY:
                        print(MenuMessage.HOW_TO_PLAY)
                    case Menu.LEADERS:
                        print("Скоро...")
                    case _:
                        print(MenuMessage.MENU_NOT_FOUND)

            case State.ACCESS:
                if user_registration:
                    menu_item = AccessMenu.REGISTER
                    user_registration = False
                elif user_authorization:
                    menu_item = AccessMenu.AUTHORIZATION
                    user_authorization = False
                else:
                    print(AccessMenuMessage.MENU)
                    for access_menu in AccessMenu:
                        print(f"{access_menu}. {AccessMenu.message(access_menu)}")
                    menu_item = menu_selection(AccessMenu)
                match menu_item:
                    case AccessMenu.REGISTER:
                        print(RegisterMessage.TITLE)
                        input_username = input(RegisterMessage.INPUT_NAME).strip()
                        if len(input_username) != 0 and check_username(
                            username=input_username
                        ):
                            indicate_password = input(
                                RegisterMessage.INPUT_PASS
                            ).strip()
                            if len(indicate_password) != 0:
                                register(
                                    username=input_username, password=indicate_password
                                )
                                print(RegisterMessage.SUCCESS_REGISTER)
                                user_authorization = True
                        if not user_authorization:
                            user_registration = True

                    case AccessMenu.AUTHORIZATION:
                        names = [
                            RegisterMessage.NEW_USER
                        ] + AccountStorage().get_usernames()
                        print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                        for number, name in enumerate(names):
                            print(f"{number}. {name}")

                        select_user = input(AuthMessage.SELECT_USER_INDEX).strip()
                        if not check_index(names, select_user):
                            print(AuthMessage.USER_NOT_FOUND)
                            user_authorization = True
                            continue

                        user_index = int(select_user)
                        username = names[user_index]
                        if user_index == 0:
                            user_registration = True
                            continue
                        if user_id := AccountStorage().get_user_id(username):
                            current_menu = State.SESSION
                            print(AuthMessage.USER.format(username))
                            attempts = AuthAttempts.ATTEMPTS
                            for input_attempt in range(1, attempts + 1):
                                password = input(AuthMessage.ENTRY_PASSWORD).strip()
                                if authentication(user_id=user_id, password=password):
                                    current_menu = State.SESSION
                                    break
                                elif input_attempt == attempts:
                                    print(AuthMessage.ATTEMPTS_ENDED)
                                    current_menu = State.MENU
                    case _:
                        print(AccessMenuMessage.MENU_NOT_FOUND)

            case State.SESSION:
                for session_menu in SessionMenu:
                    print(f"{session_menu}. {SessionMenu.message(session_menu)}")
                match menu_selection(SessionMenu):
                    case SessionMenu.PLAY:
                        print(SessionMessage.SELECT_DIFFICULTY)
                        for difficulty_mode in ModeSelection:
                            print(
                                f"{difficulty_mode}. {ModeSelection.message(difficulty_mode)}"
                            )
                        difficulty = None
                        while True:
                            try:
                                select_difficulty = int(
                                    input(SessionMessage.ENTER).strip()
                                )
                                difficulty = ModeSelection(select_difficulty)
                            except ValueError:
                                print(SessionMessage.NOT_FOUND)
                                continue
                            break
                        print(SessionMessage.SELECTED_DIFFICULTY, difficulty.message())
                        session_result = run(user_complexity=difficulty)
                        print(
                            f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
                            f"{SessionMessage.CORRECT}: {session_result.correct}\n"
                            f"{SessionMessage.NOT_CORRECT}: {session_result.not_correct}"
                        )
                        break
                    case SessionMenu.MY_STATISTICS:
                        print("Моя статистика:\nСкоро...")
                    case _:
                        print(SessionMessage.MENU_NOT_FOUND)


if __name__ == "__main__":
    main()
