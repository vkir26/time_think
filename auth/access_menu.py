from enum import IntEnum


class AccessMenu(IntEnum):
    AUTHORIZATION = 1
    REGISTER = 2


def menu_selector(selected_menu: int) -> AccessMenu:
    return AccessMenu(selected_menu)
