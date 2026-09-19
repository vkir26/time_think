from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from enum import StrEnum

from app.core import get_task, Task
from app.session import ModeSelection, difficulty_parameters, SessionParameters
from app.game_statistics import StatisticsStorage, UserStatistic
from app.messages import MenuMessage, RegisterMessage, AuthMessage, SessionMessage

from auth.config import (
    AccountStorage,
    peppered_password,
    create_access_token,
    jwt_secret_key,
    ALGORITHM,
)
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from jose import jwt, JWTError
from datetime import datetime
from app.database import connect_db, Request
from typing import Any

app = FastAPI()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Добро пожаловать в игру `Время думать`"}


router_v1 = APIRouter(prefix="/v1")


class AccountCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str = Field(min_length=5, max_length=15)


class RegisterAccountResponse(BaseModel):
    success_message: str


@router_v1.post("/signup")
def register_account(account: AccountCredentials) -> RegisterAccountResponse:
    username = account.username
    if name_is_exist(name=username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=RegisterMessage.NAME_EXISTS
        )

    password = account.password
    register(username=username, password=password)
    return RegisterAccountResponse(success_message=RegisterMessage.SUCCESS_REGISTER)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


SECURITY = HTTPBearer()


def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(SECURITY)) -> str:
    token = creds.credentials
    try:
        payload = jwt.decode(token=token, key=jwt_secret_key(), algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ID пользователя не найден",
            )
        return str(user_id)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен"
        )


@router_v1.post("/signin")
def authorization(credentials: AccountCredentials) -> AuthResponse:
    username = credentials.username
    password = peppered_password(credentials.password)

    account = AccountStorage().get_by_username(username=username)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=AuthMessage.USER_NOT_FOUND
        )

    user_id: str | None = authenticate(password=password, account=account)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthMessage.INCORRECT_PASSWORD,
        )
    access_token = create_access_token(user_id=user_id)
    return AuthResponse(access_token=access_token, token_type="bearer")


@router_v1.get("/how_to_play")
def how_to_play() -> dict[str, MenuMessage]:
    return {"message": MenuMessage.HOW_TO_PLAY}


class SessionStatus(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


def check_active_session(user_id: str) -> tuple[str, int, int] | None:
    request = Request(
        query=""" SELECT task, rounds, lives
                  FROM game_sessions
                  WHERE user_id = ?
                    AND is_active = ? """,
        param=(user_id, SessionStatus.ACTIVE),
    )
    session_data: tuple[str, int, int] | None = connect_db(request=request).fetchone()

    return session_data


class SessionMode(BaseModel):
    difficulty: ModeSelection = Field(default=ModeSelection.EASY)


class SessionData(BaseModel):
    question: Task = Field(default_factory=get_task)
    difficulty: SessionParameters


class SessionResponse(BaseModel):
    question: str
    difficulty: SessionParameters


@router_v1.post("/start")
def start_session(
    user_id: str = Depends(get_current_user_id), mode: SessionMode = Depends()
) -> SessionResponse:
    session_is_active = check_active_session(user_id=user_id)
    if session_is_active is not None:
        task, rounds, lives = session_is_active
        return SessionResponse(
            question=task, difficulty=SessionParameters(rounds, lives)
        )

    difficulty_level = difficulty_parameters[mode.difficulty]
    session = SessionData(question=get_task(), difficulty=difficulty_level)
    session_start = str(datetime.now())
    request = Request(
        query=""" INSERT INTO game_sessions (user_id, task, correct_answer, difficulty, rounds, lives, is_active, started_at)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
              """,
        param=(
            user_id,
            session.question.task,
            session.question.correct_answer.answer,
            mode.difficulty.name,
            session.difficulty.rounds,
            session.difficulty.lives,
            SessionStatus.ACTIVE,
            session_start,
        ),
    )
    connect_db(request=request)

    return SessionResponse(
        question=session.question.task,
        difficulty=difficulty_level,
    )


class SessionAnswer(BaseModel):
    answer: int


class UserSession(BaseModel):
    task: str
    correct_answer: int
    difficulty: str
    rounds: int
    lives: int
    correct_answers: int
    wrong_answers: int
    question_counter: int
    started_at: str


def session_validate(session_data: tuple[Any, ...]) -> UserSession:
    session_fields = list(UserSession.model_fields.keys())
    if len(session_data) != len(session_fields):
        raise ValueError("Некорректные данные сессии")

    current_session = dict(zip(session_fields, session_data))
    return UserSession.model_validate(current_session)


def gen_new_task(user_id: str) -> Task:
    new_task = get_task()
    request = Request(
        query=""" UPDATE game_sessions
                  SET task           = ?,
                      correct_answer = ?
                  WHERE user_id = ?
                    AND is_active = ? """,
        param=(
            new_task.task,
            new_task.correct_answer.answer,
            user_id,
            SessionStatus.ACTIVE,
        ),
    )
    connect_db(request=request)

    return new_task


class AnswerResponse(BaseModel):
    correct: bool
    correct_answers: int
    wrong_answers: int
    question: str


def session_end(user_id: str) -> None:
    request = Request(
        query=""" UPDATE game_sessions
                  SET is_active = ?
                  WHERE user_id = ? """,
        param=(SessionStatus.INACTIVE, user_id),
    )
    connect_db(request=request)


def add_statistics(
    user_id: str,
    session_start: str,
    session_end: str,
    difficulty: str,
    correct_answers: int,
    wrong_answers: int,
) -> None:
    StatisticsStorage().write_statistics(
        UserStatistic(
            user_id=user_id,
            session_start=session_start,
            session_end=session_end,
            difficulty=difficulty,
            correct=correct_answers,
            incorrect=wrong_answers,
        )
    )


class StatisticItem(BaseModel):
    session_start: str
    session_end: str
    difficulty: str
    correct: int
    incorrect: int


class MyStatsResponse(BaseModel):
    items: list[StatisticItem]
    total: int
    page: int
    page_size: int


@router_v1.get("/my_stats")
def show_my_stats(
    user_id: str = Depends(get_current_user_id), page: int = 1, page_size: int = 10
) -> MyStatsResponse:
    user_statistics = StatisticsStorage().get_my_statistics(
        user_id=user_id, limit=page_size, offset=(page - 1) * page_size
    )
    items = [
        StatisticItem(
            session_start=stat.session_start,
            session_end=stat.session_end,
            difficulty=stat.difficulty,
            correct=stat.correct,
            incorrect=stat.incorrect,
        )
        for stat in user_statistics
    ]
    return MyStatsResponse(
        items=items,
        total=StatisticsStorage().count_by_user(user_id=user_id),
        page=page,
        page_size=page_size,
    )


@router_v1.post("/answer")
def answer(
    user_answer: SessionAnswer, user_id: str = Depends(get_current_user_id)
) -> dict[str, str | int] | AnswerResponse:
    request = Request(
        query=""" SELECT task, correct_answer, difficulty, rounds, lives, correct_answers, wrong_answers, question_counter, started_at
                  FROM game_sessions
                  WHERE user_id = ?
                    AND is_active = ? """,
        param=(user_id, SessionStatus.ACTIVE),
    )
    session_data = connect_db(request=request).fetchone()
    if session_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SessionMessage.SESSION_NOT_FOUND,
        )
    session = session_validate(session_data=session_data)

    correct = session.correct_answer == user_answer.answer
    session.question_counter += 1
    if correct:
        session.correct_answers += 1
        if session.question_counter != session.rounds:
            new_task = gen_new_task(user_id=user_id)
            session.task = new_task.task
            session.correct_answer = new_task.correct_answer.answer

        request = Request(
            query=""" UPDATE game_sessions
                      SET correct_answers  = ?,
                          question_counter = ?
                      WHERE user_id = ?
                        AND is_active = ? """,
            param=(
                session.correct_answers,
                session.question_counter,
                user_id,
                SessionStatus.ACTIVE,
            ),
        )
    else:
        session.wrong_answers += 1
        request = Request(
            query=""" UPDATE game_sessions
                      SET wrong_answers    = ?,
                          question_counter = ?
                      WHERE user_id = ?
                        AND is_active = ? """,
            param=(
                session.wrong_answers,
                session.question_counter,
                user_id,
                SessionStatus.ACTIVE,
            ),
        )
    connect_db(request=request)

    if session.question_counter >= session.rounds:
        session_end(user_id=user_id)
        add_statistics(
            user_id=user_id,
            session_start=session.started_at,
            session_end=str(datetime.now()),
            difficulty=session.difficulty,
            correct_answers=session.correct_answers,
            wrong_answers=session.wrong_answers,
        )
        return {
            "message": SessionMessage.END_GAME,
            "correct": session.correct_answers,
            "wrong": session.wrong_answers,
        }

    if session.wrong_answers >= session.lives:
        session_end(user_id=user_id)
        add_statistics(
            user_id=user_id,
            session_start=session.started_at,
            session_end=str(datetime.now()),
            difficulty=session.difficulty,
            correct_answers=session.correct_answers,
            wrong_answers=session.wrong_answers,
        )
        return {"message": "Закончились жизни"}

    return AnswerResponse(
        correct=correct,
        correct_answers=session.correct_answers,
        wrong_answers=session.wrong_answers,
        question=session.task,
    )


app.include_router(router_v1)
