from enum import Enum, StrEnum
from dataclasses import dataclass
from typing import Type, TypeVar

from auth.config import AccountStorage, Account, peppered_password
from app.menu import MainMenu, AuthSubmenu, SessionMenu
from app.session import run, ModeSelection
from app.messages import (
    MenuMessage,
    SessionMessage,
    RegisterMessage,
    AuthMessage,
)
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from datetime import datetime
from app.game_statistics import StatisticsStorage, UserStatistic


def show_main_menu() -> None:
    print(MenuMessage.MENU)
    for menu in MainMenu:
        print(f"{menu}. {MainMenu.message(menu)}")


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


def datetime_formatting(timedate: str) -> str:
    new_format = "%d.%m.%Y %H:%M:%S"
    datetime_format = datetime.fromisoformat(timedate)
    return datetime.strftime(datetime_format, new_format)


@dataclass(frozen=True, slots=True)
class Session:
    user_id: str


def handle_registration() -> Session | None:
    print(RegisterMessage.TITLE)
    username = input(RegisterMessage.INPUT_NAME).strip()
    if check_username(username=username):
        password = input(RegisterMessage.INPUT_PASS).strip()
        if len(password) != 0:
            session = Session(register(username=username, password=password))
            print(RegisterMessage.SUCCESS_REGISTER)
            return session
    return None


class AuthResult(StrEnum):
    SUCCESS = "success"
    GO_REGISTER = "go_register"
    FAILED = "failed"
    RETRY = "retry"


@dataclass(frozen=True, slots=True)
class AuthorizationOutcome:
    result: AuthResult
    session: Session | None = None


def authentication(account: Account, password: str) -> str | None:
    if identification := authenticate(password=password, account=account):
        print(AuthMessage.SUCCESS_AUTHORIZATION)
    else:
        print(AuthMessage.INCORRECT_PASSWORD)
    return identification


def handle_authorization() -> AuthorizationOutcome:
    print(f"{AuthMessage.TITLE}\n{AuthMessage.SELECTING_AUTH_SECTION}")
    for menu in AuthSubmenu:
        print(f"{menu}. {menu.message()}")

    match menu_selection(AuthSubmenu):
        case AuthSubmenu.NEW_USER:
            return AuthorizationOutcome(result=AuthResult.GO_REGISTER)
        case AuthSubmenu.ENTER_USERNAME:
            username = str(input(RegisterMessage.INPUT_NAME))
            account = AccountStorage().get_by_username(username=username)

            if account is None:
                print(AuthMessage.USER_NOT_FOUND)
                return AuthorizationOutcome(result=AuthResult.RETRY)

            print(AuthMessage.USER.format(username))
            for i in range(ATTEMPTS):
                password = peppered_password(input(AuthMessage.ENTRY_PASSWORD).strip())
                if user_id := authentication(account=account, password=password):
                    return AuthorizationOutcome(
                        result=AuthResult.SUCCESS, session=Session(user_id=user_id)
                    )
                elif i + 1 == ATTEMPTS:
                    return AuthorizationOutcome(result=AuthResult.FAILED)
    return AuthorizationOutcome(result=AuthResult.RETRY)


def show_session_menu() -> None:
    for session_menu in SessionMenu:
        print(f"{session_menu}. {SessionMenu.message(session_menu)}")


def play_game(user_id: str) -> None:
    print(SessionMessage.SELECT_DIFFICULTY)
    for difficulty_mode in ModeSelection:
        print(f"{difficulty_mode}. {ModeSelection.message(difficulty_mode)}")
    difficulty = None
    while True:
        try:
            select_difficulty = int(input(SessionMessage.ENTER).strip())
            difficulty = ModeSelection(select_difficulty)
        except ValueError:
            print(SessionMessage.DIFFICULTY_NOT_FOUND)
            continue
        break
    print(SessionMessage.SELECTED_DIFFICULTY, difficulty.message())
    start_session = datetime.now()
    session_result = run(user_complexity=difficulty)
    end_session = datetime.now()
    StatisticsStorage().write_statistics(
        UserStatistic(
            user_id=user_id,
            session_start=str(start_session),
            session_end=str(end_session),
            difficulty=difficulty.name,
            correct=session_result.correct,
            incorrect=session_result.not_correct,
        )
    )
    print(
        f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
        f"{SessionMessage.CORRECT}: {session_result.correct}\n"
        f"{SessionMessage.NOT_CORRECT}: {session_result.not_correct}"
    )


def show_my_statistics(user_id: str) -> None:
    user_statistics = StatisticsStorage().get_my_statistics(user_id=user_id)
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


def handle_session(session: Session) -> None:
    show_session_menu()
    match menu_selection(SessionMenu):
        case SessionMenu.PLAY:
            play_game(user_id=session.user_id)
        case SessionMenu.MY_STATISTICS:
            show_my_statistics(user_id=session.user_id)
        case SessionMenu.LEADERS:
            print("Скоро...")


class Menu(Enum):
    MAIN = MainMenu
    AUTHORIZATION = MainMenu.AUTHORIZATION
    REGISTRATION = MainMenu.REGISTRATION
    SESSION = SessionMenu


ATTEMPTS = 5


def main() -> None:
    current_menu = Menu.MAIN
    session: Session | None = None

    while True:
        match current_menu, session:
            case Menu.MAIN, None:
                show_main_menu()
                match menu_selection(MainMenu):
                    case MainMenu.REGISTRATION:
                        current_menu = Menu.REGISTRATION
                    case MainMenu.AUTHORIZATION:
                        current_menu = Menu.AUTHORIZATION
                    case MainMenu.HOW_TO_PLAY:
                        print(MenuMessage.HOW_TO_PLAY)

            case Menu.REGISTRATION, None:
                registered = handle_registration()
                if registered is not None:
                    session = registered
                    current_menu = Menu.SESSION

            case Menu.AUTHORIZATION, None:
                outcome = handle_authorization()
                match outcome.result:
                    case AuthResult.SUCCESS:
                        if outcome.session is None:
                            raise RuntimeError("Session not found")
                        session = outcome.session
                        current_menu = Menu.SESSION
                    case AuthResult.GO_REGISTER:
                        current_menu = Menu.REGISTRATION
                    case AuthResult.FAILED:
                        current_menu = Menu.MAIN
                    case AuthResult.RETRY:
                        continue

            case Menu.SESSION, Session() as s:
                handle_session(session=s)


if __name__ == "__main__":
    main()
