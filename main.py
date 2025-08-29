from messages import GameModeMessage, SessionMessage
from session import run

print(SessionMessage.START_GAME)


def main() -> None:
    try:
        print(SessionMessage.SELECT_DIFFICULTY)
        for num, difficulty in enumerate(GameModeMessage, 1):
            print(f"{num}. {difficulty}")
        select_difficulty = int(input(SessionMessage.ENTER))
        user_answer = run(select_difficulty)
        print(
            f"{'=' * 15}\n{SessionMessage.END_GAME}\n"
            f"{SessionMessage.CORRECT}: {user_answer.CORRECT}\n"
            f"{SessionMessage.NOT_CORRECT}: {user_answer.NOT_CORRECT}"
        )
    except ValueError:
        print(SessionMessage.NOT_FOUND)
        main()


if __name__ == "__main__":
    main()
