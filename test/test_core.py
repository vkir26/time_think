import pytest
from core import answer_validator, generate_task, Task, Answer


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
