from enum import IntEnum
from typing import assert_never


class Menu(IntEnum):
    START_GAME = 1
    HOW_TO_PLAY = 2
    LEADERS = 3

    def message(self) -> str:
        match self:
            case Menu.START_GAME:
                return "Начать игру"
            case Menu.HOW_TO_PLAY:
                return "Как играть?"
            case Menu.LEADERS:
                return "Лидеры"
            case _ as unreachable_case:
                assert_never(unreachable_case)


class SessionMenu(IntEnum):
    PLAY = 1
    MY_STATISTICS = 2

    def message(self) -> str:
        match self:
            case SessionMenu.PLAY:
                return "Играть"
            case SessionMenu.MY_STATISTICS:
                return "Моя статистика"
            case _ as unreachable_case:
                assert_never(unreachable_case)
