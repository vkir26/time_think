from pathlib import Path
import csv
from dataclasses import dataclass, asdict
from datetime import datetime

statistics_file = Path("users_statistics.csv")


@dataclass(frozen=True, slots=True)
class UserStatistic:
    user_id: str
    session_start: str
    session_end: str
    difficulty: str
    correct: str
    incorrect: str


def create_statistics_file() -> None:
    with open(statistics_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow((UserStatistic.__annotations__.keys()))


class StatisticsStorage:
    if not statistics_file.exists():
        create_statistics_file()

    def __init__(self) -> None:
        self.statistic = self.get_statistics
        self.datetime_format = "%d-%m-%Y %H:%M:%S"

    def get_statistics(self, user_id: str) -> list[UserStatistic]:
        my_statistic = []
        with open(statistics_file, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            for statistic in reader:
                statistical_data = UserStatistic(**statistic)
                if statistical_data.user_id == user_id:
                    my_statistic.append(statistical_data)
        return my_statistic

    def get_my_statistic(self, user_id: str) -> list[UserStatistic]:
        return sorted(
            self.statistic(user_id),
            key=lambda my_statistic: datetime.strptime(
                my_statistic.session_end, self.datetime_format
            ),
            reverse=True,
        )

    def write_statistics(self, stats: UserStatistic) -> None:
        with open(statistics_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(list(asdict(stats).values()))
