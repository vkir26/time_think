from enum import IntEnum
from typing import assert_never


class MainMenu(IntEnum):
    START_GAME = 1
    HOW_TO_PLAY = 2

    def message(self) -> str:
        match self:
            case MainMenu.START_GAME:
                return "Войти"
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
