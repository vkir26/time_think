from enum import StrEnum
from dataclasses import dataclass
from core import check_answer, get_task


class Gamemode(StrEnum):
    EASY = "легко"
    NORMAL = "нормально"
    HARD = "сложно"
    SURVIVAL = "выживание"


@dataclass(frozen=True, slots=True)
class SessionParameters:
    attempts: int
    lives: int


difficulty_parameters: dict[Gamemode, SessionParameters] = {
    Gamemode.EASY: SessionParameters(attempts=3, lives=3),
    Gamemode.NORMAL: SessionParameters(attempts=4, lives=2),
    Gamemode.HARD: SessionParameters(attempts=5, lives=1),
    Gamemode.SURVIVAL: SessionParameters(attempts=-1, lives=1),
}


class Message(StrEnum):
    START_GAME = (
        f"Приветствуем игрок! \n"
        f"Добро пожаловать в игру 'Время думать'\n"
        f"Выберите сложность {[diff.value for diff in Gamemode]}"
    )
    END_GAME = "Игра завершилась, Ваши результаты:"
    CORRECT = "Правильно"
    NOT_CORRECT = "Неправильно"
    USER_INPUT_ERROR = "Ответ должен быть числом.\nПовторите попытку ввода"


def get_parameters(custom_difficulty: Gamemode) -> SessionParameters:
    return difficulty_parameters[custom_difficulty]


def run() -> None:
    not_correct_answer = 0
    correct_answer = 0
    question_counter = 0

    task = get_task()
    print(Message.START_GAME)
    difficulty_selection = Gamemode.SURVIVAL
    difficulty = get_parameters(difficulty_selection)
    while (
        question_counter < difficulty.attempts
        or difficulty_selection == Gamemode.SURVIVAL
    ):
        if not_correct_answer == difficulty.lives:
            break
        user_answer = int(input(f"Задание: {task}\nОтвет: "))
        if check_answer(task, user_answer):
            print(Message.CORRECT)
            correct_answer += 1
            task = get_task()
        else:
            print(Message.NOT_CORRECT)
            not_correct_answer += 1
        question_counter += 1

    print(
        f"{'=' * 15}\n{Message.END_GAME}\n"
        f"{Message.CORRECT}: {correct_answer}\n"
        f"{Message.NOT_CORRECT}: {not_correct_answer}"
    )
