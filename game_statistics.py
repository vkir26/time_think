from pathlib import Path
import csv
from datetime import datetime
from pydantic import BaseModel

from session import ModeSelection

statistics_file = Path("users_statistics.csv")


class StatisticRow(BaseModel):
    user_id: str
    session_start: datetime
    session_end: datetime
    difficulty: ModeSelection
    correct: int
    incorrect: int


def create_statistics_file() -> None:
    with open(statistics_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow((StatisticRow.__annotations__.keys()))


class StatisticsStorage:
    def __init__(self) -> None:
        if not statistics_file.exists():
            create_statistics_file()
        self.statistic = self.get_statistics()

    @classmethod
    def get_statistics(cls) -> dict[str, list[StatisticRow]]:
        storage: dict[str, list[StatisticRow]] = {}
        with open(statistics_file, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            for statistic in reader:
                data = StatisticRow.model_validate(statistic)
                if storage.get(data.user_id, None) is None:
                    storage[data.user_id] = []
                storage[data.user_id].append(data)
        return storage

    def get_user_statistic(self, user_id: str) -> list[StatisticRow]:
        return sorted(
            self.statistic.get(user_id, []),
            key=lambda my_statistic: my_statistic.session_end,
            reverse=True,
        )

    @classmethod
    def write_statistics(cls, stats: StatisticRow) -> None:
        with open(statistics_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(stats.model_dump().values())
