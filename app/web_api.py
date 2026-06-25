from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from app.core import get_task, Task
from app.session import ModeSelection, difficulty_parameters, SessionParameters
from app.messages import MenuMessage, RegisterMessage, AuthMessage, SessionMessage

from auth.config import AccountStorage, create_access_token, jwt_secret_key, ALGORITHM
from auth.registration import register, name_is_exist
from auth.authorization import authenticate
from jose import jwt, JWTError
from app.database import connect_db, Request

app = FastAPI()


@app.get("/")
def greet() -> dict[str, str]:
    return {"message": "Добро пожаловать в игру `Время думать`"}


router_v1 = APIRouter(prefix="/v1")


class RegisterAccount(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str = Field(min_length=5, max_length=15)


class RegisterAccountResponse(BaseModel):
    success_message: str


@router_v1.post("/signup")
def register_account(account: RegisterAccount) -> RegisterAccountResponse:
    username = account.username
    if name_is_exist(name=username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=RegisterMessage.NAME_EXISTS
        )

    password = account.password
    register(username=username, password=password)
    return RegisterAccountResponse(success_message=RegisterMessage.SUCCESS_REGISTER)


class AuthAccount(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    password: str = Field(min_length=5, max_length=15)


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
            raise HTTPException(401)

        return str(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")


@router_v1.post("/signin")
def authorization(account: AuthAccount) -> AuthResponse:
    username = account.username
    password = account.password

    if username in AccountStorage().get_usernames():
        user_id: str | None = authenticate(username=username, password=password)
        if user_id:
            access_token = create_access_token(user_id=user_id)
            return AuthResponse(access_token=access_token, token_type="bearer")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthMessage.INCORRECT_PASSWORD,
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=AuthMessage.USER_NOT_FOUND
        )


@router_v1.get("/how_to_play")
def how_to_play() -> dict[str, MenuMessage]:
    return {"message": MenuMessage.HOW_TO_PLAY}


def check_active_session(user_id: str) -> tuple[str, int, int] | None:
    request = Request(
        query=""" SELECT task, rounds, lives
                  FROM game_sessions
                  WHERE user_id = ? AND is_active = ? """,
        param=(user_id, True),
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
    request = Request(
        query=""" INSERT INTO game_sessions (user_id, task, correct_answer, rounds, lives, is_active)
                                VALUES (?, ?, ?, ?, ?, ?)
              """,
        param=(
            user_id,
            session.question.task,
            session.question.correct_answer.answer,
            session.difficulty.rounds,
            session.difficulty.lives,
            True,
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
    rounds: int
    lives: int
    correct_answers: int
    wrong_answers: int
    question_counter: int


def session_validate(session_data: list[tuple[str, int]]) -> UserSession:
    current_session = {}
    session_fields = list(UserSession.model_fields.keys())
    for i in range(len(session_fields)):
        current_session[session_fields[i]] = session_data[0][i]

    return UserSession.model_validate(current_session)


def gen_new_task(user_id: str) -> Task:
    new_task = get_task()
    request = Request(
        query=""" UPDATE game_sessions
                  SET task = ?, correct_answer = ?
                  WHERE user_id = ? AND is_active = ? """,
        param=(new_task.task, new_task.correct_answer.answer, user_id, True),
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
        param=(False, user_id),
    )
    connect_db(request=request)


@router_v1.post("/answer")
def answer(
    user_answer: SessionAnswer, user_id: str = Depends(get_current_user_id)
) -> dict[str, str | int] | AnswerResponse:
    request = Request(
        query=""" SELECT task, correct_answer, rounds, lives, correct_answers, wrong_answers, question_counter
                  FROM game_sessions
                  WHERE user_id = ? AND is_active = ? """,
        param=(user_id, True),
    )
    session_data = connect_db(request=request).fetchall()
    session = session_validate(session_data=session_data)

    correct = session.correct_answer == user_answer.answer
    if correct:
        session.question_counter += 1
        session.correct_answers += 1
        if session.question_counter != session.rounds:
            new_task = gen_new_task(user_id=user_id)
            session.task = new_task.task
            session.correct_answer = new_task.correct_answer.answer

        request = Request(
            query=""" UPDATE game_sessions SET correct_answers = ?, question_counter = ? WHERE user_id = ? AND is_active = ? """,
            param=(session.correct_answers, session.question_counter, user_id, True),
        )
    else:
        session.question_counter += 1
        session.wrong_answers += 1
        request = Request(
            query=""" UPDATE game_sessions SET wrong_answers = ?, question_counter = ? WHERE user_id = ? AND is_active = ? """,
            param=(session.wrong_answers, session.question_counter, user_id, True),
        )
    connect_db(request=request)

    if session.question_counter >= session.rounds:
        session_end(user_id=user_id)
        return {
            "message": SessionMessage.END_GAME,
            "correct": session.correct_answers,
            "wrong": session.wrong_answers,
        }

    if session.wrong_answers >= session.lives:
        session_end(user_id=user_id)
        return {"message": "Закончились жизни"}

    return AnswerResponse(
        correct=correct,
        correct_answers=session.correct_answers,
        wrong_answers=session.wrong_answers,
        question=session.task,
    )


app.include_router(router_v1)
