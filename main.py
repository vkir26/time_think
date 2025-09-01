from messages import GameModeMessage, SessionMessage
from session import run, difficulty_selector, ModeSelection

print(SessionMessage.START_GAME)


def set_difficulty() -> ModeSelection:
    while True:
        try:
            select_difficulty = int(input(SessionMessage.ENTER))
            difficulty = difficulty_selector(select_difficulty=select_difficulty)
        except ValueError:
            print(SessionMessage.NOT_FOUND)
            continue
        print(
            SessionMessage.SELECTED_DIFFICULTY, GameModeMessage[difficulty.name].value
        )
        return difficulty


def main() -> None:
    print(SessionMessage.SELECT_DIFFICULTY)
    for num, difficulty in enumerate(GameModeMessage, 1):
        print(f"{num}. {difficulty.value}")
    user_answer = run(user_complexity=set_difficulty())
    print(
        f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
        f"{SessionMessage.CORRECT}: {user_answer.CORRECT}\n"
        f"{SessionMessage.NOT_CORRECT}: {user_answer.NOT_CORRECT}"
    )


if __name__ == "__main__":
    main()
