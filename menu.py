from enum import IntEnum
from typing import assert_never


class MainMenu(IntEnum):
    REGISTRATION = 1
    AUTHORIZATION = 2
    HOW_TO_PLAY = 3

    def message(self) -> str:
        match self:
            case MainMenu.AUTHORIZATION:
                return "Авторизация"
            case MainMenu.REGISTRATION:
                return "Регистрация"
            case MainMenu.HOW_TO_PLAY:
                return "Как играть?"
            case _ as unreachable_case:
                assert_never(unreachable_case)


class SessionMenu(IntEnum):
    PLAY = 1
    MY_STATISTICS = 2
    LEADERS = 3

    def message(self) -> str:
        match self:
            case SessionMenu.PLAY:
                return "Играть"
            case SessionMenu.MY_STATISTICS:
                return "Моя статистика"
            case SessionMenu.LEADERS:
                return "Лидеры"
            case _ as unreachable_case:
                assert_never(unreachable_case)
