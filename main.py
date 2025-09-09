from messages import GameModeMessage, SessionMessage
from session import run, ModeSelection


def set_difficulty() -> ModeSelection:
    while True:
        try:
            select_difficulty = ModeSelection(int(input(SessionMessage.ENTER)))
            break
        except ValueError:
            print(SessionMessage.NOT_FOUND)
    print(
        SessionMessage.SELECTED_DIFFICULTY,
        GameModeMessage[select_difficulty.name].value,
    )
    return select_difficulty


def main() -> None:
    print(SessionMessage.SELECT_DIFFICULTY)
    for num, difficulty in enumerate(GameModeMessage, 1):
        print(f"{num}. {difficulty.value}")
    user_answer = run(user_complexity=set_difficulty())
    print(
        f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
        f"{SessionMessage.CORRECT}: {user_answer.correct}\n"
        f"{SessionMessage.NOT_CORRECT}: {user_answer.not_correct}"
    )


if __name__ == "__main__":
    main()
