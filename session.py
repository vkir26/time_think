from enum import IntEnum
from dataclasses import dataclass
from core import check_answer, get_task
from messages import SessionMessage as Message


class ModeSelection(IntEnum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    SURVIVAL = 4


@dataclass(frozen=True, slots=True)
class SessionParameters:
    rounds: int | float
    lives: int


difficulty_parameters: dict[ModeSelection, SessionParameters] = {
    ModeSelection.EASY: SessionParameters(rounds=3, lives=3),
    ModeSelection.NORMAL: SessionParameters(rounds=4, lives=2),
    ModeSelection.HARD: SessionParameters(rounds=5, lives=1),
    ModeSelection.SURVIVAL: SessionParameters(rounds=float("inf"), lives=1),
}


@dataclass(frozen=True, slots=True)
class Result:
    correct: int
    not_correct: int


def get_parameters(custom_difficulty: ModeSelection) -> SessionParameters:
    return difficulty_parameters[custom_difficulty]


def run(user_complexity: ModeSelection) -> Result:
    not_correct_answer = 0
    correct_answer = 0
    question_counter = 0

    task = get_task()
    difficulty = get_parameters(user_complexity)
    while question_counter < difficulty.rounds:
        if not_correct_answer == difficulty.lives:
            break
        try:
            user_answer = int(input(Message.ENTERING_RESPONSE.format(task)))
        except ValueError:
            print(Message.USER_INPUT_ERROR)
            continue
        if check_answer(task, user_answer):
            print(Message.CORRECT)
            correct_answer += 1
            task = get_task()
        else:
            print(Message.NOT_CORRECT)
            not_correct_answer += 1
        question_counter += 1

    return Result(correct=correct_answer, not_correct=not_correct_answer)
