from enum import Enum
from dataclasses import dataclass
from typing import Type, TypeVar
from menu import MainMenu, SessionMenu
from session import run, ModeSelection
from messages import (
    MenuMessage,
    SessionMessage,
    RegisterMessage,
    AuthMessage,
)
from auth.config import AccountStorage
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from datetime import datetime
from game_statistics import StatisticsStorage, UserStatistic

T = TypeVar("T", bound=Enum)


def menu_selection(menu_type: Type[T]) -> T:
    while True:
        try:
            select_menu = int(input(MenuMessage.INPUT))
            return menu_type(select_menu)
        except ValueError:
            print(MenuMessage.MENU_NOT_FOUND)


def check_username(username: str) -> bool:
    number_of_characters = 3
    if len(username) < number_of_characters:
        print(RegisterMessage.NAME_LEN.format(number_of_characters))
        return False
    if name_is_exist(username):
        print(RegisterMessage.NAME_EXISTS)
        return False
    return True


def authentication(user_id: str, password: str) -> bool:
    match identification := authenticate(user_id=user_id, password=password):
        case True:
            print(AuthMessage.SUCCESS_AUTHORIZATION)
        case _:
            print(AuthMessage.INCORRECT_PASSWORD)
    return identification


def names_by_index() -> dict[str, str]:
    names = [RegisterMessage.NEW_USER] + AccountStorage().get_usernames()
    return {str(number): name for number, name in enumerate(names)}


def datetime_formatting(timedate: str) -> str:
    new_format = "%d.%m.%Y %H:%M:%S"
    datetime_format = datetime.fromisoformat(timedate)
    return datetime.strftime(datetime_format, new_format)


class Menu(Enum):
    MAIN = MainMenu
    AUTHORIZATION = MainMenu.AUTHORIZATION
    REGISTRATION = MainMenu.REGISTRATION
    SESSION = SessionMenu


@dataclass(frozen=True, slots=True)
class Session:
    user_id: str


ATTEMPTS = 5


def main() -> None:
    current_menu = Menu.MAIN
    session: Session | None = None

    while True:
        match current_menu, session:
            case Menu.MAIN, None:
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

            case Menu.REGISTRATION, None:
                print(RegisterMessage.TITLE)
                username = input(RegisterMessage.INPUT_NAME).strip()
                if check_username(username=username):
                    password = input(RegisterMessage.INPUT_PASS).strip()
                    if len(password) != 0:
                        session = Session(
                            register(username=username, password=password)
                        )
                        print(RegisterMessage.SUCCESS_REGISTER)
                        current_menu = Menu.SESSION

            case Menu.AUTHORIZATION, None:
                print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                changer = names_by_index()
                for number, name in changer.items():
                    print(f"{number}. {name}")
                user_position = input(AuthMessage.SELECT_USER_INDEX).strip()
                if (selected := changer.get(user_position, None)) is None:
                    print(AuthMessage.USER_NOT_FOUND)
                    continue

                if selected == RegisterMessage.NEW_USER:
                    current_menu = Menu.REGISTRATION
                    continue

                if user_id := AccountStorage().get_by_username(selected):
                    print(AuthMessage.USER.format(selected))
                    for i in range(ATTEMPTS):
                        password = input(AuthMessage.ENTRY_PASSWORD).strip()
                        if authentication(user_id=user_id, password=password):
                            session = Session(user_id=user_id)
                            current_menu = Menu.SESSION
                            break
                        elif i + 1 == ATTEMPTS:
                            print(AuthMessage.ATTEMPTS_ENDED)
                            current_menu = Menu.MAIN

            case Menu.SESSION, Session() as s:
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
                            UserStatistic(
                                user_id=s.user_id,
                                session_start=str(start_session),
                                session_end=str(end_session),
                                difficulty=difficulty.name,
                                correct=str(session_result.correct),
                                incorrect=str(session_result.not_correct),
                            )
                        )
                        print(
                            f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
                            f"{SessionMessage.CORRECT}: {session_result.correct}\n"
                            f"{SessionMessage.NOT_CORRECT}: {session_result.not_correct}"
                        )
                    case SessionMenu.MY_STATISTICS:
                        user_statistics = StatisticsStorage().get_my_statistics(
                            user_id=s.user_id
                        )
                        if len(user_statistics) > 0:
                            print(SessionMessage.STATISTICS_HEADER)
                            for numbering, user in enumerate(user_statistics, 1):
                                print(
                                    f"{numbering}.",
                                    SessionMessage.PRINT_STATISTICS.format(
                                        datetime_formatting(user.session_start),
                                        datetime_formatting(user.session_end),
                                        ModeSelection[user.difficulty].message(),
                                        user.correct,
                                        user.incorrect,
                                    ),
                                )
                            print("#" * 35)
                        else:
                            print(SessionMessage.STATISTICS_NOT_FOUND)
                    case SessionMenu.LEADERS:
                        print("Скоро...")


if __name__ == "__main__":
    main()
