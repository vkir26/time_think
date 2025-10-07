from pathlib import Path
import csv
from dataclasses import dataclass

statistics_file = Path("users_statistics.csv")


def create_statistics_file() -> None:
    with open(statistics_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                "user_id",
                "session_start",
                "session_end",
                "difficulty",
                "correct",
                "incorrect",
            )
        )


if not statistics_file.exists():
    create_statistics_file()


@dataclass(frozen=True, slots=True)
class UserStatistics:
    user_id: str
    session_start: str
    session_end: str
    difficulty: str
    correct: str
    incorrect: str


class StatisticsStorage:
    def __init__(self) -> None:
        self.statistics = self.get_statistics()
        self.my_statistics = self.get_my_statistics

    def get_statistics(self) -> list[UserStatistics]:
        with open(statistics_file, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            self.statistics = [UserStatistics(**statistics) for statistics in reader]
        return self.statistics

    def get_my_statistics(self, user_id: str) -> list[UserStatistics]:
        my_statistics = []
        for statistics in self.statistics:
            if statistics.user_id in user_id:
                my_statistics.append(statistics)
        return my_statistics[::-1]


def write_statistics(
    user_id: str,
    session_start: str,
    session_end: str,
    difficulty: str,
    correct: int,
    incorrect: int,
) -> None:
    with open(statistics_file, "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [user_id, session_start, session_end, difficulty, correct, incorrect]
        )


# user_statistics = StatisticsStorage().get_my_statistics("a19b253d-be28-49b3-baab-72306c098d86")
# print("Моя статистика:")
# for numbering, user in enumerate(user_statistics, 1):
#     print(
#         f"{numbering}. Начало игры: {user.session_start} | Окончание игры: {user.session_end} | "
#         f"Сложность: {user.difficulty} | Правильных ответов: {user.correct} | Неправильных ответов: {user.incorrect}"
#     )
