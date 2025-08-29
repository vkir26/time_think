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
    ATTEMPTS: int
    LIVES: int


difficulty_parameters: dict[ModeSelection, SessionParameters] = {
    ModeSelection.EASY: SessionParameters(ATTEMPTS=3, LIVES=3),
    ModeSelection.NORMAL: SessionParameters(ATTEMPTS=4, LIVES=2),
    ModeSelection.HARD: SessionParameters(ATTEMPTS=5, LIVES=1),
    ModeSelection.SURVIVAL: SessionParameters(ATTEMPTS=-1, LIVES=1),
}


@dataclass(frozen=True, slots=True)
class Result:
    CORRECT: int
    NOT_CORRECT: int


def get_parameters(custom_difficulty: ModeSelection) -> SessionParameters:
    return difficulty_parameters[custom_difficulty]


def run(select_user: int) -> Result:
    not_correct_answer = 0
    correct_answer = 0
    question_counter = 0

    task = get_task()
    difficulty_selection = ModeSelection(select_user)
    difficulty = get_parameters(ModeSelection(select_user))
    while (
        question_counter < difficulty.ATTEMPTS
        or difficulty_selection == ModeSelection.SURVIVAL
    ):
        if not_correct_answer == difficulty.LIVES:
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

    return Result(CORRECT=correct_answer, NOT_CORRECT=not_correct_answer)
