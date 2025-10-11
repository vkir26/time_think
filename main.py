from enum import IntEnum
from session import run, ModeSelection
from messages import SessionMessage, AccessMenuMessage, RegisterMessage, AuthMessage
from auth.config import datafile, create_datafile, AccountStorage
from auth.access_menu import AccessMenu
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from datetime import datetime
from game_statistics import StatisticsStorage, UserStatistic


def menu_selection() -> int:
    while True:
        try:
            select_menu = int(input(AccessMenuMessage.INPUT))
            menu = AccessMenu(select_menu)
            break
        except ValueError:
            print(AccessMenuMessage.MENU_NOT_FOUND)
    return menu


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


class AuthAttempts(IntEnum):
    ATTEMPTS = 5


def get_datetime() -> str:
    return datetime.now().strftime(StatisticsStorage().datetime_format)


def main() -> None:
    print(AccessMenuMessage.MENU)
    for exists_menu in AccessMenu:
        print(f"{exists_menu}. {AccessMenu.message(exists_menu)}")

    if not datafile.exists():
        create_datafile()

    menu = menu_selection()

    while True:
        match menu:
            case AccessMenu.REGISTER:
                print(RegisterMessage.TITLE)
                input_username = input(RegisterMessage.INPUT_NAME).strip()
                if len(input_username) != 0 and check_username(username=input_username):
                    indicate_password = input(RegisterMessage.INPUT_PASS).strip()
                    if len(indicate_password) != 0:
                        register(username=input_username, password=indicate_password)
                        print(RegisterMessage.SUCCESS_REGISTER)
                        menu = AccessMenu.AUTHORIZATION

            case AccessMenu.AUTHORIZATION:
                names = [RegisterMessage.NEW_USER] + AccountStorage().get_usernames()
                print(f"{AuthMessage.TITLE}\n{AuthMessage.ACCOUNT_SELECTION}")
                for number, name in enumerate(names):
                    print(f"{number}. {name}")

                select_user = input(AuthMessage.SELECT_USER_INDEX).strip()
                match check_index(names, select_user):
                    case False:
                        print(AuthMessage.USER_NOT_FOUND)
                        menu = AccessMenu.AUTHORIZATION
                        continue

                user_index = int(select_user)
                username = names[user_index]
                if user_index == 0:
                    menu = AccessMenu.REGISTER
                if user_id := AccountStorage().get_user_id(username):
                    print(AuthMessage.USER.format(username))
                    attempts = AuthAttempts.ATTEMPTS
                    for input_attempt in range(1, attempts + 1):
                        password = input(AuthMessage.ENTRY_PASSWORD).strip()
                        if authentication(user_id=user_id, password=password):
                            print(SessionMessage.SELECT_DIFFICULTY)
                            for difficulty_index, difficulty_mode in enumerate(
                                ModeSelection, 1
                            ):
                                print(
                                    f"{difficulty_index}. {ModeSelection.message(difficulty_mode)}"
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

                            print(
                                SessionMessage.SELECTED_DIFFICULTY, difficulty.message()
                            )
                            start_session = get_datetime()
                            session_result = run(user_complexity=difficulty)
                            end_session = get_datetime()
                            StatisticsStorage().write_statistics(
                                UserStatistic(
                                    user_id=user_id,
                                    session_start=start_session,
                                    session_end=end_session,
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

                            user_statistics = StatisticsStorage().get_my_statistic(
                                user_id=user_id
                            )
                            print("Ваша статистика:")
                            for numbering, user in enumerate(user_statistics, 1):
                                print(
                                    f"{numbering}. Начало игры: {user.session_start} | Окончание игры: {user.session_end} | "
                                    f"Сложность: {user.difficulty} | Правильных ответов: {user.correct} | Неправильных ответов: {user.incorrect}"
                                )
                            break
                        elif input_attempt == attempts:
                            print(AuthMessage.ATTEMPTS_ENDED)
                    break

            case _:
                print(AccessMenuMessage.MENU_NOT_FOUND)
                menu = menu_selection()


if __name__ == "__main__":
    main()
