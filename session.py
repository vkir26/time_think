from enum import StrEnum

from core import main, get_task, Task


class Message(StrEnum):
    END_GAME = "Игра завершилась, Ваши результаты:"
    CORRECT = "Correct"
    NOT_CORRECT = "Not correct"
    USER_INPUT_ERROR = "Ответ должен быть числом.\nПовторите попытку ввода: "


def user_answer() -> int:
    try:
        return int(input())
    except ValueError:
        print(Message.USER_INPUT_ERROR)
        return user_answer()


def check_task(generated_task: Task) -> bool:
    return main(generated_task, user_answer())


def run() -> str:
    attempts = 5
    not_correct_answer = 0
    correct_answer = 0

    task = get_task()
    for i in range(attempts):
        if not_correct_answer != 3:
            print(task)
            if check_task(task):
                print(Message.CORRECT)
                correct_answer += 1
                task = get_task()
            else:
                print(Message.NOT_CORRECT)
                not_correct_answer += 1

    return (
        f"{'=' * 15}\n{Message.END_GAME}\n"
        f"{Message.CORRECT}: {correct_answer}\n"
        f"{Message.NOT_CORRECT}: {not_correct_answer}"
    )
