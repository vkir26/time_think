from enum import IntEnum
from typing import assert_never


class AccessMenu(IntEnum):
    AUTHORIZATION = 1
    REGISTER = 2

    def message(self) -> str:
        match self:
            case AccessMenu.AUTHORIZATION:
                return "Авторизоваться"
            case AccessMenu.REGISTER:
                return "Зарегистрироваться"
            case _ as unreachable_case:
                assert_never(unreachable_case)
