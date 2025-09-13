from messages import SessionMessage
from session import run, ModeSelection


def set_difficulty(select_difficulty: str) -> ModeSelection | None:
    try:
        return ModeSelection(int(select_difficulty))
    except ValueError:
        return None


def main() -> None:
    print(SessionMessage.SELECT_DIFFICULTY)
    for difficulty_index, difficulty_mode in enumerate(ModeSelection, 1):
        print(f"{difficulty_index}. {ModeSelection.message(difficulty_mode)}")

    while True:
        select_difficulty = input(SessionMessage.ENTER).strip()
        match difficulty := set_difficulty(select_difficulty):
            case None:
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
