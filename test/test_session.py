from session import user_answer
from unittest.mock import patch
import pytest


@pytest.mark.parametrize("user_input, result", [(["10"], 10), (["TEST", "5"], 5)])
def test_user_answer(user_input: str, result: int) -> None:
    """patch("builtins.input", side_effect=inputs) заменяет функцию input так,
    что при каждом вызове она возвращает следующий элемент из списка user_input"""
    with patch("builtins.input", side_effect=user_input):
        assert user_answer() == result
