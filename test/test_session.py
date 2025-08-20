import pytest


@pytest.mark.parametrize("user_input, result", [(["10"], 10), (["TEST", "5"], 5)])
def test_user_answer(user_input: str, result: int) -> None: ...
