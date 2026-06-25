from typing import Sequence, Union
from alembic import op


revision: str = "7ec086a7590f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id TEXT PRIMARY KEY,"
        "username TEXT NOT NULL UNIQUE,"
        "password TEXT NOT NULL)"
    )
    op.execute(
        "CREATE TABLE IF NOT EXISTS users_statistics ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id TEXT NOT NULL,"
        "session_start DATETIME,"
        "session_end DATETIME,"
        "difficulty TEXT,"
        "correct INTEGER,"
        "incorrect INTEGER,"
        "FOREIGN KEY (user_id) REFERENCES users(id));"
    )
    op.execute(
        "CREATE TABLE IF NOT EXISTS game_sessions ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id TEXT NOT NULL,"
        "task TEXT NOT NULL,"
        "correct_answer INTEGER NOT NULL,"
        "rounds INTEGER NOT NULL,"
        "lives INTEGER NOT NULL,"
        "correct_answers INTEGER DEFAULT 0 NOT NULL,"
        "wrong_answers INTEGER DEFAULT 0 NOT NULL,"
        "question_counter INTEGER DEFAULT 0 NOT NULL,"
        "is_active INTEGER DEFAULT 0 NOT NULL,"
        "FOREIGN KEY (user_id) REFERENCES users(id));"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
