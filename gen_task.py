import random
from dataclasses import dataclass
import pytest


@dataclass(frozen=True, slots=True)
class Answer:
    user_answer: int

    def __eq__(self, other: int) -> bool:  # type: ignore[override]
        return self.user_answer == other


@dataclass(frozen=True, slots=True)
class Task:
    task: str
    correct_answer: Answer

    def __str__(self) -> str:
        return self.task


def generate_task() -> list[int]:
    return [random.randint(1, 7) for _ in range(2)]


def get_task() -> Task:
    task_values = generate_task()
    task_condition = "{} + {}".format(*task_values)
    correct_answer = sum(task_values)

    return Task(task=task_condition, correct_answer=Answer(correct_answer))


def answer_validator(ready_task: Task, answer: Answer) -> bool:
    return ready_task.correct_answer == answer.user_answer


def main() -> bool:
    return answer_validator(ready_task=task, answer=Answer(user_answer))


if __name__ == "__main__":
    task = get_task()
    attempts = 5
    for i in range(attempts):
        print(task)
        user_answer = int(input())
        if main():
            print("Correct")
            break
        else:
            print("Not correct")


@pytest.mark.parametrize(
    "answer_on_task, answer_user, result",
    [(1, 1, True), (1, 2, False), (5, 3, False), (7, 7, True)],
)
def test_answer_validator(answer_on_task: int, answer_user: int, result: bool) -> None:
    assert (
        answer_validator(
            Task(task="task_condition", correct_answer=Answer(answer_on_task)),
            answer=Answer(answer_user),
        )
        == result
    )


@pytest.mark.parametrize("answer_user", [7])
def test_generate_task(seed: None, answer_user: int) -> None:
    assert sum(generate_task()) == answer_user
