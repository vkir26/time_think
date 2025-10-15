from dataclasses import dataclass
from enum import Enum, StrEnum
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
from datetime import datetime
from game_statistics import StatisticRow, StatisticsStorage

T = TypeVar("T", bound=Enum)


def menu_selection(menu_type: Type[T]) -> T:
    while True:
        try:
            select_menu = int(input(MenuMessage.INPUT))
            return menu_type(select_menu)
        except ValueError:
            print(MenuMessage.MENU_NOT_FOUND)


def check_username(username: str) -> bool:
    if len(username) < 3:
        print("Имя должно быть длиннее 3 символов")
        return False
    if name_is_exist(username):
        print(RegisterMessage.NAME_EXISTS)
        return False
    return True


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


class Registration(StrEnum):
    REG = "REG"


class Menu(Enum):
    MAIN = MainMenu
    REGISTRATION = Registration
    AUTHORIZATION = AccessMenu
    SESSION = SessionMenu


ATTEMPTS = 5


def main() -> None:
    current_menu = Menu.MAIN
    user_id: str | None = None

    while True:
        print(current_menu, "--" * 10)
        match current_menu:
            case Menu.MAIN:
                print(MenuMessage.MENU)
                for menu in MainMenu:
                    print(f"{menu}. {MainMenu.message(menu)}")
                match menu_selection(MainMenu):
                    case MainMenu.REGISTRATION:
                        current_menu = Menu.REGISTRATION
                    case MainMenu.AUTHORIZATION:
                        current_menu = Menu.AUTHORIZATION
                    case MainMenu.HOW_TO_PLAY:
                        print(MenuMessage.HOW_TO_PLAY)

            case Menu.REGISTRATION:
                print(RegisterMessage.TITLE)
                username = input(RegisterMessage.INPUT_NAME).strip()
                if check_username(username=username):
                    password = input(RegisterMessage.INPUT_PASS).strip()
                    if len(password) != 0:
                        user_id = register(username=username, password=password)
                        print(RegisterMessage.SUCCESS_REGISTER)
                        current_menu = Menu.SESSION
                        print(current_menu, "+++")
            case Menu.AUTHORIZATION:
                names = [RegisterMessage.NEW_USER] + AccountStorage().get_usernames()
                print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                changer = {str(number): name for number, name in enumerate(names)}
                for e, n in changer.items():
                    print(f"{e}. {n}")
                inp = input(AuthMessage.SELECT_USER_INDEX).strip()
                if (username := changer.get(inp, None)) is None:
                    continue

                if username == RegisterMessage.NEW_USER:
                    current_menu = Menu.REGISTRATION
                    continue

                if candidate := AccountStorage().get_by_username(username):
                    print(AuthMessage.USER.format(username))
                    for _ in range(ATTEMPTS):
                        password = input(AuthMessage.ENTRY_PASSWORD).strip()
                        if authentication(user_id=candidate, password=password):
                            user_id = candidate
                            current_menu = Menu.SESSION
                            break
                    else:
                        print(AuthMessage.ATTEMPTS_ENDED)
                        current_menu = Menu.MAIN

            case Menu.SESSION:
                print(f"ПРИВЕТ {user_id}")
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
                        start_session = datetime.now()
                        session_result = run(user_complexity=difficulty)
                        end_session = datetime.now()
                        StatisticsStorage().write_statistics(
                            StatisticRow(
                                user_id=user_id,
                                session_start=start_session,
                                session_end=end_session,
                                difficulty=difficulty,
                                correct=session_result.correct,
                                incorrect=session_result.not_correct,
                            )
                        )
                        print(
                            f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
                            f"{SessionMessage.CORRECT}: {session_result.correct}\n"
                            f"{SessionMessage.NOT_CORRECT}: {session_result.not_correct}"
                        )
                    case SessionMenu.MY_STATISTICS:
                        user_statistics = StatisticsStorage().get_user_statistic(
                            user_id=user_id
                        )
                        if len(user_statistics) > 0:
                            print(SessionMessage.STATISTICS_HEADER)
                            for numbering, user in enumerate(user_statistics, 1):
                                print(
                                    f"{numbering}.",
                                    SessionMessage.PRINT_STATISTICS.format(
                                        user.session_start,
                                        user.session_end,
                                        user.difficulty,
                                        user.correct,
                                        user.incorrect,
                                    ),
                                )
                        else:
                            print("Тут пусто...")
                        print("-" * 10)
                    case SessionMenu.LEADERS:
                        print("Скоро...")


if __name__ == "__main__":
    main()
