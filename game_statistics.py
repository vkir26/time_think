from pathlib import Path
import csv
from dataclasses import dataclass, asdict

statistics_file = Path("files/users_statistics.csv")


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
    def __init__(self) -> None:
        if not statistics_file.exists():
            create_statistics_file()
        self.statistic = self.get_statistics

    def get_statistics(self, user_id: str) -> list[UserStatistic]:
        my_statistic = []
        with open(statistics_file, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            for statistic in reader:
                statistical_data = UserStatistic(**statistic)
                if statistical_data.user_id == user_id:
                    my_statistic.append(statistical_data)
        return my_statistic

    def get_my_statistics(self, user_id: str) -> list[UserStatistic]:
        return sorted(
            self.statistic(user_id),
            key=lambda my_statistic: my_statistic.session_end,
            reverse=True,
        )

    def write_statistics(self, stats: UserStatistic) -> None:
        with open(statistics_file, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(list(asdict(stats).values()))
