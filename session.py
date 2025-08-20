from enum import StrEnum, IntEnum
from core import check_answer, get_task


class SessionParameters(IntEnum):
    ATTEMPTS = 5
    LIVES = 3


class Message(StrEnum):
    END_GAME = "Игра завершилась, Ваши результаты:"
    CORRECT = "Правильно"
    NOT_CORRECT = "Неправильно"


class ErrorMessage(StrEnum):
    USER_INPUT_ERROR = "Ответ должен быть числом.\nПовторите попытку ввода"


def run() -> None:
    not_correct_answer = 0
    correct_answer = 0

    task = get_task()
    for attempt in range(SessionParameters.ATTEMPTS):
        if not_correct_answer != SessionParameters.LIVES:
            user_answer = int(input(f"Задание: {task}\nОтвет: "))
            if check_answer(task, user_answer):
                print(Message.CORRECT)
                correct_answer += 1
                task = get_task()
            else:
                print(Message.NOT_CORRECT)
                not_correct_answer += 1

    print(
        f"{'=' * 15}\n{Message.END_GAME}\n"
        f"{Message.CORRECT}: {correct_answer}\n"
        f"{Message.NOT_CORRECT}: {not_correct_answer}"
    )
