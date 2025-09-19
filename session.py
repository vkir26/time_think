from enum import IntEnum
from dataclasses import dataclass
from core import check_answer, get_task
from messages import SessionMessage as Message
from typing import assert_never


class ModeSelection(IntEnum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    SURVIVAL = 4

    def message(self) -> str:
        match self:
            case ModeSelection.EASY:
                return "легко"
            case ModeSelection.NORMAL:
                return "нормально"
            case ModeSelection.HARD:
                return "сложно"
            case ModeSelection.SURVIVAL:
                return "выживание"
            case _ as unreachable_case:
                assert_never(unreachable_case)


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

assert len(difficulty_parameters) == len(ModeSelection), (
    "Укажите параметры сложности в 'difficulty_parameters'!"
)


@dataclass(frozen=True, slots=True)
class Result:
    correct: int
    not_correct: int


def get_parameters(custom_difficulty: ModeSelection) -> SessionParameters:
    try:
        return difficulty_parameters[custom_difficulty]
    except KeyError:
        return difficulty_parameters[ModeSelection.EASY]


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
