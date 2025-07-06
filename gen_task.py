from dataclasses import dataclass
import pytest


@dataclass(frozen=True, slots=True)
class Task:
    task: str
    correct_answer: int


@dataclass(frozen=True, slots=True)
class Answer:
    user_answer: int


def generate_task() -> list[int]:
    return [1, 1]


def get_task() -> Task:
    task_values = generate_task()
    task_condition = "{} + {}".format(*task_values)
    correct_answer = sum(task_values)

    return Task(task=task_condition, correct_answer=correct_answer)


def answer_validator(ready_task: Task, answer: Answer) -> bool:
    if ready_task.correct_answer == answer.user_answer:
        return True
    return False


if __name__ == "__main__":
    task = get_task()
    attempts = 5
    for i in range(attempts):
        print(task.task)
        user_answer = int(input())
        if answer_validator(ready_task=task, answer=Answer(user_answer)):
            print("Correct")
            break
        else:
            print("Not correct")


@pytest.mark.parametrize(
    "ready_task, answer, result",
    [(1, 1, True), (1, 2, False), (5, 3, False), (7, 7, True)],
)
def test_answer_validator(ready_task: int, answer: int, result: bool) -> None:
    assert (
        answer_validator(
            Task(task="None", correct_answer=ready_task), Answer(user_answer=answer)
        )
        == result
    )
