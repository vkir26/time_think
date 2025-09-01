from enum import StrEnum, Enum


class GameModeMessage(Enum):
    EASY = "легко"
    NORMAL = "нормально"
    HARD = "сложно"
    SURVIVAL = "выживание"


class SessionMessage(StrEnum):
    START_GAME = "Приветствуем игрок! \nДобро пожаловать в игру 'Время думать'"
    SELECT_DIFFICULTY = "Выберите сложность (цифрой):"
    NOT_FOUND = "Игровая сложность не найдена"
    ENTER = "Ввод: "
    SELECTED_DIFFICULTY = "Выбранная сложность:"
    END_GAME = "Игра завершилась, Ваши результаты:"
    CORRECT = "Правильно"
    NOT_CORRECT = "Неправильно"
    USER_INPUT_ERROR = "Ответ должен быть числом.\nПовторите попытку ввода"
    ENTERING_RESPONSE = "Задание: {}\nОтвет: "
