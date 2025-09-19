from messages import SessionMessage
from session import run, ModeSelection


def main() -> None:
    print(SessionMessage.SELECT_DIFFICULTY)
    for difficulty_index, difficulty_mode in enumerate(ModeSelection, 1):
        print(f"{difficulty_index}. {ModeSelection.message(difficulty_mode)}")

    difficulty = None
    while True:
        try:
            select_difficulty = int(input(SessionMessage.ENTER).strip())
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


if __name__ == "__main__":
    main()
