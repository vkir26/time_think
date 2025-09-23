import pytest
from main import check_index
from messages import RegisterMessage

USER_LIST = [RegisterMessage.NEW_USER] + ["Иван", "Юрий", "Юля", "Мария", "Гена"]


@pytest.mark.parametrize(
    "usernames, select_index, result",
    [
        (USER_LIST, "3", True),
        (USER_LIST, "0", True),
        (USER_LIST, "-1", False),
        (USER_LIST, "5", True),
        (USER_LIST, "6", False),
        (USER_LIST, "TEXT", False),
        (USER_LIST, "", False),
    ],
)
def test_account_selection(
    usernames: list[str], select_index: str, result: bool
) -> None:
    assert check_index(usernames=usernames, select_index=select_index) == result
