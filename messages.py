from enum import StrEnum


class AccessMenuMessage(StrEnum):
    MENU = "Выберете меню (цифрой):"
    AUTHORIZATION = "1. Авторизоваться"
    REGISTER = "2. Зарегистрироваться"
    INPUT = "Ввод: "
    MENU_NOT_FOUND = "Меню не найдено, попробуйте заново"


class AuthMessage(StrEnum):
    TITLE = "[АВТОРИЗАЦИЯ]"
    ACCOUNT_SELECTION = "Выберете аккаунт для входа (цифрой):"
    SELECT_USER_INDEX = "Имя пользователя №: "
    USER = "Пользователь: {}"
    ENTRY_PASSWORD = "Пароль: "
    USER_NOT_FOUND = "Пользователь не найден"
    INCORRECT_PASSWORD = "Пароль указан неверно"
    SUCCESS_AUTHORIZATION = "Успешная авторизация!"


class RegisterMessage(StrEnum):
    NEW_USER = "Новый пользователь"
    TITLE = "[РЕГИСТРАЦИЯ]"
    INPUT_NAME = "Введите имя: "
    NAME_EXISTS = "Данное имя уже существует"
    INPUT_PASS = "Придумайте пароль: "
    SUCCESS_REGISTER = "Успешная регистрация!"
