from enum import IntEnum


class AccessMenu(IntEnum):
    AUTHORIZATION = 1
    REGISTER = 2

    def message(self) -> str:
        match self:
            case self.AUTHORIZATION:
                return "Авторизоваться"
            case self.REGISTER:
                return "Зарегистрироваться"

            case _:
                return "Название меню отсутствует"


def menu_selector(selected_menu: int) -> AccessMenu:
    return AccessMenu(selected_menu)
