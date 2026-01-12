from dataclasses import dataclass, astuple
from database import connect_db, Request


@dataclass(frozen=True, slots=True)
class UserStatistic:
    user_id: str
    session_start: str
    session_end: str
    difficulty: str
    correct: int
    incorrect: int


class StatisticsStorage:
    def __init__(self) -> None:
        pass

    def get_my_statistics(self, user_id: str) -> list[UserStatistic]:
        request = Request(
            query=""" SELECT session_start, session_end, difficulty, correct, incorrect
                                    FROM users_statistics
                                    WHERE user_id = ? """,
            param=(user_id,),
        )
        rows = connect_db(request=request).fetchall()
        return [UserStatistic(user_id, *row) for row in rows]

    def write_statistics(self, stats: UserStatistic) -> None:
        request = Request(
            query=""" INSERT INTO users_statistics (user_id, session_start, session_end, difficulty, correct, incorrect) VALUES (?, ?, ?, ?, ?, ?) """,
            param=(astuple(stats)),
        )
        connect_db(request=request)
