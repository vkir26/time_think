from enum import Enum
from typing import Type, TypeVar
from menu import MainMenu, SessionMenu
from session import run, ModeSelection
from messages import (
    MenuMessage,
    SessionMessage,
    AccessMenuMessage,
    RegisterMessage,
    AuthMessage,
)
from auth.config import AccountStorage
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


class Menu(Enum):
    MAIN = MainMenu
    ACCESS = AccessMenu
    SESSION = SessionMenu


ATTEMPTS = 5


def main() -> None:
    current_menu = Menu.MAIN
    is_registered = False
    is_authorized = False

    while True:
        match current_menu:
            case Menu.MAIN:
                print(MenuMessage.MENU)
                for menu in MainMenu:
                    print(f"{menu}. {MainMenu.message(menu)}")
                match menu_selection(MainMenu):
                    case MainMenu.START_GAME:
                        current_menu = Menu.ACCESS
                    case MainMenu.HOW_TO_PLAY:
                        print(MenuMessage.HOW_TO_PLAY)

            case Menu.ACCESS:
                if is_registered:
                    menu_item = AccessMenu.REGISTER
                    is_registered = False
                elif is_authorized:
                    menu_item = AccessMenu.AUTHORIZATION
                    is_authorized = False
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
                                is_authorized = True
                        if not is_authorized:
                            is_registered = True

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
                            is_authorized = True
                            continue

                        user_index = int(select_user)
                        username = names[user_index]
                        if user_index == 0:
                            is_registered = True
                            continue
                        if user_id := AccountStorage().get_user_id(username):
                            current_menu = Menu.SESSION
                            print(AuthMessage.USER.format(username))
                            for input_attempt in range(1, ATTEMPTS + 1):
                                password = input(AuthMessage.ENTRY_PASSWORD).strip()
                                if authentication(user_id=user_id, password=password):
                                    current_menu = Menu.SESSION
                                    break
                                elif input_attempt == ATTEMPTS:
                                    print(AuthMessage.ATTEMPTS_ENDED)
                                    current_menu = Menu.MAIN

            case Menu.SESSION:
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
                    case SessionMenu.LEADERS:
                        print("Скоро...")


if __name__ == "__main__":
    main()
