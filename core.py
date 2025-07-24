import random
from dataclasses import dataclass
from builtins import object


@dataclass(frozen=True, slots=True)
class Answer:
    _answer: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Answer):
            raise NotImplementedError
        return self._answer == other._answer


@dataclass(frozen=True, slots=True)
class Task:
    task: str
    correct_answer: Answer

    def __str__(self) -> str:
        return self.task

    def check(self, answer: Answer) -> bool:
        return self.correct_answer == answer


def generate_task() -> list[int]:
    return [random.randint(1, 7) for _ in range(2)]


def get_task() -> Task:
    task_values = generate_task()
    task_condition = "{} + {}".format(*task_values)
    correct_answer = sum(task_values)

    return Task(task=task_condition, correct_answer=Answer(correct_answer))


def answer_validator(ready_task: Task, answer: Answer) -> bool:
    return ready_task.check(answer=answer)


def main(task: Task, user_answer: int) -> bool:
    return answer_validator(ready_task=task, answer=Answer(user_answer))
