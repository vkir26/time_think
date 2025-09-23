from enum import StrEnum


class AccessMenuMessage(StrEnum):
    MENU = "Выберете меню (цифрой):"
    INPUT = "Ввод: "
    MENU_NOT_FOUND = (
        "Раздел меню недоступен или отсутствует.\nПопробуйте выбрать другой раздел"
    )


class AuthMessage(StrEnum):
    TITLE = "[АВТОРИЗАЦИЯ]"
    ACCOUNT_SELECTION = "Выберете аккаунт для входа (цифрой):"
    SELECT_USER_INDEX = "Имя пользователя №: "
    USER = "Пользователь: {}"
    ENTRY_PASSWORD = "Пароль: "
    USER_NOT_FOUND = "Пользователь не найден"
    INCORRECT_PASSWORD = "Пароль указан неверно"
    ATTEMPTS_ENDED = "Использовано максимальное количество попыток входа"
    SUCCESS_AUTHORIZATION = "Успешная авторизация!"
    KEY_NOT_FOUND = "Ключ {} не найден"


class RegisterMessage(StrEnum):
    NEW_USER = "Новый пользователь"
    TITLE = "[РЕГИСТРАЦИЯ]"
    INPUT_NAME = "Введите имя: "
    NAME_EXISTS = "Данное имя уже существует"
    INPUT_PASS = "Придумайте пароль: "
    SUCCESS_REGISTER = "Успешная регистрация!"
